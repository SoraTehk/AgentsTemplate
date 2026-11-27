# Check the agent docs

Read AGENTS.md and every `docs/` file except `_HUMANS.md`. Where present, also check CLAUDE.md,
`.claude/rules/`, `.claude/agents/`, the local Claude skill junction and `.claude/settings.json`. Report each finding as
`path:line: what's wrong, and the fix you propose`, most serious first. Change nothing until the user approves; lines
for the instructions follow the gate.

## Mechanical

Compare the line counts with each doc's budget and flag files with a byte-order mark. Run the block together
in PowerShell from the project root.

```powershell
$docPaths = 'AGENTS.md', 'CLAUDE.md', 'docs', '.claude/rules', '.claude/agents'
foreach ($path in $docPaths) {
    if (!(Test-Path -LiteralPath $path)) { continue }
    $files = Get-ChildItem -LiteralPath $path -File -Recurse
    foreach ($file in $files) {
        if ($file.Extension -ne '.md' -or $file.Name -eq '_HUMANS.md') { continue }
        $bytes = [IO.File]::ReadAllBytes($file.FullName)
        [PSCustomObject]@{
            Path = Resolve-Path -Relative $file.FullName
            Lines = @(Get-Content -LiteralPath $file.FullName).Count
            Utf8Bom = $bytes.Length -ge 3 -and $bytes[0] -eq 239 -and $bytes[1] -eq 187 -and $bytes[2] -eq 191
        }
    }
}
```

- Check installed agent docs and their filenames for unfilled `{{...}}` placeholders. The shared skill's
  reusable assets and examples retain their placeholders. Check agent docs other than CLAUDE.md for `<!--`.
- Frontmatter: valid YAML whose `---` is the file's first line; every agent's `name` unique across the workspace.
- Every link, anchor and Claude `@path` import resolves. AGENTS.md lists both startup docs as ordinary paths.
  When CLAUDE.md is present, its imports load AGENTS.md and those same two docs. The Claude agent-docs
  junction, if present, targets the shared skill directory in this checkout.

## Structure

- Each Docs table lists exactly the numbered docs in its folder, and the Features table exactly the `docs/<Feature>/`
  folders.
- Each feature has its `1_<FEATURE>.md`. Its code and test folders appear in the project index's Features table.
  If a `.claude/rules/<Feature>.md` exists, its `paths` match those folders.
- Cross-references belong in indexes, apart from the startup paths and tool-specific pointers checked above.
  Feature paths in the project index, feature index and any Claude path rule agree.
- Every rule starts with Always, Ask first or Never, sits in the doc for its kind, and none contradicts another.
- `.claude/settings.json` has no `permissions.allow` list: approvals are each developer's own.

## Truth

- Every path a doc names exists, and every `$env:<NAME>` it uses is in the project index's Variables.
- Each command's programs and flags exist in the versions the Prerequisites name; `Tools/ue.py` has each subcommand
  the instructions call.
- Each Vocabulary term is the name the code uses, and the code uses no synonym for it.
- Done milestones and TODOs are gone; each decision still holds; nothing restates an agent's built-in defaults.

In Claude Code, `/doctor prompt-audit` can give a second opinion on contradictions and dead references.
