<#.SYNOPSIS
  Push main to GitHub using GITHUB_TOKEN (classic PAT with repo scope).
  Use when cached HTTPS credentials are for a different user than the repo owner.
#>
param(
    [string]$RemoteOwner = 'amaanc986',
    [string]$RepoName = 'ECOMMERCE-PROJECT-',
    [string]$Branch = 'main'
)

$ErrorActionPreference = 'Stop'
$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Error 'Set environment variable GITHUB_TOKEN to a GitHub personal access token that can push to this repository.'
    exit 1
}

$pushUrl = "https://x-access-token:$token@github.com/$RemoteOwner/$RepoName.git"
try {
    git push $pushUrl $Branch
}
finally {
    $pushUrl = $null
    Remove-Variable pushUrl -ErrorAction SilentlyContinue
}
