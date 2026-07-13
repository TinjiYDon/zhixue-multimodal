# Create BACKLOG Epic Issues (P0-2 .. P0-7)
# Run from repo root:
#   powershell -ExecutionPolicy Bypass -File .\scripts\create_backlog_issues.ps1

$ErrorActionPreference = "Stop"
$Repo = "TinjiYDon/zhixue-multimodal"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$BodyDir = Join-Path $ScriptDir "issue-bodies"

# Collaborator list order = role order: miniapp, web, multimedia, backend
$Assignees = @{
  P02 = @("TinjiYDon")
  P03 = @("whq6830-arch")
  P04 = @("yucc280")
  P05 = @("TinjiYDon")
  P06 = @("RynnYuan")
  P07 = @("oceancat91")
}

$Labels = @(
  @{ Name = "p0-2"; Color = "1d76db"; Desc = "upload course" }
  @{ Name = "p0-3"; Color = "5319e7"; Desc = "multimedia whisper" }
  @{ Name = "p0-4"; Color = "0e8a16"; Desc = "job api worker" }
  @{ Name = "p0-5"; Color = "d93f0b"; Desc = "alignment rag" }
  @{ Name = "p0-6"; Color = "fbca04"; Desc = "web frontend" }
  @{ Name = "p0-7"; Color = "006b75"; Desc = "uniapp miniapp" }
  @{ Name = "api"; Color = "0075ca"; Desc = "backend api" }
  @{ Name = "multimedia"; Color = "bfd4f2"; Desc = "ffmpeg asr ocr" }
  @{ Name = "jobs"; Color = "c2e0c6"; Desc = "job domain" }
  @{ Name = "worker"; Color = "fef2c0"; Desc = "async worker" }
  @{ Name = "web"; Color = "d4c5f9"; Desc = "vue web" }
  @{ Name = "miniapp"; Color = "c5def5"; Desc = "miniapp" }
)

$Issues = @(
  @{ Key = "P02"; Num = "2"; Title = "[P0-2] upload API + Course"; Labels = "p0-2,api"; BodyFile = "P02.md" }
  @{ Key = "P03"; Num = "3"; Title = "[P0-3] FFmpeg + WhisperX + OCR"; Labels = "p0-3,multimedia"; BodyFile = "P03.md" }
  @{ Key = "P04"; Num = "4"; Title = "[P0-4] Job/Course API + Worker"; Labels = "p0-4,api,jobs,worker"; BodyFile = "P04.md" }
  @{ Key = "P05"; Num = "5"; Title = "[P0-5] alignment + RAG + /ask"; Labels = "p0-5,api"; BodyFile = "P05.md" }
  @{ Key = "P06"; Num = "6"; Title = "[P0-6] Web timeline + Q&A"; Labels = "p0-6,web"; BodyFile = "P06.md" }
  @{ Key = "P07"; Num = "7"; Title = "[P0-7] UniApp miniapp"; Labels = "p0-7,miniapp"; BodyFile = "P07.md" }
)

function Ensure-Label($Name, $Color, $Description) {
  gh label create $Name --repo $Repo --color $Color --description $Description --force 2>$null
}

function Issue-Exists($Num) {
  $q = "[P0-$Num]"
  $found = gh issue list --repo $Repo --search "in:title $q" --json number,title --limit 5 | ConvertFrom-Json
  return ($found | Where-Object { $_.title -like "$q*" }).Count -gt 0
}

Write-Host "==> Ensuring labels..."
foreach ($lb in $Labels) {
  Ensure-Label $lb.Name $lb.Color $lb.Desc
}

Write-Host "==> Creating issues..."
$Created = @()

foreach ($item in $Issues) {
  if (Issue-Exists $item.Num) {
    Write-Host "SKIP  $($item.Title) (already exists)"
    continue
  }

  $bodyPath = Join-Path $BodyDir $item.BodyFile
  if (-not (Test-Path $bodyPath)) {
    Write-Warning "SKIP  $($item.Title) - missing body file $bodyPath"
    continue
  }

  $users = $Assignees[$item.Key]
  $assignArg = ($users -join ",")

  $url = gh issue create --repo $Repo `
    --title $item.Title `
    --label $item.Labels `
    --assignee $assignArg `
    --body-file $bodyPath 2>&1 | Out-String
  $url = $url.Trim()

  if ($LASTEXITCODE -ne 0) {
    Write-Warning "Assign failed for $($item.Title) ($assignArg) - creating without assignee"
    $url = gh issue create --repo $Repo `
      --title $item.Title `
      --label $item.Labels `
      --body-file $bodyPath
  }

  Write-Host "OK    $url"
  $Created += $url
}

Write-Host ""
Write-Host "Done. Created $($Created.Count) issue(s)."
if ($Created.Count -lt $Issues.Count) {
  Write-Host "Tip: skipped items may already exist or RynnYuan must Accept invite first."
  Write-Host "Collaborators: gh api repos/$Repo/collaborators --jq '.[].login'"
}
