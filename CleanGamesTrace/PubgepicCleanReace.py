import os
import winreg as reg
import shutil
import tempfile
from pathlib import Path

# Contenuto dello script PowerShell
powershell_script = """
$processNames = @("EpicGamesLauncher","Farlight84EpicLauncher")
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

$NomiFileDiLog = @("pubgepic log - File e Cartelle.txt")

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
$fileNames = @("pubgepic log - Elementi di Registro.txt") # Aggiungi altri nomi di file secondo necessità

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
"""


# Percorso del file PowerShell temporaneo
powershell_script_path = os.path.join(os.environ['TEMP'], 'temp_script.ps1')

# Scrivi lo script PowerShell nel file temporaneo
with open(powershell_script_path, 'w') as ps_file:
    ps_file.write(powershell_script)

# Esegui lo script PowerShell come amministratore usando PowerShell.exe
os.system(f'powershell.exe -ExecutionPolicy Bypass -File "{powershell_script_path}"')

# Lista dei nomi delle cartelle da eliminare
folders_to_delete = ["Epic Games", "Riot Games", "Ubisoft Game Launcher", "Steam", "Package Cache", "VALORANT", "EpicGamesLauncher"]

# Percorsi AppData Local, Roaming e ProgramData
app_data_local = Path(os.getenv('LOCALAPPDATA'))
app_data_roaming = Path(os.getenv('APPDATA'))
program_data = Path(os.getenv('PROGRAMDATA'))

# Percorsi delle cartelle temporanee
temp_user = Path(tempfile.gettempdir())
temp_windows = Path("C:/Windows/Temp")

def remove_folder_if_exists(base_path, folder_name=""):
    path_to_delete = base_path / folder_name
    if path_to_delete.exists():
        try:
            shutil.rmtree(path_to_delete)
            print(f"Eliminata la cartella: {path_to_delete}")
        except Exception as e:
            print(f"Non è stato possibile eliminare: {path_to_delete}. Errore: {e}")
    else:
        print(f"La cartella non esiste: {path_to_delete}")

def remove_contents(path):
    if path.exists():
        for item in path.glob('*'):
            try:
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
                print(f"Eliminato: {item}")
            except Exception as e:
                print(f"Non è stato possibile eliminare l'oggetto: {item}. Errore: {e}")
        print(f"Tentativo di eliminazione completato per: {path}")
    else:
        print(f"Il percorso non esiste: {path}")

# Pulizia delle cartelle specificate e delle cartelle temporanee
for folder in folders_to_delete:
    remove_folder_if_exists(app_data_local, folder)
    remove_folder_if_exists(app_data_roaming, folder)
    remove_folder_if_exists(program_data, folder)

remove_contents(temp_user)
remove_contents(temp_windows)


