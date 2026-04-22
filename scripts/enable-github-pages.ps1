<#
.SYNOPSIS
  Enables GitHub Pages for this repo with source = GitHub Actions.

.DESCRIPTION
  Create a PAT: https://github.com/settings/tokens — scope **repo** (private repos) or **public_repo** (public only).

  Run:
    $env:GITHUB_TOKEN = "ghp_...."
    .\scripts\enable-github-pages.ps1
#>
param(
  [string]$Owner = "Sancte3D",
  [string]$Repo = "WebsiteME",
  [string]$Token = $env:GITHUB_TOKEN
)

$ErrorActionPreference = "Stop"
if (-not $Token) {
  Write-Host "Set GITHUB_TOKEN to a PAT, then run again." -ForegroundColor Yellow
  Write-Host '  $env:GITHUB_TOKEN = "ghp_..."' -ForegroundColor Gray
  Write-Host "  .\scripts\enable-github-pages.ps1" -ForegroundColor Gray
  exit 1
}

$headers = @{
  Authorization          = "Bearer $Token"
  Accept                 = "application/vnd.github+json"
  "X-GitHub-Api-Version" = "2022-11-28"
}

$uri = "https://api.github.com/repos/$Owner/$Repo/pages"
$body = @{ build_type = "workflow" } | ConvertTo-Json

try {
  Invoke-RestMethod -Method Put -Uri $uri -Headers $headers -Body $body -ContentType "application/json"
  Write-Host "OK: Pages set to GitHub Actions. Check Actions for deploy, then Settings -> Pages for URL." -ForegroundColor Green
}
catch {
  Write-Host $_.Exception.Message -ForegroundColor Red
  if ($_.ErrorDetails.Message) { Write-Host $_.ErrorDetails.Message -ForegroundColor Red }
  exit 1
}
