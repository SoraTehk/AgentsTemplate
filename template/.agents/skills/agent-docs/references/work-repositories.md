# Add a work repository

A work repository sits inside this one and has its own AGENTS.md and project docs. **Ask first** to register
each repository by folder. If it exposes a named agent for delegation, verify its name before adding it.

## 1. AGENTS.md, after the Rules section

```markdown
## Work repositories

- **Always** divide cross-repository changes by owning repository and check each side against the documented contract.
- **Always** follow each work repository's AGENTS.md, project index and instructions when working there.
  When its named agent is available for delegation and the session permits it, pass that agent the user's request
  verbatim, return its reply in full and resume it for follow-ups. Otherwise read the child's instructions directly
  and use its root as the working directory for its commands.
```

## 2. The project index, at the end of the Docs section

```markdown
### Work repositories

Each one documents itself; AGENTS.md says how to work with them.

| Repository | What it is | Agent (if available) | Index |
| --- | --- | --- | --- |
| `ChildA/` | One line on what it is | `ChildA` | [AGENTS.md](../ChildA/AGENTS.md) |
```

Below the table, when they depend on each other, one line per seam:
`ChildA --(contract, such as a plugin's public API)--> ChildB`.

## 3. The conventions' Contracts

One row per seam, in the format the conventions' own rules give (references/docs.md).

Each work repository's `Tools/ue.py` finds its own project and engine. A `UE_ENGINE_DIR` override inherited
from the parent process applies to all children. In Claude Code, start the parent with `claude --add-dir <folder>`
for each child to make its agent available.
