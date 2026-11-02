# Each doc's own rules

They add to the shared rules in SKILL.md. A feature's doc follows the root doc's rules below, plus its own line.

## AGENTS.md and CLAUDE.md

- **Always** keep AGENTS.md to rules every turn needs. Budget: ~45 lines, not counting what it imports.
- **Never** import (`@path`) anything but the docs every session needs: the project index and the instructions.
  Claude Code loads an import's full text every session. **Always** put each import on its own line, under a sentence
  telling an agent that opened the file with a tool to read them.
- **Never** add to CLAUDE.md anything but `@AGENTS.md` and lines for Claude-only behaviour.

## .claude/agents/

- This repository's agent, used when a parent repository opens it with `--add-dir`. **Always** keep its `name`
  unique across every repository in the workspace, without ":", and its frontmatter valid YAML: Claude Code silently
  skips a file that breaks either.
- This repository's permissions and hooks don't apply inside a parent session. **Always** add `permissionMode`,
  `disallowedTools` or `hooks` frontmatter for any that must hold there too.

## The project index, 1.\<PROJECT>.md, and a feature's 1.\<FEATURE>.md

- **Always** name an index after its project or feature in ALL_CAPS, words split by underscores, as the numbered docs
  are: `LyraStarterGame` → `1.LYRA_STARTER_GAME.md`, `BuildingSystem` → `1.BUILDING_SYSTEM.md`. Its folder and its
  heading keep the name as it is (`docs/BuildingSystem/`, `# 1. BuildingSystem`).
- **Always** change only the Docs table when a doc is added, removed or renamed; no other doc names it. The project
  index's row for 6.TODOS, once it exists:
  `| [6.TODOS](6.TODOS.md) | Work deferred across sessions (not your in-session task list) | Before refactoring, or when you defer something |`
- What and why: grow it into two to four sentences: the problem, who has it, and what this project does about it.
- Features table, one row per `docs/<Feature>/` folder:

  ```markdown
  | Feature | Index | Code |
  | --- | --- | --- |
  | Inventory | [1.INVENTORY](Inventory/1.INVENTORY.md) | `Source/<Module>/Inventory/` |
  ```

- Milestones: status is one of done, in progress, next, parked. Newest at the bottom; delete done rows once nobody
  needs them. **Now** says what the current one has been checked by, and what not yet.
- Prerequisites: the exact version, and in "Why", what needs it and the error you see without it. Where a tool is on
  a machine is a variable, not part of the table.
- Variables: name, meaning and an example only; each machine's values are its own.
- SESSION_FILES base: what the files are compared against, such as "commit 1a2b3c4, where branch feature/Inventory
  started". Update it when the next piece of work starts, and after any rebase or history rewrite: a base no longer
  in the history lists the wrong files.
- Layout: only folders whose purpose isn't obvious from the name.
- Budget: ~150 lines.

**A feature's index** also:

- **Always** keeps **Code** and **Tests** listing every folder the feature owns; the rule's `paths` match them. A
  feature in a plugin lives in `Plugins/<Plugin>/Source/<Module>/`.
- Docs table, replacing "None yet", one row per numbered doc in its folder, in number order:

  ```markdown
  | Doc | Holds | Read when |
  | --- | --- | --- |
  | [2.INSTRUCTIONS](2.INSTRUCTIONS.md) | Its own tasks, commands and procedures | Before your first action in it |
  | [3.CONVENTIONS](3.CONVENTIONS.md) | Its vocabulary, and rules for its code only | Before writing or reviewing its code |
  | [4.TEST](4.TEST.md) | Its own test framework rows | Before changing its behaviour |
  | [5.DECISIONS](5.DECISIONS.md) | Why it works the way it does | Before reversing a choice in it |
  | [6.TODOS](6.TODOS.md) | Its deferred work and known gaps | Before refactoring it, or when you defer something in it |
  ```

- Status: planned, in progress, done or parked.
- Contract: what other code and other features may rely on: public types, interfaces, delegates, gameplay tags, data
  formats. Another feature relies on nothing else.
- How it works: what it is now: what runs where (server, owning client), in what order. Name the class a reader
  should open first.
- Layout: every folder it owns, code and content, and what each holds.

## 2.INSTRUCTIONS

- **Always** write one row per thing an agent does. A "how" that doesn't fit its cell goes in a section below the
  table, linked from its row.
