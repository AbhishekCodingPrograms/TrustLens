# ==============================================================================
# TrustLens: Deploy to IBM LinuxONE (s390x)
# Theme: AI Secured - Innovation Without Exposure (IBM Z Datathon 2026)
# ==============================================================================
# Securely transfers the verified deployment archive over SCP/SSH,
# extracts it into an isolated remote directory, and optionally bootstraps
# the Python 3.12 virtual environment and runs the test suite on LinuxONE.
# ==============================================================================

[CmdletBinding()]
param (
    [string]$ServerIP = "148.100.77.3",
    [string]$SSHUser = "linux1",
    [string]$SSHKeyPath = "$HOME\Downloads\trustlenskey.pem",
    [string]$ArchiveFile = "dist\trustlens_s390x_deploy.tar.gz",
    [string]$RemoteTargetDir = "TrustLens",
    [switch]$BootstrapRemote,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Expand environment variables in SSHKeyPath
$ResolvedKeyPath = [System.Environment]::ExpandEnvironmentVariables($SSHKeyPath)
$ResolvedArchive = Join-Path $ProjectRoot $ArchiveFile

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host " TrustLens: Remote Deployment to IBM LinuxONE (s390x)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Remote Host:       $SSHUser@$ServerIP"
Write-Host "SSH Key:           $ResolvedKeyPath"
Write-Host "Local Archive:     $ResolvedArchive"
Write-Host "Remote Target Dir: $RemoteTargetDir"

# 1. Pre-flight Local Validations
if (-not (Test-Path $ResolvedKeyPath)) {
    Write-Error "SSH private key not found at '$ResolvedKeyPath'. Please check the path and try again."
    exit 1
}

if (-not (Test-Path $ResolvedArchive)) {
    Write-Host "Deployment archive not found. Generating package now..." -ForegroundColor Yellow
    & powershell -ExecutionPolicy Bypass -File (Join-Path $ScriptDir "package_for_linuxone.ps1")
    if (-not (Test-Path $ResolvedArchive)) {
        Write-Error "Could not locate or generate '$ResolvedArchive'."
        exit 1
    }
}

$ArchiveItem = Get-Item $ResolvedArchive
$ArchiveName = $ArchiveItem.Name
Write-Host "[OK] Local archive verified: $([math]::Round($ArchiveItem.Length / 1KB, 2)) KB" -ForegroundColor Green

# 2. Check SSH & SCP Executables
$SshExe = Get-Command "ssh.exe" -ErrorAction SilentlyContinue
$ScpExe = Get-Command "scp.exe" -ErrorAction SilentlyContinue

if (-not $SshExe -or -not $ScpExe) {
    Write-Error "OpenSSH client (ssh.exe, scp.exe) not found on system PATH."
    exit 1
}

# Base SSH parameters (strict key checking with batch mode fallback)
$SshArgs = @(
    "-n",
    "-i", $ResolvedKeyPath,
    "-o", "BatchMode=yes",
    "-o", "StrictHostKeyChecking=accept-new",
    "-o", "ConnectTimeout=10"
)

if ($DryRun) {
    Write-Host ""
    Write-Host "[DRY-RUN MODE] Commands that would be executed:" -ForegroundColor Yellow
    Write-Host "1. Test connectivity: ssh $($SshArgs -join ' ') $SSHUser@$ServerIP 'uname -m'"
    Write-Host "2. Create target directory: ssh $($SshArgs -join ' ') $SSHUser@$ServerIP 'mkdir -p $RemoteTargetDir'"
    Write-Host "3. Upload archive: scp -i $ResolvedKeyPath $ResolvedArchive $SSHUser@${ServerIP}:${RemoteTargetDir}/"
    Write-Host "4. Extract archive: ssh $($SshArgs -join ' ') $SSHUser@$ServerIP 'cd $RemoteTargetDir && tar -xzf $ArchiveName'"
    if ($BootstrapRemote) {
        Write-Host "5. Bootstrap venv: ssh $($SshArgs -join ' ') $SSHUser@$ServerIP 'cd $RemoteTargetDir && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/pytest tests/ -v'"
    }
    exit 0
}

# 3. Test Remote Connectivity & Architecture
Write-Host "Connecting to remote LinuxONE host..." -ForegroundColor Gray
try {
    $remoteArch = (& ssh.exe @SshArgs "$SSHUser@$ServerIP" "uname -m").Trim()
    Write-Host "[OK] Connected successfully! Remote Architecture: $remoteArch" -ForegroundColor Green
    if ($remoteArch -ne "s390x") {
        Write-Warning "Target architecture is '$remoteArch' (expected s390x). Proceeding with caution."
    }
}
catch {
    Write-Error "Failed to connect to $SSHUser@$ServerIP via SSH: $_"
    exit 1
}

# 4. Create Remote Project Directory
Write-Host "Creating remote directory '$RemoteTargetDir'..." -ForegroundColor Gray
& ssh.exe @SshArgs "$SSHUser@$ServerIP" "mkdir -p $RemoteTargetDir"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create remote directory '$RemoteTargetDir'."
    exit 1
}

