# Agent docs: notes for humans

This file is for people. Claude Code is blocked from reading it (`Read(./docs/_HUMANS.md)` in
`.claude/settings.json`), and no agent doc links to it, so it costs agents no tokens. To have Claude
edit it, remove that deny rule for the session.

## The files

| File | Job | Loaded |
| --- | --- | --- |
| `AGENTS.md` | Enforces 2.INSTRUCTIONS and test-first, and indexes the docs | Every turn, every agent |
| `CLAUDE.md` | `@AGENTS.md`, so Claude Code reads the same index | Every turn, Claude only |
| `docs/1.PROJECT.md` | Facts: purpose, milestones, prerequisites, layout | On demand |
| `docs/2.INSTRUCTIONS.md` | How to do things: shell commands, tool per action, a playbook per task | Before the first action |
| `docs/3.CONVENTIONS.md` | What code looks like: style, naming, architecture, contracts | Before writing code |
| `docs/4.TEST.md` | How tests are written, so they can come first | Before writing code |
| `docs/5.DECISIONS.md` | Why things are the way they are | Before reversing a choice |
| `docs/6.TODOS.md` | Deferred work an agent must know about while editing | Before refactoring |
| `docs/<Feature>/README.md` | One feature's contract and workings | Via the index, or the path rule below |
| `.claude/rules/<Feature>.md` | Makes Claude read the feature doc when it touches that code | When a matching file is touched |
| `docs/_FEATURE_TEMPLATE/` | The README and rule to copy when starting a feature | When a feature is created |
| `.claude/settings.json` | Plugins, and permissions: what runs without asking, what is never read | At launch, only in this repository |
| `.claude/agents/SUBAGENTS.md` | This repository's agent, used when a parent session adds it with `--add-dir`. Any filename loads; the `.md` extension, valid YAML frontmatter, and a `name` unique across the workspace are what count | In the parent session |
| `docs/_HUMANS.md` | This file | Never, by agents |

## The gate

If a task matches no playbook in 2.INSTRUCTIONS, or needs a command or tool it doesn't list, the agent
stops, proposes the missing lines, and continues once they're in the file. Expect this often at first;
2.INSTRUCTIONS grows out of real gaps. Review every proposed line: that file decides what agents do.

A new project starts with every command and the test framework marked *not set up yet*. That's
deliberate: the first task that needs a build or a test makes the agent stop and propose one, so these
get set up by the work that needs them, with you approving each line. The other defaults (tools, git
format, conventions, test practice) suit most projects; edit any that yours decides differently.

## Where to start the agent

**With work repositories, start in the parent and add each one:**

```sh
claude --add-dir ChildA --add-dir ChildB
```

One session then holds every repository, and you type only there. The parent delegates work inside a
work repository to that repository's agent (`.claude/agents/`), which works in its own context and can
be resumed for follow-ups. Tested on Claude Code 2.1.296, with work repositories nested inside the parent:

| From each `--add-dir` repository | Loaded? |
| --- | --- |
| Skills, slash commands, agents | Yes |
| `CLAUDE.md` / `AGENTS.md` and rules | Yes, because the parent's settings set `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` |
| Plugins it enables | Yes, once installed on this machine (the first interactive session offers it) |
| Plugins it disables | No: it can't turn off a plugin you enabled yourself |
| Permissions, hooks, `env` | **No.** These come only from the folder you started in. Put rules that must hold in a parent session into the parent's settings, or into the work repository's agent frontmatter |

`settings.json` can't make `--add-dir` permanent (`permissions.additionalDirectories` grants file access
only), so keep the command in a shell alias or script.

Other ways to start:

| Started in | Gets | Use when |
| --- | --- | --- |
| A work repository, on its own | Its full setup, plus every parent's instructions | Long work inside that one repository |
| A repository cloned alone | Its own setup only | It isn't part of a workspace |

Codex and other agents read only the AGENTS.md files from the git root down to where they start, so
there, start in the repository you're working on.

## The working directory never changes

Every session stays in the folder it started in, so paths always mean the same thing and the parent never
ends up running a child's commands from the wrong place. Three layers hold this:

