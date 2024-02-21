import subprocess
import os
import time

# Definisce il contenuto dello script PowerShell
ps_script_content = """
# Imposta il percorso del file di log sul desktop
$desktopPath = [Environment]::GetFolderPath("Desktop")
$logFile = Join-Path -Path $desktopPath -ChildPath "OldDeviceLog.txt"

# Importa il modulo PnpDevice
Import-Module PnpDevice | Out-File -FilePath $logFile

# Ottiene tutti i dispositivi PnP
$allDevices = Get-PnpDevice

# Stampa l'elenco completo dei dispositivi con lo stato di connessione e scrive nel file di log
"Elenco completo dei dispositivi con stato di connessione:" | Out-File -FilePath $logFile -Append
foreach ($device in $allDevices) {
    $status = if ($device.Present) { "Collegato" } else { "Non collegato" }
    "$($device.FriendlyName) - $status" | Out-File -FilePath $logFile -Append
}

# Linea vuota per separare le due liste e scrive nel file di log
"`nElenco dei dispositivi Non collegati:" | Out-File -FilePath $logFile -Append

# Filtra e stampa solo i dispositivi non collegati e scrive nel file di log
$nonConnectedDevices = $allDevices | Where-Object { -not $_.Present }
foreach ($device in $nonConnectedDevices) {
    "$($device.FriendlyName) - Non collegato" | Out-File -FilePath $logFile -Append
}

# Chiede conferma prima di procedere con la rimozione
$confirmRemoval = 'S' #Read-Host "Vuoi procedere con la rimozione dei dispositivi non collegati? (S/N)"
if ($confirmRemoval -eq 'S') {
    "Inizio rimozione dei dispositivi non collegati..." | Out-File -FilePath $logFile -Append
    foreach ($device in $nonConnectedDevices) {
        "Rimozione del dispositivo: $($device.FriendlyName)" | Out-File -FilePath $logFile -Append
        & pnputil /remove-device $device.InstanceId
    }
    "Rimozione completata." | Out-File -FilePath $logFile -Append
} else {
    "Rimozione annullata." | Out-File -FilePath $logFile -Append
}

"""

# Imposta il percorso e il nome del file dello script PowerShell
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
ps_script_filename = "manage_devices.ps1"
ps_script_path = os.path.join(desktop_path, ps_script_filename)

# Scrive lo script PowerShell in un file
with open(ps_script_path, "w") as ps_script_file:
    ps_script_file.write(ps_script_content)

# Comando per eseguire lo script PowerShell come amministratore
run_as_admin_command = f"powershell Start-Process powershell -ArgumentList '-File {ps_script_path}' -Verb RunAs"

# Esegue lo script PowerShell come amministratore
subprocess.run(run_as_admin_command, shell=True)


