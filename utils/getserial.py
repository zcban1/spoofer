import subprocess
import os
from datetime import datetime

OUTPUT_FILE = "getSerial_py.txt"

# Ottieni il nome utente corrente
current_username = os.getlogin()

# Ottieni la data e l'ora correnti
current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(OUTPUT_FILE, "w") as output_file:
    output_file.write(f"Autore: {current_username}\n")
    output_file.write(f"Data e ora di creazione: {current_datetime}\n\n")
    
    # Informazioni sul nome del computer
    output_file.write("ComputerSystem Name:\n")
    output_file.write(subprocess.getoutput("wmic computersystem get name"))

    # Account Utente filtrati
    output_file.write("\n\nUser Accounts (filtered):\n")
    # Questo comando elenca gli account, potresti voler filtrare ulteriormente questi risultati.
    user_accounts = subprocess.getoutput("wmic useraccount get name,sid")
    # Aggiungi qui il filtraggio per escludere account di sistema predefiniti, se necessario
    output_file.write(user_accounts)


    # Numero di serie del BIOS
    output_file.write("\n\nBIOS Serial Number:\n")
    output_file.write(subprocess.getoutput("wmic bios get serialnumber"))


    # Numero di serie della CPU
    output_file.write("\n\nCPU Serial Number:\n")
    output_file.write(subprocess.getoutput("wmic cpu get serialnumber"))

    # Numero di serie del Case del Sistema
    output_file.write("\n\nSystem Enclosure Serial Number:\n")
    output_file.write(subprocess.getoutput("wmic systemenclosure get serialnumber"))

    # Numeri di serie della Scheda Madre
    output_file.write("\n\nBaseBoard Serial Numbers:\n")
    output_file.write(subprocess.getoutput("wmic baseboard get serialnumber"))

    # Numeri di serie dei Chip di Memoria RAM
    output_file.write("\n\nMemory Chip Serial Numbers:\n")
    output_file.write(subprocess.getoutput("wmic memorychip get serialnumber"))

    # Informazioni sui dischi SERIAL NUMBER
    output_file.write("\n\nDisk Drive SERIAL NUMBER:\n")
    output_file.write(subprocess.getoutput("wmic diskdrive get model,serialnumber"))

    # Seriali dei volumi PARTITION SERIAL
    output_file.write("\n\nDisk Serial Partition:\n")
    output_file.write(subprocess.getoutput("vol C:"))
    output_file.write(subprocess.getoutput("vol D:"))
    output_file.write(subprocess.getoutput("vol E:"))

    # Informazioni sull'adattatore di rete
    output_file.write("\n\nNetwork Adapter Information:\n")
    output_file.write(subprocess.getoutput('wmic nic where "NetConnectionStatus=2" get Name,macaddress'))

    # Informazioni sulla GPU NVIDIA
    output_file.write("\n\nNVIDIA GPU UUID Information:\n")
    output_file.write(subprocess.getoutput('nvidia-smi --query-gpu=gpu_name,uuid --format=csv'))

    # Numeri di serie dei monitor
    powershell_command = 'PowerShell -Command "Get-WmiObject -Namespace root\wmi -Class WmiMonitorID | ForEach-Object { [System.Text.Encoding]::ASCII.GetString($_.SerialNumberID) }"'
    output_file.write("\n\nMonitor dysp Serial Numbers:\n")
    output_file.write(subprocess.getoutput(powershell_command))

    

print(f"Results have been saved to {OUTPUT_FILE}")