| Layer | What it does |
| --- | --- |
| 2.INSTRUCTIONS "Run a shell command" | Tells the agent to pass directories as arguments (`git -C`, `cmake -S/-B`) and never `cd` |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` in `settings.json` | Claude Code returns to the starting folder after every Bash or PowerShell command anyway |
| Deny rules in `settings.json` | Block `cd`, `pushd`, `Set-Location` and their aliases, in combined commands too, and `Cd` turns off `/cd` |

Deny rules match the command text Claude writes, so they catch the usual spellings but aren't a security
boundary. A tool that only works from its own folder needs a wrapper that takes the folder as an argument,
added to 2.INSTRUCTIONS before use.

## Claude Code defaults, deliberately not written down

Claude Code's built-in system prompt already makes it: use its file tools instead of `cat`, `find`,
`grep`, `sed` or `echo >`; read a file before editing it; prefer editing to creating files; confirm
before destructive or hard-to-reverse actions; commit and push only when asked; never skip hooks
(`--no-verify`) or use interactive git (`-i`). Repeating these in 2.INSTRUCTIONS spends tokens every
session for nothing. Write a rule there only when this repository wants something different. These
defaults can change between Claude Code versions, so recheck before relying on one.

## How these docs relate to Claude Code features

| Ours | Claude Code feature | How they combine |
| --- | --- | --- |
| `AGENTS.md` + `CLAUDE.md` | Memory files, native AGENTS.md | Built on the feature |
| The gate in AGENTS.md | Permissions, hooks | The gate is guidance. For hard enforcement, list the shell commands from 2.INSTRUCTIONS in `permissions.allow`: those run without asking, anything else prompts you |
| 4.TEST test-first | Hooks | Guidance. To enforce it, add a hook that runs the test suite before the agent finishes |
| 2.INSTRUCTIONS playbooks | Skills | Overlap by design. A playbook is reached through the gate every time; a skill loads only if Claude picks it. Turn a playbook into a skill only when it outgrows ~10 steps or needs scripts, and leave a one-line playbook pointing to it |
| 2.INSTRUCTIONS "Find a symbol" row | Code intelligence (LSP) plugins | Built on the feature: the `LSP` tool for navigation, plus diagnostics after every edit |
| 2.INSTRUCTIONS commands and setup | `/run-skill-generator`, `/verify` | Both record build and launch recipes as `.claude/skills/run-<name>/`, a second copy of your commands. Keep 2.INSTRUCTIONS as the source; if you generate one, make it point there |
| 3.CONVENTIONS | `.claude/rules/` with `paths` | Repository-wide conventions stay in 3.CONVENTIONS, for every agent. A convention for one directory or language can be a path rule instead, auto-loaded by Claude only. Never keep it in both |
| `docs/<Feature>/` | `.claude/rules/` with `paths` | Built on the feature |
| 5.DECISIONS | Auto memory | No clash: auto memory is private to your machine. During a sync, move anything there the team needs (`/memory` shows it) |
| 6.TODOS | The in-session task list | No clash: the task list lasts one session. The index says so |
| The sync playbook | `/init`, `/doctor prompt-audit` | Don't run `/init` here: it writes content into `CLAUDE.md` and breaks the one-line import. Run `/doctor prompt-audit` after a sync: it finds contradictions and dead references |
| Hiding this file | Permissions `deny` | Built on the feature |

## Your settings or the repository's

Anything installed or set in `~/.claude/settings.json` works only for you. A new developer gets only
what the repository's `.claude/settings.json` declares.

| Setting | Where | Why |
| --- | --- | --- |
| Plugins the code needs (a language's LSP plugin, project tooling) | Repository | Everyone working here needs them; 2.INSTRUCTIONS names their tools |
| The `claude-plugins-official` marketplace entry | Repository (already in the template) | A fresh machine doesn't know that marketplace until its first interactive session, so plugins from it would fail to resolve |
| Permissions for this repository's commands and secrets | Repository | Same rules for everyone |
| Model, effort level, update channel, theme | You | Personal preference; the docs don't depend on them |
| Personal plugins, skills and hooks | You | Unless the team agrees to make one standard |

**Plugins that change built-in tools.** Some personal plugins block or redirect a built-in tool, for
example to save context. On that machine, a 2.INSTRUCTIONS row naming the blocked tool won't work. Either
make the plugin a team standard (declare it in the repository and name its tools in 2.INSTRUCTIONS), or
keep that row free of tool names.

**Code intelligence.** Enable one official LSP plugin per language the repository uses. Each needs its
language server on `PATH`, so list that in 1.PROJECT Prerequisites:

| Language | Plugin | Language server | Install (see the plugin's README for other systems) |
| --- | --- | --- | --- |
| C/C++ | `clangd-lsp` | `clangd` | `winget install LLVM.LLVM` |
| C# | `csharp-lsp` | `csharp-ls` | `dotnet tool install --global csharp-ls` |
| Python | `pyright-lsp` | `pyright-langserver` | `npm install -g pyright` |
| Lua | `lua-lsp` | `lua-language-server` | Release download, or a package manager |
| TypeScript | `typescript-lsp` | `typescript-language-server` | `npm install -g typescript-language-server typescript` |

It works if a `Found N new diagnostic issues` line appears after Claude edits a file of that language.
If it doesn't, check the Errors tab in `/plugin` for `Executable not found in $PATH`. Cloud sessions don't
start language servers at all.

## Routine

**Sync the docs** in a fresh session, in the repository whose code changed:

> Sync the docs with the code for `main..HEAD`.

Any git range works. With no range, the agent uses the commits since `docs/` last changed. The playbook
"Sync the docs with the code" in 2.INSTRUCTIONS does the rest. For a contract between repositories, sync
the repository that owns it first.

**Check what loaded:** `/memory` lists the instruction files, `/context` shows what they cost, and
`/doctor prompt-audit` reviews them.

**Add to the environment:**

- A plugin: `"<plugin>@<marketplace>": true` in `enabledPlugins` (browse with `/plugin`). A marketplace
  other than the official one also needs an `extraKnownMarketplaces` entry. Then add its row to
  2.INSTRUCTIONS "Skills and plugins". If you already installed it for yourself, still declare it here.
- A skill: `.claude/skills/<name>/SKILL.md`, plus its row in 2.INSTRUCTIONS.
- An MCP server: `.mcp.json`. Each person approves it once.
- Personal settings: `CLAUDE.local.md` and `.claude/settings.local.json`. Both are git-ignored.
