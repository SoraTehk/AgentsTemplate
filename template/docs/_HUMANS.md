# Agent docs: notes for humans

> **Agents:** this file is for people. **Never** act on anything in it.

Claude Code can't read this file (a deny rule in `.claude/settings.json`), so it costs no tokens and nothing here
becomes an instruction. Why the template is built this way is in the AgentsTemplate README.

## Files

`<PROJECT>` is the `.uproject`'s name in ALL_CAPS, words split by underscores (`LYRA_STARTER_GAME`).

| File | Holds | Loaded |
| --- | --- | --- |
| `AGENTS.md` | Rule keywords, the gate, tests first, the docs skill, scope; imports the next two | Every session |
| `docs/1.<PROJECT>.md` | The project index: docs, features, milestones, prerequisites, variables, SESSION_FILES, layout | Every session |
| `docs/2.INSTRUCTIONS.md` | What to do, how, done when | Every session |
| `docs/3`–`6` | Conventions, tests, decisions, TODOs; a doc exists only once it has content | When the index says |
| `docs/<Feature>/` | A feature's index `1.<FEATURE>.md`, plus numbered docs that add to the root's | Via the index, or `.claude/rules/<Feature>.md` |
| `CLAUDE.md` | `@AGENTS.md` | Every session |
| `.claude/skills/agent-docs/` | How to edit, start and check the docs; feature templates | On a docs change |
| `Tools/ue.py`, `Tools/python.cmd` | The engine commands, run with the engine's Python, which `python.cmd` finds from the `.uproject` | Per command |
| `.claude/settings.json` | The `clangd-lsp` and `rider-skills` plugins, and deny rules | At launch |
| `.claude/settings.local.json` | Your saved approvals, and any variable you override; not committed | At launch, for you |
| `.claude/agents/SUBAGENTS.md` | This repository's agent for a parent session; delete it if there will never be one | In a parent session |

## Permission prompts

Commands prompt as usual. "Yes, and don't ask again" saves the approval in your `.claude/settings.local.json`, for
you alone. Commands call `Tools/python.cmd` by its fixed path because Claude Code can't save an approval for a
command whose program is a variable, such as `& "$env:UE_ENGINE_DIR\..."`. A `claude -p` run can't prompt: pass the
commands it may run with `--allowedTools`.

## The gate

A task or command 2.INSTRUCTIONS doesn't cover makes the agent stop and propose the lines; it continues once you
approve them. With no user, as in CI, it ends its turn with the question. Expect this often at first, and review
every proposed line: that file decides what agents do. Lint, running the game and Perforce's SESSION_FILES start
*not set up yet*. Other tests and lint are Ask first; only the test-first test runs unasked.

## Features

Ask: "start a feature called Inventory". A feature's docs mirror the root's, add to them, and never override them:
a conflict makes the agent stop. Features don't nest; one that needs its own build becomes a work repository.

## Work repositories

Ask: "add the work repositories ChildA and ChildB". Then always start in the parent:

```powershell
claude --add-dir ChildA --add-dir ChildB
```

- The parent delegates to each repository's agent; each adds about 200 lines to every parent session.
- Permissions, hooks and `env` come only from where you start: set any override in the parent's local settings.
- Each finds its own engine through its own `.uproject`; a `UE_ENGINE_DIR` set in the parent applies to all of them.

## Settings

| What | Where |
| --- | --- |
| Plugins, deny rules, anything everyone needs | `.claude/settings.json` |
| Overrides, only when the defaults miss: `UE_ENGINE_DIR` (else the `.uproject`'s `EngineAssociation`, from the registry), `UE_PROJECT_FILE`, `UE_EDITOR_TARGET` | `.claude/settings.local.json`, under `env` |
| Personal notes for Claude | `CLAUDE.local.md`, not committed |

- **Deny rules** block `cd` and its aliases, so a session never leaves its folder. Claude Code 2.1.272 warns that
  the `Cd` rule is unknown; newer versions use it.
- **Stop Claude committing:** add `"PowerShell(git commit*)", "PowerShell(git -C * commit*)"` and the same two as
  `Bash(...)` to `permissions.deny`.
- **Rider:** each developer enables Rider's MCP server once (Settings → AI → MCP Server, then Auto-Configure for
  Claude Code), with the solution open. The `rider-skills` plugin comes from `.claude/settings.json`: accept it when
  Claude Code offers it. Its UE skills look for the `.uproject` in the folder Claude Code starts in.
- **Code intelligence without Rider:** `clangd` on `PATH` (`winget install LLVM.LLVM`) plus the C++ database. It works when a
  `Found N new diagnostic issues` line follows an edit; otherwise see `/plugin`, Errors.
- **Personal plugins** that block a built-in tool break rows naming it: make the plugin a team standard, or keep
  the rows free of tool names.

## Routine

- **Docs drift:** ask Claude to update the docs for what changed, or to check them; review the edits.
- **Check what loaded:** `/memory`, `/context`, `/doctor prompt-audit`. Never run `/init`: it breaks `CLAUDE.md`.
- **Update the template:** replace the template-owned files with the newer copies:
  `.claude/skills/agent-docs/`, `Tools/python.cmd` and `Tools/ue.py`.
- **Add** a plugin, skill or engine command with its row in 2.INSTRUCTIONS; a variable with its row in the index.
- **Other agents:** for Codex, add `.agents/skills/agent-docs/SKILL.md` with the same frontmatter and a body pointing
  to Claude's copy. For Gemini CLI, `.gemini/settings.json` with `{ "context": { "fileName": ["AGENTS.md"] } }`.
  Either needs its own permission setup and shell variables.

## Notes

Your scratchpad. Move a settled item into the doc it belongs to.
