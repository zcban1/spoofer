import os
import winreg as reg

def delete_key(root, path):
    try:
        reg.DeleteKey(root, path)
        print(f"Chiave {path} eliminata.")
    except FileNotFoundError:
        print(f"La chiave {path} non esiste.")
    except PermissionError:
        print(f"Non hai i permessi per eliminare la chiave {path}.")
    except OSError as e:
        print(f"Errore durante l'eliminazione della chiave {path}: {e}")

def delete_value(key_path, value_name):
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_ALL_ACCESS) as key:
            reg.DeleteValue(key, value_name)
            print(f"Valore {value_name} eliminato.")
    except FileNotFoundError:
        print(f"Il valore {value_name} non esiste.")
    except OSError as e:
        print(f"Errore durante l'eliminazione del valore {value_name}: {e}")

# Percorsi delle chiavi da eliminare
key_paths = [
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riot Game Riot_Client.",
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riot Game valorant.live"
]

# Elimina le chiavi
for path in key_paths:
    delete_key(reg.HKEY_CURRENT_USER, path)

# Percorsi e nomi dei valori REG_DWORD da eliminare
value_paths = {
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\FeatureUsage\\AppSwitched": [
        "C:\\Riot Games\\Riot Client\\UX\\RiotClientUx.exe",
        "C:\\Riot Games\\VALORANT\\live\\ShooterGame\\Binaries\\Win64\\VALORANT-Win64-Shipping.exe"
    ],
    "SOFTWARE\\Classes\\Local Settings\\Software\\Microsoft\\Windows\\Shell\\MuiCache": [
        "C:\\Riot Games\\Riot Client\\RiotClientServices.exe.FriendlyAppName",
        "C:\\Riot Games\\Riot Client\\RiotClientServices.exe.ApplicationCompany"
    ],
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run": [
        "RiotClient"
    ]
}

# Elimina i valori REG_DWORD
for key_path, values in value_paths.items():
    for value_name in values:
        delete_value(key_path, value_name)

# Elimina la chiave SHC
shc_key_path = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\UFH\\SHC"
delete_key(reg.HKEY_CURRENT_USER, shc_key_path)



# Contenuto dello script PowerShell
powershell_script = """
$processNames = @("vgtray", "RiotClientServices")
foreach ($processName in $processNames) {
    $runningProcess = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if ($runningProcess) {
        Write-Output "Chiusura del processo $processName..."
        Stop-Process -Name $processName -Force
        Write-Output "Processo $processName chiuso con successo."
    } else {
        Write-Output "Il processo $processName non è in esecuzione."
    }
}

$NomiFileDiLog = @("RiotClient log - File e Cartelle.txt")

Write-Output "Inizio ricerca dei file di log in Disco C:"

foreach ($nomeFileDiLog in $NomiFileDiLog) {
    Write-Output "Cercando il file di log: $nomeFileDiLog nel Disco C:"

    $filesDiLog = Get-ChildItem -Path "C:\" -Filter $nomeFileDiLog -Recurse -ErrorAction SilentlyContinue -Force

    foreach ($fileDiLog in $filesDiLog) {
        $PercorsiFile = $fileDiLog.FullName
        Write-Output "File di log trovato: $PercorsiFile - Inizio elaborazione"

        $percorsi = Get-Content $PercorsiFile

        foreach ($linea in $percorsi) {
            $percorso = $linea -split '\s{4,}' | Select-Object -First 1
            Write-Output "Elaborazione del percorso: $percorso"

            if (Test-Path $percorso) {
                try {
                    # Ottieni l'oggetto di controllo degli accessi (ACL)
                    $acl = Get-Acl $percorso

                    # Controlla se l'utente corrente ha i diritti di eliminazione, altrimenti aggiungili
                    $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("BUILTIN\Administrators", "FullControl", "Allow")
                    $acl.AddAccessRule($rule)

                    # Imposta il nuovo oggetto di controllo degli accessi (ACL)
                    Set-Acl $percorso $acl

                    if (Test-Path $percorso -PathType Container) {
                        Write-Output "Trovata cartella: $percorso. Inizio eliminazione..."
                        Remove-Item $percorso -Recurse -Force 
                        Write-Output "Cartella eliminata: $percorso"
                    }
                    elseif (Test-Path $percorso -PathType Leaf) {
                        Write-Output "Trovato file: $percorso. Inizio eliminazione..."
                        Remove-Item $percorso -Force -Recurse
                        Write-Output "File eliminato: $percorso"
                    }
                }
                catch {
                    Write-Output "Il percorso non esiste o è stato già eliminato."
                }
            } else {
                Write-Output "Il percorso non esiste o è stato già eliminato."
            }
        }
    }
}

Write-Output "Elaborazione completata"

############################################################2 step
# Ora processa i file relativi agli elementi di registro
# Lista dei nomi dei file da cercare
# Lista dei nomi dei file da cercare
$fileNames = @("RiotClient log - Elementi di Registro.txt") # Aggiungi altri nomi di file secondo necessità

Write-Output "Inizio ricerca dei file in Disco C:"

foreach ($fileName in $fileNames) {
    Write-Output "Cercando il file: $fileName nel Disco C:"

    # Cerca il file nel Disco C:
    $files = Get-ChildItem -Path "C:\" -Filter $fileName -Recurse -ErrorAction SilentlyContinue -Force

    if ($files.Count -eq 0) {
        Write-Output "Nessun file trovato per: $fileName"
    }

    foreach ($file in $files) {
        $filePath = $file.FullName
        Write-Output "File trovato: $filePath - Inizio elaborazione"

        # Leggi il file riga per riga
        Get-Content $filePath | ForEach-Object {
            # Controlla se la riga contiene la parola "Creato"
            if ($_ -match "\s+Creato\s*$") {
                # Estrai il percorso della chiave di registro dalla riga
                $registryPath = ($_ -split "\s+Creato")[0].Trim()
                Write-Output "Chiave di registro da eliminare: $registryPath"
                
                # Verifica se la chiave di registro esiste
                if (Test-Path "Registry::$registryPath") {
                    # Elimina la chiave di registro
                    Remove-Item "Registry::$registryPath" -Force -Recurse
                    Write-Output "Eliminata chiave di registro: $registryPath"
                } else {
                    Write-Output "Chiave di registro non trovata: $registryPath"
                }
            }
        }
    }
}

Write-Output "Elaborazione completata"

# Definisci i percorsi delle chiavi nel Registro di sistema
$firstKeyPath = "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riot Game Riot_Client."
$secondKeyPath = "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riot Game valorant.live"

# Verifica se le chiavi esistono e se sì, eliminale
if (Test-Path $firstKeyPath) {
    Remove-Item -Path $firstKeyPath -Force
    Write-Host "Chiave $firstKeyPath eliminata."
} else {
    Write-Host "La chiave $firstKeyPath non esiste."
}

if (Test-Path $secondKeyPath) {
    Remove-Item -Path $secondKeyPath -Force
    Write-Host "Chiave $secondKeyPath eliminata."
} else {
    Write-Host "La chiave $secondKeyPath non esiste."
}





"""


# Percorso del file PowerShell temporaneo
powershell_script_path = os.path.join(os.environ['TEMP'], 'temp_script.ps1')

# Scrivi lo script PowerShell nel file temporaneo
with open(powershell_script_path, 'w') as ps_file:
    ps_file.write(powershell_script)

# Esegui lo script PowerShell come amministratore usando PowerShell.exe
os.system(f'powershell.exe -ExecutionPolicy Bypass -File "{powershell_script_path}"')
