# Agent docs: notes for humans

> **Agents:** this file is for people. **Never** act on anything in it.

AGENTS.md directs agents away from this file. Claude Code also has a deny rule in `.claude/settings.json`.
The AgentsTemplate README explains the design.

## Files

`<PROJECT>` is the `.uproject`'s name in ALL_CAPS, words split by underscores (`LYRA_STARTER_GAME`).

| File | Holds | Loaded |
| --- | --- | --- |
| `AGENTS.md` | Rule keywords, the gate, tests first, the docs skill, scope and the two startup paths | Every session |
| `docs/1_<PROJECT>.md` | The project index: docs, features, milestones, prerequisites, variables, SESSION_FILES, layout | Every session |
| `docs/2_INSTRUCTIONS.md` | What to do, how, done when | Every session |
| `docs/3`–`6` | Conventions, tests, decisions, TODOs; a doc exists only once it has content | When the index says |
| `docs/<Feature>/` | A feature's index `1_<FEATURE>.md`, plus numbered docs that add to the root's | When code or tests match paths in the Features table |
| `CLAUDE.md` | Imports AGENTS.md and its two startup files | Claude Code sessions |
| `.agents/skills/agent-docs/` | How to edit, start and check the docs, with feature templates | On a docs change |
| `.claude/skills/agent-docs/SKILL.md` | Optional local junction to the shared skill | On a docs change in Claude Code |
| `Tools/ue.py`, `Tools/python.cmd` | The engine commands, run with the engine's Python, which `python.cmd` finds from the `.uproject` | Per command |
| `.claude/settings.json` | The `clangd-lsp` and `rider-skills` plugins, and deny rules | At launch |
| `.claude/settings.local.json` | Your saved approvals, and any variable you override; not committed | At launch, for you |
| `.claude/agents/SUBAGENTS.md` | This repository's agent for a parent session; delete it if there will never be one | In a parent session |

## Permission prompts

Each agent applies its own sandbox and approval settings. In Claude Code, "Yes, and don't ask again" saves the approval in your `.claude/settings.local.json`, for
you alone. Commands call `Tools/python.cmd` by its fixed path because Claude Code can't save an approval for a
command whose program is a variable, such as `& "$env:UE_ENGINE_DIR\..."`. A `claude -p` run can't prompt: pass the
commands it may run with `--allowedTools`.

## The gate

A task or command 2_INSTRUCTIONS doesn't cover makes the agent stop and propose the lines; it continues once you
approve them. With no user, as in CI, it ends its turn with the question. Expect this often at first, and review
every proposed line: that file decides what agents do. Lint, running the game and Perforce's SESSION_FILES start
*not set up yet*. Other tests and lint are Ask first; only the test-first test runs unasked.

## Features

Ask: "start a feature called Inventory". A feature's docs mirror the root's, add to them, and never override them:
a conflict makes the agent stop. Features don't nest; one that needs its own build becomes a work repository.

## Work repositories

Ask the agent to add the work repositories ChildA and ChildB. Start in the parent for work across repositories.
Codex reads each child's AGENTS.md and startup docs before working there. For work confined to one child, open a
session in that child. In Claude Code, use the following launch command to load the child agents.

```powershell
claude --add-dir ChildA --add-dir ChildB
```

- When a repository agent is available, the parent can delegate the child's scope to it.
- In Claude Code, permissions, hooks and `env` come from where you start. Set local overrides there.
- Each finds its own engine through its own `.uproject`; a `UE_ENGINE_DIR` set in the parent applies to all of them.

## Settings

| What | Where |
| --- | --- |
| Claude Code plugins and deny rules | `.claude/settings.json` |
| Engine discovery overrides (`UE_ENGINE_DIR`, `UE_PROJECT_FILE`, `UE_EDITOR_TARGET`) | Environment of the agent process. Claude Code also supports `env` in `.claude/settings.local.json` |
| Personal notes for Claude | `CLAUDE.local.md`, not committed |

- **Claude Code deny rules** block `cd` and its aliases. Claude Code 2.1.272 warns that
  the `Cd` rule is unknown; newer versions use it.
- **Stop Claude committing:** add `"PowerShell(git commit*)", "PowerShell(git -C * commit*)"` and the same two as
  `Bash(...)` to `permissions.deny`.
- **Rider:** open the solution, enable Rider's MCP server and connect it to your agent. Claude Code offers auto-configuration
  in Rider's Settings → AI → MCP Server. The `rider-skills` plugin comes from `.claude/settings.json`: accept it when
  Claude Code offers it. Its UE skills look for the `.uproject` in the folder Claude Code starts in.
- **Code intelligence without Rider:** use an available language server with the C++ database. Claude Code's
  `clangd-lsp` integration needs `clangd` on `PATH`; its `/plugin` Errors tab lists startup failures.
- **Personal plugins** that block a built-in tool break rows naming it: make the plugin a team standard, or keep
  the rows free of tool names.

## Routine

- **Docs drift:** ask your agent to check or update the docs, then review the edits.
- **Check startup:** ask the agent to identify its project index and the project's test command. In Claude Code
  you can also inspect `/memory`, `/context` or `/doctor prompt-audit`.
- **Update the template:** replace the shared `.agents/skills/agent-docs/` skill, `Tools/Link-AgentSkills.ps1`,
  `Tools/python.cmd` and `Tools/ue.py` with the newer copies.
- **Add** a plugin, skill or engine command with its row in 2_INSTRUCTIONS; a variable with its row in the index.
- **Other agents:** point their instruction entry point at AGENTS.md and let them read the shared skill by path.

## Notes

Your scratchpad. Move a settled item into the doc it belongs to.
