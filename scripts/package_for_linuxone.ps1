# ==============================================================================
# TrustLens: Package for IBM LinuxONE Deployment
# Theme: AI Secured - Innovation Without Exposure (IBM Z Datathon 2026)
# ==============================================================================
# Creates a clean, verified deployment archive from the Windows development environment.
# Strictly excludes: .env, secrets, *.pem, *.key, .venv, caches, test artifacts.
# ==============================================================================

[CmdletBinding()]
param (
    [string]$OutputDir = "dist",
    [string]$ArchiveName = "trustlens_s390x_deploy.tar.gz",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " TrustLens: Packaging for IBM LinuxONE (s390x)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Source Root: $ProjectRoot"
Write-Host "Target Archive: $OutputDir\$ArchiveName"

# 1. Verify required source files exist
$RequiredItems = @(
    "app.py",
    "config.py",
    "privacy.py",
    "integrity.py",
    "document_qa.py",
    "audit.py",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "pytest.ini",
    ".env.example",
    ".gitignore",
    "README.md",
    "docs",
    "sample_docs",
    "tests"
)

foreach ($item in $RequiredItems) {
    $fullPath = Join-Path $ProjectRoot $item
    if (-not (Test-Path $fullPath)) {
        Write-Error "Required project item missing: $item. Packaging aborted."
        exit 1
    }
}
Write-Host "[OK] All required project source files verified." -ForegroundColor Green

if ($DryRun) {
    Write-Host "[DRY-RUN] Validated source directory. Exiting without creating archive." -ForegroundColor Yellow
    exit 0
}

# 2. Setup Staging Directory
$OutDirPath = Join-Path $ProjectRoot $OutputDir
if (-not (Test-Path $OutDirPath)) {
    New-Item -ItemType Directory -Path $OutDirPath -Force | Out-Null
}

$StagingDir = Join-Path $ProjectRoot "build_staging_tmp"
if (Test-Path $StagingDir) {
    Remove-Item -Path $StagingDir -Recurse -Force
}
New-Item -ItemType Directory -Path $StagingDir -Force | Out-Null

try {
    Write-Host "Staging clean deployment files..." -ForegroundColor Gray

    # Copy files
    $FilesToCopy = @(
        "app.py",
        "config.py",
        "privacy.py",
        "integrity.py",
        "document_qa.py",
        "audit.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "pytest.ini",
        ".env.example",
        ".gitignore",
        "README.md"
    )

    foreach ($file in $FilesToCopy) {
        Copy-Item -Path (Join-Path $ProjectRoot $file) -Destination $StagingDir -Force
    }

    # Copy allowed directories with exclusions
    $DirsToCopy = @("docs", "sample_docs", "tests", "scripts", "submission")
    foreach ($dir in $DirsToCopy) {
        $destSubDir = Join-Path $StagingDir $dir
        $sourceDirFull = (Join-Path $ProjectRoot $dir)
        Get-ChildItem -Path $sourceDirFull -Recurse -File | ForEach-Object {
            # Strictly filter out cache and temporary files before creating paths
            if ($_.FullName -match '__pycache__' -or $_.FullName -match '\.pytest_cache') {
                return
            }
            $relPath = $_.FullName.Substring($sourceDirFull.Length).TrimStart("\", "/")
            $targetFilePath = Join-Path $destSubDir $relPath
            $targetParent = Split-Path -Parent $targetFilePath
            if (-not (Test-Path $targetParent)) {
                New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
            }
            Copy-Item -Path $_.FullName -Destination $targetFilePath -Force
        }
    }

    # Ensure empty data dir with .gitkeep
    $dataDir = Join-Path $StagingDir "data"
    New-Item -ItemType Directory -Path $dataDir -Force | Out-Null
    Set-Content -Path (Join-Path $dataDir ".gitkeep") -Value "# TrustLens local runtime data folder`n" -NoNewline

    # 3. Security Sanity Check on Staging
    Write-Host "Running cryptographic and secret sanity checks on staged package..." -ForegroundColor Gray

    $IllegalPatterns = @("*.pem", "*.key", "*.cert", ".env", "*.tmp", "__pycache__")
    foreach ($pattern in $IllegalPatterns) {
        $badFiles = Get-ChildItem -Path $StagingDir -Recurse -Filter $pattern -ErrorAction SilentlyContinue
        if ($badFiles) {
            Write-Error "CRITICAL SECURITY ERROR: Forbidden file '$($badFiles[0].FullName)' detected in deployment bundle! Aborting."
            exit 1
        }
    }

    # Check for actual .env file specifically
    if (Test-Path (Join-Path $StagingDir ".env")) {
        Write-Error "CRITICAL: .env file found in staging directory. Real secrets must never be packaged!"
        exit 1
    }

    Write-Host "[OK] Zero secrets, credentials, or cache artifacts present in staging." -ForegroundColor Green

    # 4. Generate compressed tar.gz archive using tar.exe
    $TarExe = Get-Command "tar.exe" -ErrorAction SilentlyContinue
    if (-not $TarExe) {
        Write-Error "tar.exe not found on system PATH. Install or ensure Windows tar is available."
        exit 1
    }

    $FinalArchivePath = Join-Path $OutDirPath $ArchiveName
    if (Test-Path $FinalArchivePath) {
        Remove-Item -Path $FinalArchivePath -Force
    }

    Write-Host "Compressing archive via tar.exe..." -ForegroundColor Gray
    & tar.exe -czf $FinalArchivePath -C $StagingDir .

    if (-not (Test-Path $FinalArchivePath)) {
        Write-Error "Failed to generate $FinalArchivePath"
        exit 1
    }

    # 5. Output Verification Details
    $ArchiveItem = Get-Item $FinalArchivePath
    $HashResult = Get-FileHash -Path $FinalArchivePath -Algorithm SHA256

    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Host " Deployment Package Created Successfully!" -ForegroundColor Green
    Write-Host "==================================================================" -ForegroundColor Green
    Write-Host "Archive:  $($ArchiveItem.FullName)"
    Write-Host "Size:     $([math]::Round($ArchiveItem.Length / 1KB, 2)) KB"
    Write-Host "SHA-256:  $($HashResult.Hash)"
    Write-Host ""
    Write-Host "Next Step: Run .\scripts\deploy_linuxone.ps1 to upload and deploy to IBM LinuxONE." -ForegroundColor Cyan

}
finally {
    if (Test-Path $StagingDir) {
        Remove-Item -Path $StagingDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}
