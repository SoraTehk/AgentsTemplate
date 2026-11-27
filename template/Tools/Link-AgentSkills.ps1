param(
    [Parameter(Mandatory, Position = 0)]
    [ValidatePattern('^[a-z0-9][a-z0-9-]*$')]
    [string] $Skill,
    [string] $ProjectRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'
$root = (Get-Item -LiteralPath $ProjectRoot).FullName
$source = [IO.Path]::GetFullPath((Join-Path $root ".agents/skills/$Skill"))
if (!(Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) {
    throw "Missing shared skill in $source"
}

$parent = $root
foreach ($folder in '.claude', 'skills') {
    $parent = Join-Path $parent $folder
    $directory = [IO.Directory]::CreateDirectory($parent)
    if ($directory.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        throw "Expected a local directory at $parent"
    }
}

$aliasPath = Join-Path $parent $Skill
$existing = Get-ChildItem -LiteralPath $parent -Force | Where-Object Name -eq $Skill
if ($existing) {
    if ($existing.LinkType -eq 'Junction' -and $existing.Target -eq $source) {
        Write-Output "Already linked: $aliasPath"
        return
    }
    throw "Preserve or move the existing entry at $aliasPath before linking."
}
New-Item -ItemType Junction -Path $aliasPath -Target ([WildcardPattern]::Escape($source)) | Out-Null
Write-Output "Linked $aliasPath to $source"
