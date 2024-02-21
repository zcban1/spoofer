import ctypes
import os
import subprocess
import datetime

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command_as_admin(command, output_file_name):
    if is_admin():
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            log_message(output_file_name, f"Output: {result.stdout}", "INFO")
        except subprocess.CalledProcessError as e:
            log_message(output_file_name, f"Error: {e.stderr}", "ERROR")
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "python", f'"{os.path.abspath(__file__)}" {command}', None, 1)

def log_message(output_file_name, message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] [{level}] {message}\n"
    with open(output_file_name, 'a') as file:
        file.write(formatted_message)


def delete_cache_files(cache_folder):
    """
    Funzione ausiliaria per eliminare i file nella cartella cache specificata.

    Args:
    cache_folder (str): Percorso della cartella cache.
    """
    if os.path.exists(cache_folder):
        for filename in os.listdir(cache_folder):
            file_path = os.path.join(cache_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Errore durante l\'eliminazione di {file_path}. Motivo: {e}')
        print(f"Pulizia della cache in {cache_folder} completata.")
    else:
        print(f"Cartella Cache in {cache_folder} non trovata.")

def clear_browser_cache():
    """
    Funzione per cancellare i file nella cartella cache di diversi browser.
    Cerca automaticamente le cartelle cache nel profilo utente corrente.
    """
    user_profile_path = os.environ['USERPROFILE']

    # Percorsi della cartella Cache dei browser
    brave_cache_folder = os.path.join(user_profile_path, r'AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Cache\Cache_Data')
    chrome_cache_folder = os.path.join(user_profile_path, r'AppData\Local\Google\Chrome\User Data\Default\Cache')

    # Chiama la funzione ausiliaria per ciascun browser
    delete_cache_files(brave_cache_folder)
    delete_cache_files(chrome_cache_folder)


output_file_name = 'system_maintenance_log.txt'

log_message(output_file_name, 'Inizio operazioni di manutenzione')

# Pulizia dei file di sistema temporanei
log_message(output_file_name, 'Pulizia dei file di sistema temporanei')
run_command_as_admin("cleanmgr /sagerun:1", output_file_name)

# Pulizia dei file temporanei di Windows
log_message(output_file_name, 'Pulizia dei file temporanei di Windows')
run_command_as_admin("del /q /f /s %temp%\\*", output_file_name)

# Pulizia dei file di log di Windows
log_message(output_file_name, 'Pulizia dei file di log di Windows')
run_command_as_admin("del /q /f /s %systemroot%\\Logs\\*", output_file_name)
run_command_as_admin("del /q /f /s %systemroot%\\Panther\\*", output_file_name)

# Pulizia della cache DNS
log_message(output_file_name, 'Pulizia della cache DNS')
run_command_as_admin("ipconfig /flushdns", output_file_name)

# Reset client DNS
log_message(output_file_name, ' Reset client DNS')
run_command_as_admin("netsh interface ip delete arpcache", output_file_name)
run_command_as_admin("netsh winsock reset", output_file_name)

# Ripristino delle impostazioni TCP/IP
log_message(output_file_name, 'Ripristino delle impostazioni TCP/IP')
run_command_as_admin("netsh winsock reset", output_file_name)
run_command_as_admin("netsh int ip reset", output_file_name)


# Rimozione dei programmi dall'avvio automatico
log_message(output_file_name, 'Rimozione dei programmi dall\'avvio automatico')
run_command_as_admin("reg delete HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /f", output_file_name)
run_command_as_admin("reg delete HKLM\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /f", output_file_name)


# Pulizia dei Report di Errori di Windows
log_message(output_file_name, 'Pulizia dei Report di Errori di Windows')
run_command_as_admin("del /q /f /s %systemroot%\\Minidump\\*", output_file_name)
run_command_as_admin("WEvtUtil cl Application", output_file_name)

# Rimozione dei File di Installazione Obsoleti
log_message(output_file_name, 'Rimozione dei File di Installazione Obsoleti')
run_command_as_admin("Dism.exe /online /Cleanup-Image /StartComponentCleanup /ResetBase", output_file_name)

# Pulizia della Cartella di Download
log_message(output_file_name, 'Pulizia della Cartella di Download')
run_command_as_admin("del /q /f /s %userprofile%\\Downloads\\*", output_file_name)

# Pulizia del Cestino
log_message(output_file_name, 'Pulizia del Cestino')
run_command_as_admin("rd /s /q %systemdrive%\\$Recycle.bin", output_file_name)

# Pulizia del File di Paginazione al Riavvio
#log_message(output_file_name, 'Pulizia del File di Paginazione al Riavvio')
#run_command_as_admin('reg add "HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" /v ClearPageFileAtShutdown /t REG_DWORD /d 1 /f', output_file_name)

# Pulizia dei File di Ripristino della Configurazione di Sistema
log_message(output_file_name, 'Pulizia dei File di Ripristino della Configurazione di Sistema')
run_command_as_admin("vssadmin Delete Shadows /All /Quiet", output_file_name)

# Pulizia dei File di Aggiornamento di Windows Obsoleti
log_message(output_file_name, 'Pulizia dei File di Aggiornamento di Windows Obsoleti')
run_command_as_admin("Dism.exe /online /Cleanup-Image /SPSuperseded", output_file_name)

log_message(output_file_name, 'Pulizia browser cache')
clear_browser_cache()



log_message(output_file_name, 'Operazioni completate')

print('Operazioni completate. I risultati sono stati registrati in', output_file_name)

