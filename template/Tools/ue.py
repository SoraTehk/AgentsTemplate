"""Unreal commands for agents, run as: Tools/python.cmd Tools/ue.py <command> [argument]

  build [-Flag ...]      Build the editor target, adding any extra Unreal Build Tool flags, such as -NoUBA.
  clang-db [-Flag ...]   Write compile_commands.json at the repository root, with the same extra flags.
  test <filter>          Run every automation test whose full name starts with the filter.
  editor-python <script> Run one Python script inside the editor.
  engine                 Print the engine's root folder: UE_ENGINE_DIR, else the one the .uproject names.

Each prints what it ran and its result, then `exit <code>` as its last line.
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import NoReturn

ROOT = Path(__file__).resolve().parent.parent


def env_path(name):
    # Tools/python.cmd sets UE_ENGINE_DIR from the .uproject's EngineAssociation when nobody else has.
    value = os.environ.get(name, "").strip()
    if not value:
        finish(2, f"{name} is not set: set it in .claude/settings.local.json, then start a new session.")
    return Path(value)


def finish(code, message=None) -> NoReturn:
    if message:
        print(message)
    print(f"exit {code}")
    sys.exit(code)


def engine():
    return env_path("UE_ENGINE_DIR") / "Engine"


def project():
    # The .uproject at the repository root, else in one folder below it (Vault keeps it in Vault/), so each work
    # repository finds its own; UE_PROJECT_FILE overrides it.
    if os.environ.get("UE_PROJECT_FILE", "").strip():
        path = env_path("UE_PROJECT_FILE")
        if not path.is_file():
            finish(2, f"UE_PROJECT_FILE names no file: {path}")
        return path
    found = sorted(ROOT.glob("*.uproject")) or sorted(ROOT.glob("*/*.uproject"))
    if len(found) != 1:
        finish(2, f"{len(found)} .uproject files in {ROOT}: set UE_PROJECT_FILE in .claude/settings.local.json.")
    return found[0]


def flags(arguments):
    # Extra Unreal Build Tool flags, each a plain -Flag or -Flag=value, so nothing else reaches cmd's command line.
    for flag in arguments:
        if not re.fullmatch(r"-[\w.+\-]+(=[\w.+\-:\\/]+)?", flag):
            finish(2, f"Not an Unreal Build Tool flag: {flag}")
    return "".join(" " + flag for flag in arguments)


def editor_target():
    # <Project>Editor when it exists, else the only *Editor target: Lyra's project is LyraStarterGame, its target
    # LyraEditor. UE_EDITOR_TARGET overrides both.
    name = os.environ.get("UE_EDITOR_TARGET", "").strip()
    if name:
        return name
    source = project().parent / "Source"
    if (source / f"{project().stem}Editor.Target.cs").is_file():
        return f"{project().stem}Editor"
    found = sorted(path.name[:-len(".Target.cs")] for path in source.glob("*Editor.Target.cs"))
    if len(found) != 1:
        finish(2, f"{len(found)} editor targets in {source}: set UE_EDITOR_TARGET in .claude/settings.local.json.")
    return found[0]


def run_batch(bat, args):
    # cmd /s strips exactly the outer quotes, so the quoted batch path and quoted arguments inside reach it unchanged.
    # Output streams straight through, as when the batch file runs in the shell itself.
    return subprocess.run(f'cmd.exe /d /s /c ""{bat}" {args}"').returncode


def run_editor(args, log):
    # Unreal reads its raw command line, not argv, so it is passed as one string with -Key="value" quoting.
    # No pipes and no inherited handles: waiting on a pipe would also wait for the MSBuild and shader workers the editor
    # leaves running. Its output goes to the log instead.
    log.parent.mkdir(parents=True, exist_ok=True)
    log.unlink(missing_ok=True)
    editor = engine() / "Binaries" / "Win64" / "UnrealEditor-Cmd.exe"
    command = (f'"{editor}" "{project()}" {args} -unattended -nullrhi -nosplash -nosound -nop4 '
               f'-ABSLOG="{log}"')
    code = subprocess.run(command, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          creationflags=subprocess.CREATE_NO_WINDOW).returncode
    if not log.is_file():
        finish(1, f"The editor exited with {code} and wrote no log at {log}")
    return code, log.read_text(encoding="utf-8-sig", errors="replace").splitlines()


def build(arguments):
    finish(run_batch(engine() / "Build" / "BatchFiles" / "Build.bat",
                     f'{editor_target()} Win64 Development "-Project={project()}" -WaitMutex -NoHotReloadFromIDE'
                     + flags(arguments)))


def clang_db(arguments):
    finish(run_batch(engine() / "Build" / "BatchFiles" / "RunUBT.bat",
                     f'-Mode=GenerateClangDatabase "-Project={project()}" {editor_target()} Win64 Development '
                     f'"-OutputDir={ROOT}"' + flags(arguments)))


def one(arguments):
    if len(arguments) > 1:
        finish(2, "Give it one argument.")
    return arguments[0] if arguments else None


def test(arguments):
    test_filter = one(arguments) or ""
    if not test_filter:
        finish(2, "Name a test, or a prefix such as the project's name.")
    if not re.fullmatch(r"[\w.+\-]+", test_filter):
        finish(2, f"Not a test name or prefix: {test_filter}")
    log = project().parent / "Saved" / "Logs" / "AgentTests.log"
    _, lines = run_editor(f'-ExecCmds="Automation RunTests {test_filter}; Quit"', log)
    results = [line for line in lines if re.search(r"Test Completed\. Result=|No automation tests matched", line)]
    print("\n".join(results) or f"No test results in {log}")
    passed = bool(results) and all("Result={Success}" in line for line in results)
    finish(0 if passed else 1)


def editor_python(arguments):
    argument = one(arguments)
    if not argument:
        finish(2, "Name the script to run.")
    script = Path(argument).resolve()
    if not script.is_file():
        finish(2, f"No script at {script}")
    log = project().parent / "Saved" / "Logs" / "AgentPython.log"
    code, lines = run_editor(f'-run=pythonscript -script="{script}" -EnablePlugins=PythonScriptPlugin', log)
    # The engine's own shutdown lines ("... externally referenced when shutting down Python") follow every script.
    lines = [line for line in lines if "LogPython" in line and "when shutting down Python" not in line]
    start = next((i for i, line in enumerate(lines) if "Running Python script" in line), 0)
    print("\n".join(lines[start:]))
    finish(code)


def engine_root(_):
    finish(0, str(engine().parent))


COMMANDS = {"build": build, "clang-db": clang_db, "test": test, "editor-python": editor_python,
            "engine": engine_root}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        finish(2, (__doc__ or "").strip())
    COMMANDS[sys.argv[1]](sys.argv[2:])
