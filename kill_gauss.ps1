$gaussExe = 'C:\GAUSS Ver1.1.74.102\application\Gauss.exe'
$simStarterExe = 'C:\GAUSS Ver1.1.74.102\application\Lib\SimStarter.exe'

if (-not (Test-Path -LiteralPath $gaussExe)) {
    Write-Host "Nu am gasit executabilul: $gaussExe"
    exit 1
}

$gaussPattern = '(?i)^"?C:\\GAUSS Ver1\.1\.74\.102\\application\\Gauss\.exe'
$simStarterPattern = '(?i)^"?C:\\GAUSS Ver1\.1\.74\.102\\application\\Lib\\SimStarter\.exe'

$targets = Get-CimInstance Win32_Process |
    Where-Object {
        $commandLine = $_.CommandLine -as [string]
        $isGauss = $_.Name -ieq 'Gauss.exe' -and (
            $_.ExecutablePath -ieq $gaussExe -or $commandLine -match $gaussPattern
        )
        $isSimStarter = $_.Name -ieq 'SimStarter.exe' -and (
            $_.ExecutablePath -ieq $simStarterExe -or $commandLine -match $simStarterPattern
        )
        $isGauss -or $isSimStarter
    } |
    Sort-Object @{ Expression = { $_.Name -ieq 'Gauss.exe' } }, ProcessId -Unique

if ($targets) {
    foreach ($target in $targets) {
        if (-not (Get-Process -Id $target.ProcessId -ErrorAction SilentlyContinue)) {
            continue
        }

        Write-Host "Oprire PID $($target.ProcessId) [$($target.Name)]..."
        & taskkill.exe /PID $target.ProcessId /F /T | Out-Host
    }
} else {
    Write-Host 'Nu am gasit procese Gauss.exe sau SimStarter.exe din folderul GAUSS.'
}

Write-Host 'Astept 5 secunde inainte de restart...'
Start-Sleep -Seconds 5
Write-Host 'Pornesc Gauss...'
Start-Process -FilePath $gaussExe
