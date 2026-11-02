# Check the agent docs

Read every agent doc first: AGENTS.md, CLAUDE.md, every `docs/` file except `_HUMANS.md`, `.claude/rules/`,
`.claude/agents/` and `.claude/settings.json`. Then go through the three lists below. Report each finding as
`path:line: what's wrong, and the fix you propose`, most serious first. Change nothing until the user approves; lines
for the instructions follow the gate.

## Mechanical

- Line counts against each doc's budget:
  `Get-ChildItem AGENTS.md, CLAUDE.md, docs, .claude -Recurse -Include *.md -File | ForEach-Object { '{0,5} {1}' -f (Get-Content -LiteralPath $_.FullName).Count, (Resolve-Path -Relative $_.FullName) }`
- A file starting with a byte-order mark:
  `Get-ChildItem AGENTS.md, CLAUDE.md, docs, .claude -Recurse -Include *.md -File | Where-Object { $b = [IO.File]::ReadAllBytes($_.FullName); $b.Length -ge 3 -and $b[0] -eq 0xEF -and $b[1] -eq 0xBB -and $b[2] -eq 0xBF } | ForEach-Object FullName`
- With your file tools: `{{` in any file or file name outside this skill's folder; `<!--` in any agent doc but
  CLAUDE.md.
- Frontmatter: valid YAML whose `---` is the file's first line; every agent's `name` unique across the workspace.
- Every link, anchor and `@path` import resolves.

## Structure

- Each Docs table lists exactly the numbered docs in its folder, and the Features table exactly the `docs/<Feature>/`
  folders.
- Each feature has its `1.<FEATURE>.md` and a `.claude/rules/<Feature>.md` whose `paths` match its Code and Tests.
- No doc but an index names another doc. No fact lives in two docs; a feature's doc doesn't repeat the root's.
- Every rule starts with Always, Ask first or Never, sits in the doc for its kind, and none contradicts another.
- `.claude/settings.json` has no `permissions.allow` list: approvals are each developer's own.

## Truth

- Every path a doc names exists, and every `$env:<NAME>` it uses is in the project index's Variables.
- Each command's programs and flags exist in the versions the Prerequisites name; `Tools/ue.py` has each subcommand
  the instructions call.
- Each Vocabulary term is the name the code uses, and the code uses no synonym for it.
- Done milestones and TODOs are gone; each decision still holds; nothing restates an agent's built-in defaults.

`/doctor prompt-audit` gives a second opinion on contradictions and dead references.
