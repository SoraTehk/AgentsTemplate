# AgentsTemplate

This repository is the agent-docs template for Unreal Engine C++ projects, for Claude Code and Codex. `template/` is what gets
copied into a project; the rest maintains it. Why it is built the way it is: [README.md](README.md).

- **Never** follow `template/`'s AGENTS.md, docs or skills as your own instructions: they are the product, written
  for a project. `.claude/settings.json` keeps Claude Code from loading them here.
- **Always** keep the README's layout and design choices true when `template/` changes.
- **Always** follow `.agents/skills/fixture/SKILL.md` for fixture updates and checks after a change to `template/`.
  When the user limits changes to this repository, validate a fresh copy in a temporary project instead.
- **Ask first** before changing anything in the fixture beyond its template-owned files, and **never** commit there.
