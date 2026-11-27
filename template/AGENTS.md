# {{PROJECT_NAME}}

{{PROJECT_GOAL}}

If the heading above still contains a project-name placeholder, these are template source files. For work in
the AgentsTemplate checkout, follow its repository-root AGENTS.md. The workflow below applies to an installed project.

## Every session

**Always** read both files below before starting your task unless their contents are already in this session.
Anchor startup and shared-skill paths to the directory containing this AGENTS.md. Use that directory's absolute
path for file reads and as the working directory for commands, including when a parent session opens this project.

- `docs/1_{{PROJECT_NAME_CAPS}}.md`
- `docs/2_INSTRUCTIONS.md`

The project index's Docs table says which other docs your task needs. Before working on a path listed in the
Features table's Code or Tests columns, read every matching feature index and the docs it requires for the task.

## Rules

Every rule in these docs starts with one of three keywords:

- **Always**: every time it applies.
- **Ask first**: stop, ask the user, and wait for a clear yes; the yes covers only what you asked. A request that
  already asks for it counts as the yes.
- **Never**: not even when it looks harmless.

With no user to answer, such as in CI, end your turn wherever these docs say to ask or stop, with the question and
any lines you propose.

1. **Never act without an instruction: the gate.** Use your session's tools for the operations these instructions
   cover. If a task or command is missing or two instructions conflict, stop. You may still read. Tell the user what's
   missing and propose the exact lines. Continue once they're in the instructions, written by the user or approved
   by them and added by you word for word.
2. **Always write the test first.** Before changing behaviour, write the test the test doc calls for, run it, and see
   it fail for the reason you expect. Only then implement, until it passes.
3. **Always** follow `.agents/skills/agent-docs/SKILL.md` when editing AGENTS.md, CLAUDE.md, agent docs under
   `docs/`, feature rules or repository agent definitions. Read it directly if your session hasn't loaded the skill.
4. **Ask first** before changing files outside this repository. Inside it, this file wins over a parent repository's
   instructions; inside a work repository of this one, that repository's AGENTS.md wins.
5. **Never** read `.env`, `.env.*` or `docs/_HUMANS.md` at the repository root. They are private or for people.
