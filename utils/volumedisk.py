import os
import random
import subprocess

def get_drive_letters():
    # Esegui il comando WMIC e ottieni le lettere dei dispositivi
    result = subprocess.run(["wmic", "logicaldisk", "get", "deviceid"], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    drive_letters = []
    for line in lines[1:]:  # Ignora l'intestazione
        elements = line.strip()
        if elements:
            drive_letters.append(elements)
    return drive_letters


def rename_drives():
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    # Ottengo informazioni dettagliate sulle unità, incluse dimensioni
    drive_info = subprocess.getoutput("wmic logicaldisk get deviceid, drivetype, size")
    drives = []

    for line in drive_info.splitlines()[1:]:  # Escludo l'intestazione
        parts = line.split()
        if parts and len(parts) >= 3:
            drive_type = int(parts[1])
            drive_size_bytes = int(parts[2]) if parts[2].isdigit() else 0
            drive_size_gb = round(drive_size_bytes / (1024**3))  # Converti in GB
            if drive_type in (2, 3):  # Tipo 2 è rimovibile (USB), 3 è fisso (SSD/HDD)
                drive_prefix = "USB" if drive_type == 2 else "SSD"
                drives.append((parts[0], drive_prefix, drive_size_gb))

    for drive, prefix, size_gb in drives:
        rand_name = f"{prefix}-{size_gb}Gb-" + ''.join(random.choice(alphanumeric) for _ in range(4))  # Aggiusta per mantenere lunghezza

        # Eseguo il comando per rinominare l'unità
        result = subprocess.run(["label", f"{drive}", rand_name], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Rinominata unità {drive} a {rand_name}")
        else:
            print(f"Errore nel rinominare l'unità {drive}: {result.stderr}")

            
def find_volumeid64_exe():
    for root, dirs, files in os.walk("C:\\"):  # Inizia dalla radice del drive C:\
        if "Volumeid64.exe" in files:
            return os.path.join(root, "volumeid64.exe")  # Restituisce il percorso completo se trovato
    return None  # Restituisce None se non viene trovato

def generate_serial_and_log():
    volumeid64_path = find_volumeid64_exe()  # Cerca il percorso di volumeid64.exe
    if volumeid64_path is None:
        print("volumeid64.exe non trovato.")
        return

    input_file = "Drive_Letters.txt"
    log_file = "serial-storage.txt"
    
    if not os.path.exists(input_file):
        print(f"Il file {input_file} non esiste.")
        return

    with open(log_file, "w") as log:  # Crea o svuota il file di log
        pass

    with open(input_file, "r") as file:
        for line in file:
            drive = line.strip()
            random_string = ''.join(random.choice("0123456789ABCDEF") for _ in range(4)) + '-' + ''.join(random.choice("0123456789ABCDEF") for _ in range(4))
            with open(log_file, "a") as log:
                log.write(f"Eseguo il comando per la lettera di unità {drive}\n")
                result = subprocess.run([volumeid64_path, drive, random_string], capture_output=True, text=True)
                log.write(result.stdout)
                log.write(result.stderr)

    print("Operazioni completate. Vedi il file di log per i dettagli:", log_file)

# Chiamate alle funzioni
drive_letters = get_drive_letters()
print(drive_letters)
rename_drives()
generate_serial_and_log()


