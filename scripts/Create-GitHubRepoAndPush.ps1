<#
.SYNOPSIS
  Create a new GitHub repository and push this project (one-time setup).

.DESCRIPTION
  Requires GitHub CLI: https://cli.github.com/  (installed via winget as GitHub.cli)

  Option A – interactive (browser):
    1. Run:  gh auth login
    2. Run:  .\scripts\Create-GitHubRepoAndPush.ps1 -RepoName "django-hmart-store"

  Option B – personal access token (no browser):
    1. Create a classic PAT with "repo" scope: https://github.com/settings/tokens
    2. Run:
       $env:GITHUB_TOKEN = "ghp_xxxxxxxx"
       .\scripts\Create-GitHubRepoAndPush.ps1 -RepoName "django-hmart-store"

  After push: connect the repo in Render (https://dashboard.render.com) and deploy.
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $RepoName,

    [string] $GhPath = "${env:ProgramFiles}\GitHub CLI\gh.exe"
)

$ErrorActionPreference = "Stop"
if (-not (Test-Path $GhPath)) {
    Write-Error "GitHub CLI not found at '$GhPath'. Install: winget install GitHub.cli"
}

$ErrorActionPreference = "SilentlyContinue"
& $GhPath auth status 2>$null | Out-Null
$authOk = ($LASTEXITCODE -eq 0)
$ErrorActionPreference = "Stop"

if (-not $authOk) {
    if ($env:GITHUB_TOKEN) {
        $env:GITHUB_TOKEN | & $GhPath auth login --with-token 2>$null
    }
    else {
        Write-Host "Not logged in. Do ONE of the following, then re-run this script:" -ForegroundColor Yellow
        Write-Host "  gh auth login" -ForegroundColor Cyan
        Write-Host "  OR set `$env:GITHUB_TOKEN` to a PAT with 'repo' scope." -ForegroundColor Cyan
        exit 1
    }
}

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
Write-Host "Repository root: $root" -ForegroundColor Green

if (-not (Test-Path ".git")) {
    Write-Error "No .git folder in $root"
}

# Replace origin so push targets the new repo under your account
git remote remove origin 2>$null

& $GhPath repo create $RepoName `
    --public `
    --source=. `
    --remote=origin `
    --push `
    --description "Django ecommerce Hmart Render-ready"

$login = & $GhPath api user --jq .login
Write-Host "Done. Repo: https://github.com/$login/$RepoName" -ForegroundColor Green
Write-Host 'Next: Render → New Web Service → connect this repo; start: gunicorn Annu.wsgi:application --bind 0.0.0.0:$PORT' -ForegroundColor Yellow
