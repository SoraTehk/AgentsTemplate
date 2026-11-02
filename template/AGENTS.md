# {{PROJECT_NAME}}

{{PROJECT_GOAL}}

## Every session

These two docs load with this file. If they didn't, because you opened it with a file tool, **always** read them
before your first action:

@docs/1.{{PROJECT_NAME_CAPS}}.md
@docs/2.INSTRUCTIONS.md

The project index's Docs table says which other docs your task needs: read them, and do everything the way they say.
Working in a feature's code, read its index first; the Features table lists it. Your training data is older than
this code: trust the docs.

## Rules

Every rule in these docs starts with one of three keywords:

- **Always**: every time it applies.
- **Ask first**: stop, ask the user, and wait for a clear yes; the yes covers only what you asked. A request that
  already asks for it counts as the yes.
- **Never**: not even when it looks harmless.

With no user to answer, such as in CI, end your turn wherever these docs say to ask or stop, with the question and
any lines you propose.

1. **Never act without an instruction: the gate.** If your task, or a command or tool it needs, isn't covered by the
   instructions, or two instructions conflict, stop: until it's resolved you may only read. Tell the user what's
   missing and propose the exact lines. Continue once they're in the instructions, written by the user or approved
   by them and added by you word for word.
2. **Always write the test first.** Before changing behaviour, write the test the test doc calls for, run it, and see
   it fail for the reason you expect. Only then implement, until it passes.
3. **Always change the agent docs through the agent-docs skill** (`.claude/skills/agent-docs/`): AGENTS.md,
   CLAUDE.md, `docs/`, `.claude/rules/` and `.claude/agents/`.
4. **Ask first** before changing files outside this repository. Inside it, this file wins over a parent repository's
   instructions; inside a work repository of this one, that repository's AGENTS.md wins.
