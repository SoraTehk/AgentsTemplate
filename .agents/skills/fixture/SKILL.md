---
name: fixture
description: Check, update, convert or smoke-test the test fixture, C:\Projects\LyraStarterGame, the real project that runs the current template. Use after any change to template/, or when asked about the fixture.
---

# The test fixture

`C:\Projects\LyraStarterGame` is Epic's Lyra sample (remote `SoraTehk/LyraStarterGame`), at that path on every
machine. It is where the template meets a real project. Its project name is `LyraStarterGame`, its game module
`LyraGame`, its editor target `LyraEditor`. Its content is in Git LFS, and it often has uncommitted work of its own:
get explicit approval before touching project-owned files. **Never** commit there.

## Template-owned files

Copied unchanged into every project and replaced whole on update; they hold no project facts:

- `.agents/skills/agent-docs/` and `Tools/Link-AgentSkills.ps1`
- `Tools/python.cmd`, `Tools/ue.py`

Everything else belongs to the project once it is set up.

## Check

1. Each template-owned path matches the template; this prints nothing when it does:
   `git diff --no-index --stat -- template/<path> C:/Projects/LyraStarterGame/<path>`
2. The fixture's `.claude/settings.json` has the template's deny rules and plugins, and no `hooks` entry or
   `Tools/approve_instructed.py` left from an older template.
3. Check that AGENTS.md names both startup docs, `docs/1_LYRA_STARTER_GAME.md` and `docs/2_INSTRUCTIONS.md`,
   and the shared skill. Verify the paths exist, Claude's entry point imports the shared guidance and its settings
   contain no `permissions.allow` list.
4. Report differences. Check is read-only.

## Update

1. Inspect `git -C C:/Projects/LyraStarterGame status --short -- .agents .claude Tools` and compare the installed
   files with the template. Ask before replacing any fixture edits, including edits to an older skill at the old path.
2. Copy changed template-owned files to the same paths in the fixture. During migration, reconcile local edits
   before enabling a checkout-local skill junction. Leave unrelated files in place.
3. List required changes to project-owned files (including settings and project docs) and ask before applying them.
4. Run Check.

## Convert

Done on 2026-11-02, not committed in the fixture. Each of Lyra's topic docs became a feature: Audio,
BlueprintIntegration, Collision, EventBus, GasLayers, GasTargeting, Interaction, Profiling and UI, each section moved
whole, by kind, into the feature's index or numbered docs, with its `§` references relinked. RENAMER became Renamer
on the current structure; TowerDefense got an index around its design diagram. Its root docs have no 6_TODOS and
no `.claude/agents/`: Lyra is never a work repository. Still open: the migrated docs are over their budgets, and
their rules are not yet in Always / Ask first / Never form; run the agent-docs check there to list them.

## Smoke test

Start a fresh session in the fixture root for each agent being checked. Give each the same read-only task:

> Identify the editor target from source and cite its path and line. Find one named automation test and show
> its exact command without running it. List both startup documents and the editing skill path you used.

Compare each answer against the fixture source, its instructions and the shared skill. Use the same named test
when comparing commands across agents. **Ask first** before running a Lyra build.
