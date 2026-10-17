---
paths:
  - "src/{{FEATURE_NAME}}/**"
---

<!--
  Claude Code only. 2.INSTRUCTIONS "Add or change a feature" copies it to .claude/rules/<Feature>.md. It is to the
  feature what CLAUDE.md is to the repository: the entry point that makes Claude read the index. A path-scoped rule
  loads when Claude touches a matching file, so the feature's docs get read without Claude having to look for them.
  Give `paths` one entry per folder the README's **Code** and **Tests** list.
-->
Before editing code here, read `docs/{{FEATURE_NAME}}/README.md`, then each doc its "Docs" table says to read for
your task.
