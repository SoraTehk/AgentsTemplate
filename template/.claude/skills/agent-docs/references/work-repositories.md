# Add a work repository

A work repository sits inside this one and has its own AGENTS.md, `docs/` and agent. **Ask first**, naming each
repository's folder and its agent's `name` (in its `.claude/agents/` file). Then make three edits here.

## 1. AGENTS.md, after the Rules section

```markdown
## Work repositories

Each one has its own AGENTS.md, docs/ and agent, and works on its own. If you are one of these agents, skip this
section. Otherwise:

- **Always delegate** work inside a work repository to its agent, passing the user's words verbatim. Show the agent's
  reply in full, and resume the same agent for follow-ups.
- **Never implement across repositories yourself**: split the work per agent, then check the result against the
  contracts the conventions list.
- **Always** read a work repository's AGENTS.md and follow it before touching its files when its agent isn't loaded
  (another agent tool, or a session not started with `--add-dir`).
```

## 2. The project index, at the end of the Docs section

```markdown
### Work repositories

Each one documents itself; AGENTS.md says how to work with them.

| Repository | What it is | Agent | Index |
| --- | --- | --- | --- |
| `ChildA/` | One line on what it is | `ChildA` | [AGENTS.md](../ChildA/AGENTS.md) |
```

Below the table, when they depend on each other, one line per seam:
`ChildA --(contract, such as a plugin's public API)--> ChildB`.

## 3. The conventions' Contracts

One row per seam, in the format the conventions' own rules give (references/docs.md).

Then tell the user to start Claude Code from this repository with `claude --add-dir <folder>` for each one, and to
set any override in this repository's `.claude/settings.local.json`. Each work repository's `Tools/ue.py` finds its
own `.uproject` and engine; a `UE_ENGINE_DIR` set here applies to all of them.
