# Enable script execution if not already enabled
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
.\.venv\Scripts\activate

# Add eksctl to PATH if it exists
$eksctlPath = "$env:USERPROFILE\.eksctl\bin"
if (Test-Path $eksctlPath) {
    $env:Path += ";$eksctlPath"
}

Write-Host "Environment activated! You can now use infra-cli commands."
Write-Host "Try: infra-cli --help" 