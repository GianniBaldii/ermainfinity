$ErrorActionPreference = "Stop"

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

Stop-PortProcess -Port 8000
Stop-PortProcess -Port 5173

Write-Host "ERMA apagada."
