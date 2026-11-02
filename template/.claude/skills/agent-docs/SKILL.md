---
name: agent-docs
description: Edit, create or check this repository's agent docs (AGENTS.md, CLAUDE.md, docs/, .claude/rules/, .claude/agents/). Use before changing any of them, for any fact, rule, command, decision or TODO; to start a feature or one of its docs; to add a work repository; or when asked to check or audit the docs.
---

# Agent docs

The agent docs tell every coding agent how to work here. This skill is how to change them without making them worse.
It holds no facts about this project, so a newer template's copy can replace it whole.

## Pick the job

| Job | Do |
| --- | --- |
| Change a doc: a fact, rule, command, decision or TODO | The shared rules below, then that doc's own rules in [references/docs.md](references/docs.md). A root doc that doesn't exist yet, such as 6.TODOS: copy it from `assets/root/` and add its row to the project index's Docs table |
| Start a feature, or another numbered doc for one | [Start a feature](#start-a-feature) |
| Add a work repository to this one | [references/work-repositories.md](references/work-repositories.md) |
| Check the docs, or review after a large change | [references/check.md](references/check.md) |

## Shared rules

For every agent doc, a feature's included:

- **Always describe the present.** Edit what changed and delete what no longer holds; version control keeps the past.
- **Always give a fact one home**: the doc whose "Holds" column in the project index names it. **Never** name or link
  another doc except from an index (the project index, `docs/1.<PROJECT>.md`, for the root docs; a feature's
  `1.<FEATURE>.md` for its own); refer to content by what it is ("the conventions", "the test framework", "the
  project index") and point back to the index for anything else.
- **Always make the smallest true edit.** Write only facts you checked. **Never** write what the code, the compiler, a
  linter or the agent's built-in defaults already say.
- **Always start a rule with Always, Ask first or Never**, as AGENTS.md defines them, and give its why when it isn't
  obvious; a Never says what to do instead. **Never** phrase a rule another way ("must", "don't", "before doing",
  "only if", "unless the user asks"): something to do only on request is Ask first.
- **Always put a rule in the doc for its kind**: how to do something in the instructions, what code looks like in the
  conventions, how tests are written in the test doc. Only rules every turn needs go in AGENTS.md.
- **Always stay within the doc's budget.** Past it, cut, or move detail down into a feature's docs; **never** just grow
  the file. AGENTS.md, the project index and the instructions load every session: keep them well under theirs.
- **Never write an HTML comment in an agent doc** other than CLAUDE.md. Claude Code strips them from the files it
  loads at start, but not from a doc it opens with a file tool, and one holding a code fence leaks into context.
  Fill-in hints and optional sections live in this skill instead.
- **Always write UTF-8 without a byte-order mark**: one hides a file's frontmatter from Claude Code.
- **Always follow the gate for the instructions**: add a line there only when the user wrote it, or approved it and
  you add it word for word.
- **Ask first** before deleting or moving content you didn't write in this task.
- **Never** keep an empty doc: create one when it first has content, and delete it, and its Docs table row, when it
  has none left.

## Start a feature

1. Copy `assets/feature/1.{{FEATURE_NAME_CAPS}}.md` to `docs/<Feature>/1.<FEATURE>.md` and `assets/feature/rule.md` to
   `.claude/rules/<Feature>.md`, replacing `{{FEATURE_NAME}}` with the feature's name, `{{FEATURE_NAME_CAPS}}` with
   that name in ALL_CAPS (`BuildingSystem` → `BUILDING_SYSTEM`), `{{PROJECT_NAME}}` with the project's, and
   `{{MODULE_NAME}}` with the module the feature's code lives in (the project index's Layout names the game module).
2. Add the feature's row to the project index's Features table. Point the index's **Code** and **Tests**, and the rule's
   `paths`, at the feature's folders.
3. Fill in what you know; leave the rest as the asset has it.

**Another numbered doc:** only once the feature has something of its own for it that the root doc with that number
doesn't hold. Copy it from `assets/feature/` the same way, and add its row to the feature's Docs table.

**Never** nest features. Split one that outgrows its folder into sibling features, or make it a work repository when
it needs its own build or release.
