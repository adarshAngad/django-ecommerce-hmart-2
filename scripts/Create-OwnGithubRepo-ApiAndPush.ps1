<#
.SYNOPSIS
  Create a NEW public repo under YOUR GitHub account and push this project (no gh auth login required).

.DESCRIPTION
  Uses the GitHub REST API to create the repository, then pushes with your token once.
  Renames the existing `origin` (e.g. amaanc986/...) to `upstream` so you keep a reference.

  1. Create a classic PAT with **repo** scope: https://github.com/settings/tokens
  2. PowerShell:
       cd c:\work\Adam\ECOMMERCE-PROJECT-
       $env:GITHUB_TOKEN = "ghp_xxxxxxxx"
       .\scripts\Create-OwnGithubRepo-ApiAndPush.ps1 -RepoName "django-ecommerce-hmart"

  If you omit -GitHubUser, the script resolves the owner from the API (the account that owns the PAT).

  If API create returns 404, your token usually cannot create repos. Fix:
    - Classic PAT: enable the **repo** scope (https://github.com/settings/tokens — "Generate new token (classic)").
    - Or create an empty repo at https://github.com/new then re-run with -SkipRepoCreate

  Fine-grained tokens (github_pat_...) often cannot use POST /user/repos — use a classic ghp_ token with **repo**.
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $RepoName,

    [string] $GitHubUser = '',

    [string] $Description = 'Django ecommerce — Render / Docker ready',

    [switch] $SkipRepoCreate
)

$ErrorActionPreference = 'Stop'
$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Error 'Set $env:GITHUB_TOKEN to a classic personal access token with repo scope: https://github.com/settings/tokens'
}

$headers = @{
    Authorization              = "Bearer $token"
    Accept                     = 'application/vnd.github+json'
    'User-Agent'               = 'Create-OwnGithubRepo-ApiAndPush'
    'X-GitHub-Api-Version'     = '2022-11-28'
}

if (-not $GitHubUser) {
    $me = Invoke-RestMethod -Uri 'https://api.github.com/user' -Headers $headers -Method Get
    $GitHubUser = $me.login
    Write-Host "GitHub user (from token): $GitHubUser" -ForegroundColor Green
}

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root
if (-not (Test-Path '.git')) {
    Write-Error "No .git folder in $root"
}

# Create repo via API (skip if you already created an empty repo on github.com/new)
if (-not $SkipRepoCreate) {
    $body = @{
        name        = $RepoName
        description = $Description
        private     = $false
        has_issues  = $true
    } | ConvertTo-Json

    try {
        Invoke-RestMethod -Uri 'https://api.github.com/user/repos' -Headers $headers -Method Post -Body $body -ContentType 'application/json' | Out-Null
        Write-Host "Created https://github.com/$GitHubUser/$RepoName" -ForegroundColor Green
    }
    catch {
        $resp = $_.Exception.Response
        $code = if ($resp) { [int]$resp.StatusCode } else { 0 }
        if ($code -eq 422) {
            Write-Host "Repository already exists on GitHub; pushing latest commits." -ForegroundColor Yellow
        }
        elseif ($code -eq 404) {
            Write-Host ''
            Write-Host 'GitHub returned 404 on POST /user/repos. Common causes:' -ForegroundColor Yellow
            Write-Host '  1) Classic PAT (ghp_...) is missing the **repo** scope - create a new classic token and check **repo**.' -ForegroundColor Yellow
            Write-Host '  2) Fine-grained token (github_pat_...) often cannot create user repos - use a classic PAT with **repo**.' -ForegroundColor Yellow
            Write-Host ''
            Write-Host 'Workaround: open https://github.com/new' -ForegroundColor Cyan
            Write-Host "  Create a PUBLIC repo named exactly: $RepoName" -ForegroundColor Cyan
            Write-Host '  Do NOT add README, license, or .gitignore.' -ForegroundColor Cyan
            Write-Host ''
            Write-Host 'Then run (same folder, same token is OK):' -ForegroundColor Green
            Write-Host "  & '.\scripts\Create-OwnGithubRepo-ApiAndPush.ps1' -RepoName '$RepoName' -SkipRepoCreate" -ForegroundColor Green
            Write-Host ''
            exit 1
        }
        else {
            throw
        }
    }
}
else {
    Write-Host "Skipping API create (-SkipRepoCreate). Repo must already exist: https://github.com/$GitHubUser/$RepoName" -ForegroundColor Yellow
}

# If current origin is not this repo yet, keep it as upstream (e.g. old amaanc986 fork).
$remotes = @(git remote)
if ($remotes -contains 'origin') {
    $cur = (git remote get-url origin).Trim()
    if (-not (($cur -like "*${GitHubUser}*") -and ($cur -like "*${RepoName}*"))) {
        if ($remotes -contains 'upstream') {
            Write-Error "Remote 'upstream' already exists. Rename/remove it, then re-run."
        }
        Write-Host "Renaming origin -> upstream (was: $cur)" -ForegroundColor DarkGray
        git remote rename origin upstream
    }
}

$cloneUrl = "https://github.com/$GitHubUser/$RepoName.git"
if (-not ((git remote) -contains 'origin')) {
    git remote add origin $cloneUrl
}
else {
    git remote set-url origin $cloneUrl
}

$branch = (git branch --show-current).Trim()
if (-not $branch) { $branch = 'main' }

# URL-encode token so special characters do not break the URL userinfo.
$encToken = [System.Uri]::EscapeDataString($token)
$pushUrl = "https://x-access-token:${encToken}@github.com/$GitHubUser/$RepoName.git"
try {
    # Windows Git Credential Manager often overrides embedded tokens; disable helpers for this push.
    git -c credential.helper= push $pushUrl "HEAD:refs/heads/$branch"
    if ($LASTEXITCODE -ne 0) {
        Write-Host ''
        Write-Host 'git push failed.' -ForegroundColor Red
        Write-Host 'Common fixes:' -ForegroundColor Yellow
        Write-Host '  1) Create a new CLASSIC PAT with at least **public_repo** (or full **repo**) scope.' -ForegroundColor Yellow
        Write-Host '  2) Clear saved GitHub credentials (they override the token in the URL):' -ForegroundColor Yellow
        Write-Host '     Win+R -> control /name Microsoft.CredentialManager -> Windows Credentials' -ForegroundColor Cyan
        Write-Host '     Remove any github.com entries, then run this script again.' -ForegroundColor Cyan
        Write-Host '  3) Confirm the empty repo exists under YOUR user:' -ForegroundColor Yellow
        Write-Host "     https://github.com/$GitHubUser/$RepoName" -ForegroundColor Cyan
        exit 1
    }
}
finally {
    $pushUrl = $null
}

git remote set-url origin $cloneUrl
try {
    git branch --set-upstream-to="origin/$branch" $branch 2>$null
}
catch { }
Write-Host "Push complete. Remote origin -> $cloneUrl" -ForegroundColor Green
Write-Host "Open: https://github.com/$GitHubUser/$RepoName" -ForegroundColor Cyan
Write-Host "Render: connect this repo + branch main; fix or remove DATABASE_URL; deploy." -ForegroundColor Yellow
