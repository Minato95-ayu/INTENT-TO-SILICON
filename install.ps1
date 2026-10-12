$ErrorActionPreference = 'Stop'

$installer = Join-Path $PSScriptRoot 'website\public\install.ps1'
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) {
    throw "Installer script not found: $installer"
}

& $installer
if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}
