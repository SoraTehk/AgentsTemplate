---
name: fixture
description: Check, update, convert or smoke-test the test fixture, C:\Projects\LyraStarterGame, the real project that runs the current template. Use after any change to template/, or when asked about the fixture.
---

# The test fixture

`C:\Projects\LyraStarterGame` is Epic's Lyra sample (remote `SoraTehk/LyraStarterGame`), at that path on every
machine. It is where the template meets a real project. Its project name is `LyraStarterGame`, its game module
`LyraGame`, its editor target `LyraEditor`. Its content is in Git LFS, and it often has uncommitted work of its own:
**never** touch files outside the template-owned list, and **never** commit there.

## Template-owned files

Copied unchanged into every project and replaced whole on update; they hold no project facts:

- `.claude/skills/agent-docs/`
- `Tools/python.cmd`, `Tools/ue.py`

Everything else belongs to the project once it is set up.

## Check

1. Each template-owned path matches the template; this prints nothing when it does:
   `git diff --no-index --stat -- template/<path> C:/Projects/LyraStarterGame/<path>`
2. The fixture's `.claude/settings.json` has the template's deny rules and plugins, and no `hooks` entry or
   `Tools/approve_instructed.py` left from an older template.
3. The fixture has AGENTS.md importing `docs/1.LYRA_STARTER_GAME.md` and `docs/2.INSTRUCTIONS.md`, a CLAUDE.md
   importing AGENTS.md, and no `permissions.allow` list.
4. Report what differs. Change nothing.

## Update

1. `git -C C:/Projects/LyraStarterGame status --short -- .claude Tools`: anything listed under a template-owned path
   is the fixture's own edit, so **ask first** before replacing it.
2. Copy the template-owned files:
   `robocopy template\.claude\skills\agent-docs C:\Projects\LyraStarterGame\.claude\skills\agent-docs /MIR /NFL /NDL /NJH /NJS`
   (exit codes below 8 are success), then copy the three `Tools/` files and set the `hooks` entry in the fixture's
   settings to the template's.
3. When the change also alters what project-owned files must hold (a rule in AGENTS.md, a row in the instructions, a
   doc's structure), list the edits the fixture's docs need and **ask first**.
4. Run Check.

## Convert

Done on 2026-11-02, not committed in the fixture. Each of Lyra's topic docs became a feature: Audio,
BlueprintIntegration, Collision, EventBus, GasLayers, GasTargeting, Interaction, Profiling and UI, each section moved
whole, by kind, into the feature's index or numbered docs, with its `§` references relinked. RENAMER became Renamer
on the current structure; TowerDefense got an index around its design diagram. Its root docs have no 6.TODOS and
no `.claude/agents/`: Lyra is never a work repository. Still open: the migrated docs are over their budgets, and
their rules are not yet in Always / Ask first / Never form; run the agent-docs check there to list them.

## Smoke test

After Update, from this repository, so the fixture's own settings and variables apply:
`env -C C:/Projects/LyraStarterGame claude -p "Without tools: list the '## ' headings you can see from docs/1.LYRA_STARTER_GAME.md and docs/2.INSTRUCTIONS.md, and say whether the agent-docs skill is available."`
in Bash. It passes when both docs' headings are listed and the skill is available. **Ask first** before running
`Tools/python.cmd Tools/ue.py build` there: a Lyra build takes many minutes.
