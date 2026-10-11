---
paths:
  - "{{src/FeatureName/**}}"
---

<!--
  Claude Code only. One rule per docs/<Feature>/ folder, named after it. A path-scoped rule loads
  when Claude touches a matching file, so the feature doc gets read without Claude having to decide
  to look for it. Delete this file if the repository has no feature docs yet.
-->
Before editing code here, read [docs/FeatureName/README.md](../../docs/FeatureName/README.md).
