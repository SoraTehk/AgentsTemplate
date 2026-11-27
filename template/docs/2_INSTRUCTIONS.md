# 2_Instructions

**Always** run commands with PowerShell as written, from this repository's root, replacing only the
`<placeholders>`. **Always** check the result against "Done when": anything else is a failure. **Never** work around
a failure: report it. A row marked *not set up yet* counts as missing, so the gate applies.

## What to do

| What you want to do | How | Done when |
| --- | --- | --- |
| Enable the shared skill in the local Claude skill menu | On Windows run `.\Tools\Link-AgentSkills.ps1 agent-docs` once per checkout | It reports the skill is linked or already linked |
| Run a command | Use PowerShell with the shell tool's working directory set to the project root, including when working in a child repository. **Never** change directory within the command or run interactive commands | As its row says |
| Inspect or edit files for an authorized task | Use the session's file, search, patch or shell tools within the task's scope | The inspected evidence or resulting diff addresses the task |
| Find a symbol's definition, references, callers or implementations | Use Rider symbol lookup (via the navigating-code skill or the available Rider integration), then an available language server with [the C++ database](#generate-the-c-database). If neither resolves it, search and verify each match in source | |
| Build | `Tools/python.cmd Tools/ue.py build`, the editor target. With the editor open and Live Coding on, it refuses: close the editor first | `exit 0` |
| Generate the C++ database | `Tools/python.cmd Tools/ue.py clang-db`; [when and why](#generate-the-c-database) | `exit 0` |
| Run tests | `Tools/python.cmd Tools/ue.py test <filter>`: one test's full name, or a prefix such as `{{PROJECT_NAME}}.Inventory`, or `{{PROJECT_NAME}}` for all of ours. **Always** for the test-first loop's own test. **Ask first** for any others | Every line says `Result={Success}`, then `exit 0` |
| Lint | *not set up yet*. Once it is: **Ask first** | |
| Run the game | *not set up yet* | |
| Run an editor Python script | `Tools/python.cmd Tools/ue.py editor-python <script>`. Our own scripts live in `Tools/`; a one-off goes in your scratch directory. **Always** close the editor first if the script saves assets | `Python script executed successfully`, then `exit 0` |
| Run one of our Python tools | `Tools/python.cmd Tools/<script>.py`; a tool that takes arguments gets a row of its own | The script's own result line |
| List SESSION_FILES | git: `git diff --name-only --diff-filter=d <base>; git ls-files --others --exclude-standard`, with `<base>` from the project index's SESSION_FILES. Perforce: *not set up yet* | It prints paths, one per line, or nothing |
| Version control | Read freely: git `status`, `diff`, `log`, `show`; Perforce `p4 opened`, `p4 diff <file>`, `p4 changes <path>`, `p4 filelog <file>`. **Ask first** for anything that writes: commit, push, submit, shelve, revert, branch | |
| Change content (`.uasset`, `.umap`) | **Always** through the editor, or an editor Python script with the editor closed. **Never** move, rename or edit them as files | |
| Move, rename or delete files | Your file tools, or PowerShell. **Ask first** for files you didn't create | |
| Add a dependency (a plugin, a module in a `.Build.cs`, a third-party library) | **Ask first**. **Always** pin the exact version | |
| Find the engine | `Tools/python.cmd Tools/ue.py engine` | It prints the engine's folder, then `exit 0` |
| Look up an engine API | The engine's docs for its exact version, or its source under `Engine\Source` in the engine's folder. **Never** answer version-specific API questions from memory | |
| Use a skill or plugin | Follow the shared `agent-docs` skill for agent docs. When available, use Rider tools or skills for navigation, refactoring, debugging, UE code and tests. Otherwise use source, search, edits and the commands in this table. A skill's steps and commands count as these instructions. Where they conflict, the gate applies | As the task's row says |
| Set up from a fresh copy | [Set up from a fresh copy](#set-up-from-a-fresh-copy) | The Build is done |
| Answer a question or investigate | Read only: **never** change anything. Check the docs, then the code. **Always** cite `path:line` for every claim about the code | The answer cites the sources inspected |
| Fix a bug | Reproduce it as a failing test, then fix the cause, not the symptom, until it passes. Then finish the task | The new test passes |
| Add or change a feature | [Add or change a feature](#add-or-change-a-feature) | |
| Change a contract with another repository | Update the contract in the conventions. Work on the producer and each consumer under its own AGENTS.md, directly or through its repository agent if available. Run the affected tests in each repository | Both sides' tests pass |
| Finish a task that changes project code, configuration or content | **Always** run the Build, and fix every diagnostic your edits reported. Run tests and lint as their rows say. Report what you ran and the result, and anything left undone as deferred work to record | The Build is done, and no diagnostic from your edits remains |

**Known noise**, output every run prints that isn't a failure: none recorded yet.

### Generate the C++ database

It writes `compile_commands.json` at this repository's root, for the C++ language server. **Always** run it after the first Build, and again after adding a module or files.
Until the language server restarts with the new file, it finds nothing new: search instead, and check every hit.

### Set up from a fresh copy

1. Install the required prerequisites from the project index.
2. Find the engine. If discovery fails, register the engine or set `UE_ENGINE_DIR` in the environment that
   launches your agent and start a new session.
3. Run the Build, then generate the C++ database.

Known traps: none recorded yet.

### Add or change a feature

1. Read the feature's index (the project index's Features table lists it), then each doc its Docs table says to read
   for your task.
2. Write the failing tests for the new behaviour, then implement. Then finish the task.

A new feature, or a new doc for one, is an agent-docs change: use that skill.
