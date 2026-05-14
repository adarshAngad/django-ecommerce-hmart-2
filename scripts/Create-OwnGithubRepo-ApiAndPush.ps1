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
#>
param(
    [Parameter(Mandatory = $true)]
    [string] $RepoName,

    [string] $GitHubUser = '',

    [string] $Description = 'Django ecommerce — Render / Docker ready'
)

$ErrorActionPreference = 'Stop'
$token = $env:GITHUB_TOKEN
if (-not $token) {
    Write-Error 'Set $env:GITHUB_TOKEN to a classic personal access token with repo scope: https://github.com/settings/tokens'
}

$headers = @{
    Authorization = "Bearer $token"
    Accept        = 'application/vnd.github+json'
    'User-Agent'  = 'Create-OwnGithubRepo-ApiAndPush'
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

# Create repo (409 if already exists — then we only push)
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
    if ($resp -and [int]$resp.StatusCode -eq 422) {
        Write-Host "Repository already exists on GitHub; pushing latest commits." -ForegroundColor Yellow
    }
    else {
        throw
    }
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

$pushUrl = "https://x-access-token:$token@github.com/$GitHubUser/$RepoName.git"
try {
    git push $pushUrl "HEAD:refs/heads/$branch"
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
