<!--
  AGENTS.md is the INDEX and the ENFORCEMENT layer: every line loads on every turn, for every agent.
  Budget: ~60 lines. Detail belongs in docs/. Replace {{PROJECT_NAME}} and {{PROJECT_GOAL}}; everything
  else has a working default. Never write an "@" followed by a path here: Claude Code would import that
  file into every turn.
-->
# {{PROJECT_NAME}}

{{PROJECT_GOAL}}

## Always

1. **Follow the instructions.** Before your first action, read [2.INSTRUCTIONS](docs/2.INSTRUCTIONS.md). Do
   everything the way it says: its commands, its tool for each action, and the playbook for your task.
2. **No instruction, no action.** If your task matches no playbook, or needs a command or tool that
   2.INSTRUCTIONS doesn't cover, or two instructions conflict: stop. Until it is resolved you may only
   read. Tell the user what is missing and propose the exact lines to add. Continue only once they are in
   2.INSTRUCTIONS, written by the user or approved by them and added by you word for word.
3. **Tests first.** Before changing behaviour, write the test [4.TEST](docs/4.TEST.md) calls for, run it,
   and see it fail for the reason you expect. Only then implement, until it passes. If 4.TEST exempts the
   change, say which exemption applies.

## Docs

Your training data is older than this code. Read the matching doc instead of relying on memory.

| Doc | Holds | Read when |
| --- | --- | --- |
| [1.PROJECT](docs/1.PROJECT.md) | Purpose, milestones, prerequisites, layout | Starting a session, or asked about scope or status |
| [2.INSTRUCTIONS](docs/2.INSTRUCTIONS.md) | Shell commands, the tool for each action, a playbook per task | Before your first action, every session |
| [3.CONVENTIONS](docs/3.CONVENTIONS.md) | Style, naming, architecture, patterns, contracts, git format | Before writing or reviewing code |
| [4.TEST](docs/4.TEST.md) | Test frameworks, layout, what each change must ship with | Before writing any code |
| [5.DECISIONS](docs/5.DECISIONS.md) | Why things are the way they are | Before reversing a choice or changing architecture |
| [6.TODOS](docs/6.TODOS.md) | Work deferred across sessions (not your in-session task list) | Before refactoring, or when you defer something |

### Feature docs

None yet.
<!-- Replace "None yet." with a table, one row per docs/<Feature>/ folder (see docs/_FEATURE_TEMPLATE/):
| Feature | Doc | Code |
| --- | --- | --- |
| Ocr | [README](docs/Ocr/README.md) | `src/Ocr/` |
-->

<!-- Uncomment when this repository contains other repositories (git submodules or nested clones).
## Work repositories

Each one has its own AGENTS.md, docs/ and agent, and works on its own. If you are one of these agents,
skip this section. Otherwise:

- **Delegate.** Hand any work inside a work repository to its agent, passing the user's words verbatim.
  Show the agent's reply in full, and resume the same agent for follow-ups.
- **Coordinate, don't implement.** Across repositories, split the work per agent, then check the result
  against the contracts in [3.CONVENTIONS](docs/3.CONVENTIONS.md#contracts-with-other-repositories).
- **No agent loaded?** Without one (another agent tool, or a session not started with `--add-dir`), read
  that repository's AGENTS.md and follow it before touching its files.

| Repository | What it is | Kind | Agent | Index |
| --- | --- | --- | --- | --- |
| `ChildA/` | One line on what it is | git submodule | `ChildA` | [AGENTS.md](ChildA/AGENTS.md) |
-->

## Scope

This repository stands alone: this file and `docs/` are enough to work here, even when it is cloned by
itself. A parent repository's instructions cover only how its work repositories fit together; inside this
repository, this file wins. In the same way, inside a work repository of this one, its own AGENTS.md
wins. Stay inside this repository unless the task says otherwise.