# 5. Secure Copy (SCP) Archive to LinuxONE
Write-Host "Uploading '$ArchiveName' over SCP..." -ForegroundColor Gray
& scp.exe -o BatchMode=yes -o StrictHostKeyChecking=accept-new -i $ResolvedKeyPath $ResolvedArchive "$SSHUser@${ServerIP}:${RemoteTargetDir}/$ArchiveName"
if ($LASTEXITCODE -ne 0) {
    Write-Error "SCP upload failed."
    exit 1
}
Write-Host "[OK] Archive uploaded to LinuxONE successfully." -ForegroundColor Green

# 6. Extract Archive on Remote Server
Write-Host "Extracting archive on remote host..." -ForegroundColor Gray
& ssh.exe @SshArgs "$SSHUser@$ServerIP" "cd $RemoteTargetDir && tar -xzf $ArchiveName && rm -f $ArchiveName"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Remote archive extraction failed."
    exit 1
}
Write-Host "[OK] Application files extracted on LinuxONE." -ForegroundColor Green

# 7. Optional Bootstrap & Testing on Remote Server
if ($BootstrapRemote) {
    Write-Host ""
    Write-Host "==================================================================" -ForegroundColor Cyan
    Write-Host " Bootstrapping Python Environment & Running Tests on LinuxONE" -ForegroundColor Cyan
    Write-Host "==================================================================" -ForegroundColor Cyan

    $bootstrapCmd = @"
set -e
cd $RemoteTargetDir
if [ ! -d ".venv" ]; then
    echo "Creating Python 3.12 virtual environment on s390x..."
    python3 -m venv .venv
fi
echo "Upgrading pip and installing s390x dependencies..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
echo "Running full automated test suite on IBM LinuxONE..."
.venv/bin/pytest tests/ -v
"@

    & ssh.exe @SshArgs "$SSHUser@$ServerIP" "bash -c '$bootstrapCmd'"
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[SUCCESS] All tests passed natively on IBM LinuxONE (s390x)!" -ForegroundColor Green
    } else {
        Write-Warning "Remote test suite encountered failures or setup warnings. Check output above."
    }
}

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host " Remote Deployment Complete!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "To launch TrustLens on IBM LinuxONE in localhost-only mode:" -ForegroundColor White
Write-Host "  ssh -i `"$ResolvedKeyPath`" $SSHUser@$ServerIP `"cd $RemoteTargetDir && .venv/bin/streamlit run app.py --server.address 127.0.0.1 --server.port 8501`"" -ForegroundColor Cyan
Write-Host ""
Write-Host "To securely access the UI from your local Windows browser via SSH tunnel:" -ForegroundColor White
Write-Host "  ssh -i `"$ResolvedKeyPath`" -L 8501:127.0.0.1:8501 $SSHUser@$ServerIP" -ForegroundColor Cyan
Write-Host "  Then open: http://localhost:8501" -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Green