- **Always** write a command as one PowerShell line, in a code span in its row's "How" cell, that runs as written
  from the repository's root, with `<name>` for one argument that changes.
- **Never** change directory in a command, or write a machine path into it: our scripts read the variables the
  project index defines.
- **Always** run an engine program or a script of ours through `Tools/python.cmd`, with forward slashes: a new engine
  command becomes a `Tools/ue.py` subcommand, anything else a `Tools/<script>.py`. **Never** start a command with a
  program named by a variable (`& "$env:UE_ENGINE_DIR\..."`): Claude Code can't save an approval for one.
  Extra Unreal Build Tool flags go after `build` or `clang-db`, written out in the row: `Tools/python.cmd Tools/ue.py
  build -NoUBA`.
- **Always** make "Done when" say what success prints; our scripts end with `exit <code>`.
- In `Tools/ue.py`: **never** wait on a pipe, or with `Start-Process -Wait`, for a program that leaves processes
  behind, such as the editor's MSBuild nodes; that hangs for minutes after it exits. Send its output to a log, wait
  for that process alone, and print what matters from the log.
- Known noise: each entry names the decision that says why, and the command that prints it filters it out.
- Version control and SESSION_FILES rows ship with both git and Perforce. At setup, keep only the system in use.
- Budget: ~200 lines. A feature's: ~100, holding what that feature alone needs; a task or command two features share
  goes in the root's.

## 3.CONVENTIONS

- **Always** keep rules repository-wide: a rule about one feature goes in that feature's conventions, one every
  feature follows comes up here.
- **Never** restate the coding standard, or what a formatter, linter or compiler warning enforces: name the tool.
- **Always** list every term of the project's own in the Vocabulary:

  ```markdown
  | Term | In the code | Meaning |
  | --- | --- | --- |
  | Item | an actor with a `UInventoryItemComponent` | Something the player can pick up and carry |
  ```

- Scope, in a codebase older than these rules: "**Scope:** SESSION_FILES, plus \<folders already written to these
  rules>. Any other file adopts them when it is next changed. **Exception:** \<legacy files a change barely touches>
  keep their own style, and the change matches them."
- Architecture, once there are modules of our own: list them with arrows meaning "may depend on", such as
  `<Project> → InventoryPlugin → Engine`.
- Contracts, one row per seam with a parent, child or sibling repository. The owner is the side whose change forces
  the other to follow:

  ```markdown
  | Contract | Producer → consumer | Owner | Spec |
  | --- | --- | --- | --- |
  | Inventory plugin API | `InventoryRepo` → `<Project>` | `InventoryRepo` | That repository's feature doc |
  ```

- Budget: ~200 lines. A feature's: ~100, only rules about that feature.

## 4.TEST

- **Always** keep it to what an agent needs to write a test here; how to run tests is in the instructions.
- A row for tests that need a ticking world:
  `| Needs a world | Functional test: an AFunctionalTest in a test map | Content/Tests/<Feature>/ | FTEST_<Subject> |`
- No automated tests yet, on purpose: record it as a decision (how every change is still tested meanwhile, and when
  to revisit), and say so here.
- Budget: ~60 lines. A feature's: ~40, only framework rows that differ from the root's.

## 5.DECISIONS

- **Always** say what holds now. A decision that changes is edited in place, adding "revised YYYY-MM-DD" to its
  heading. **Never** add an entry that supersedes another.
- **Always** merge entries that decide the same thing, and delete one that no longer holds. **Never** reuse a number:
  a merged or deleted decision leaves a gap.
- **Never** record a choice that had no real alternative. **Always** say what was rejected and why. Under ~10 lines
  each.
- Format: `## D-00N: <the decision, as a statement> (YYYY-MM-DD[, revised YYYY-MM-DD])`, then Context, Decision,
  Rejected, Revisit when.
- A feature's are numbered on their own and cited as "\<Feature> D-00N". Budget: ~100 lines.

## 6.TODOS

- **Never** list work an agent needn't know about while editing: this is not a backlog, and features and bugs belong
  in the issue tracker. An item is here so nobody "fixes" it halfway by accident.
- **Always** say why an item waits. Delete it when it's done; if finishing it settled a question, record a decision.
- Format: ``- **Area**: what. Why it waits. `where/` (YYYY-MM-DD)``, under its section: Rename, Restructure,
  Debt or Docs.
- Budget: ~80 lines, a feature's too.
