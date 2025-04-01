param()

function Invoke-UvLockInDirectory {
    param(
        [Parameter(Mandatory=$true)]
        [string]$ServicePath
    )

    $FullServicePath = Join-Path -Path $PSScriptRoot -ChildPath $ServicePath -Resolve

    Write-Host "--- Generating lock file for $ServicePath ---" -ForegroundColor Yellow

    if (-not (Test-Path -Path $FullServicePath -PathType Container)) {
        Write-Error "Directory not found: $FullServicePath"
        exit 1
    }

    Push-Location $FullServicePath
    Write-Host "Changed directory to $(Get-Location)"

    try {
        uv lock
        if ($LASTEXITCODE -ne 0) {
            throw "uv lock command failed with exit code $LASTEXITCODE"
        }
        Write-Host "Successfully generated uv.lock in $FullServicePath" -ForegroundColor Green
    }
    catch {
        Write-Error "Failed to generate uv.lock in $FullServicePath. Error: $($_.Exception.Message)"
        Pop-Location
        exit 1
    }

    Pop-Location
    Write-Host "Returned to $(Get-Location)"
    Write-Host "-------------------------------------------" -ForegroundColor Yellow
    Write-Host ""
}

$PSScriptRoot = Get-Location

Invoke-UvLockInDirectory -ServicePath "microservices\users"
Invoke-UvLockInDirectory -ServicePath "microservices\settings"

Write-Host "All lock files generated successfully." -ForegroundColor Green
exit 0