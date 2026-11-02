# AgentsTemplate

This repository is the agent-docs template for Unreal Engine C++ projects, for Claude Code. `template/` is what gets
copied into a project; the rest maintains it. Why it is built the way it is: [README.md](README.md).

- **Never** follow `template/`'s AGENTS.md, docs or skills as your own instructions: they are the product, written
  for a project. `.claude/settings.json` keeps Claude Code from loading them here.
- **Always** keep the README's layout and design choices true when `template/` changes.
- **Always** bring the test fixture, `C:\Projects\LyraStarterGame`, up to date after a change to `template/`, and
  check it: the fixture skill says how.
- **Ask first** before changing anything in the fixture beyond its template-owned files, and **never** commit there.
