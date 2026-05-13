param(
    [switch]$Install,
    [switch]$Reload,
    [switch]$StopExisting
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$BackendDir = Join-Path $Root "erma\backend"
$FrontendDir = Join-Path $Root "erma\frontend"
$LogsDir = Join-Path $Root ".logs"
$PythonExe = Join-Path $BackendDir ".venv\Scripts\python.exe"

New-Item -ItemType Directory -Force -Path $LogsDir | Out-Null

function Ensure-Backend {
    if (!(Test-Path $PythonExe)) {
        Write-Host "Creando entorno virtual del backend..."
        Push-Location $BackendDir
        python -m venv .venv
        Pop-Location
        $script:Install = $true
    }

    if ($Install) {
        Write-Host "Instalando dependencias del backend..."
        Push-Location $BackendDir
        & $PythonExe -m pip install -r requirements.txt
        Pop-Location
    }
}

function Ensure-Frontend {
    $NodeModules = Join-Path $FrontendDir "node_modules"

    if ($Install -or !(Test-Path $NodeModules)) {
        Write-Host "Instalando dependencias del frontend..."
        Push-Location $FrontendDir
        npm.cmd install
        Pop-Location
    }
}

function Test-PortAvailable {
    param(
        [int]$Port,
        [string]$Name
    )

    $Connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
        Where-Object { $_.State -eq "Listen" } |
        Select-Object -First 1

    if ($Connection) {
        $Process = Get-Process -Id $Connection.OwningProcess -ErrorAction SilentlyContinue
        $ProcessName = if ($Process) { $Process.ProcessName } else { "PID $($Connection.OwningProcess)" }
        throw "No puedo iniciar $Name porque el puerto $Port ya esta en uso por $ProcessName. Ejecuta .\scripts\dev.cmd -StopExisting para reiniciar limpio."
    }
}

function Stop-PortProcess {
    param(
        [int]$Port
    )

    $Connections = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue |
        Where-Object { $_.State -eq "Listen" }

    foreach ($Connection in $Connections) {
        $Process = Get-Process -Id $Connection.OwningProcess -ErrorAction SilentlyContinue

        if ($Process) {
            Write-Host "Apagando proceso $($Process.ProcessName) en puerto $Port..."
            Stop-Process -Id $Process.Id -Force
        }
    }
}

function Stop-ErmaPorts {
    Stop-PortProcess -Port 8000
    Stop-PortProcess -Port 5173
    Start-Sleep -Seconds 1
}

function Start-ErmaProcess {
    param(
        [string]$Name,
        [string]$FilePath,
        [string[]]$ArgumentList,
        [string]$WorkingDirectory,
        [string]$OutLog,
        [string]$ErrLog
    )

    Write-Host "Iniciando $Name..."
    return Start-Process `
        -FilePath $FilePath `
        -ArgumentList $ArgumentList `
        -WorkingDirectory $WorkingDirectory `
        -RedirectStandardOutput $OutLog `
        -RedirectStandardError $ErrLog `
        -WindowStyle Hidden `
        -PassThru
}

Ensure-Backend
Ensure-Frontend

if ($StopExisting) {
    Stop-ErmaPorts
}

Test-PortAvailable -Port 8000 -Name "backend"
Test-PortAvailable -Port 5173 -Name "frontend"

$RunId = Get-Date -Format "yyyyMMdd-HHmmss"
$BackendOut = Join-Path $LogsDir "backend-$RunId.out.log"
$BackendErr = Join-Path $LogsDir "backend-$RunId.err.log"
$FrontendOut = Join-Path $LogsDir "frontend-$RunId.out.log"
$FrontendErr = Join-Path $LogsDir "frontend-$RunId.err.log"

$BackendArgs = @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000")

if ($Reload) {
    $BackendArgs = @("-m", "uvicorn", "app.main:app", "--reload", "--host", "127.0.0.1", "--port", "8000")
}

$Backend = Start-ErmaProcess `
    -Name "backend" `
    -FilePath $PythonExe `
    -ArgumentList $BackendArgs `
    -WorkingDirectory $BackendDir `
    -OutLog $BackendOut `
    -ErrLog $BackendErr

$Frontend = Start-ErmaProcess `
    -Name "frontend" `
    -FilePath "npm.cmd" `
    -ArgumentList @("run", "dev", "--", "--host", "127.0.0.1", "--port", "5173") `
    -WorkingDirectory $FrontendDir `
    -OutLog $FrontendOut `
    -ErrLog $FrontendErr

Write-Host ""
Write-Host "ERMA esta corriendo:"
Write-Host "Frontend: http://127.0.0.1:5173"
Write-Host "Backend:  http://127.0.0.1:8000"
Write-Host ""
Write-Host "Logs:"
Write-Host "Backend:  $BackendOut"
Write-Host "Frontend: $FrontendOut"
Write-Host ""
Write-Host "Para apagar ERMA, cerra esta terminal con Ctrl+C."

try {
    while ($true) {
        if ($Backend.HasExited) {
            throw "El backend se detuvo. Revisa $BackendErr"
        }

        if ($Frontend.HasExited) {
            throw "El frontend se detuvo. Revisa $FrontendErr"
        }

        Start-Sleep -Seconds 2
    }
}
finally {
    Write-Host ""
    Write-Host "Apagando ERMA..."

    if ($Backend -and !$Backend.HasExited) {
        Stop-Process -Id $Backend.Id -Force
    }

    if ($Frontend -and !$Frontend.HasExited) {
        Stop-Process -Id $Frontend.Id -Force
    }
}
