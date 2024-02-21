import os
import subprocess
import time


def run_command(command):
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(e)

def main():
    # Aggiungere il percorso della cartella 'utils' al comando
    utils_path = "utils/"  # Assicurati che questo percorso sia corretto per il tuo sistema

    print("rimuovi_vecchi_log.py.")
    run_command(f"python {utils_path}rimuovi_vecchi_log.py")
    print("rimuovi_vecchi_log completed.")
    
    print("python GetSerial.py.")
    run_command(f"python {utils_path}GetSerial.py")
    print("GetSerial completed.")

    print("FOXTROT.")
    run_command(f"python {utils_path}foxtrot.py")
    print("FOXTROT completed.")

    print("volumedisk.")
    run_command(f"python {utils_path}volumedisk.py")
    print("volumedisk completed.")

    print("NmacV2.")
    run_command(f"python {utils_path}NmacV2.py")
    print("Nmac completed.")

    print("BIOS-AMI.")
    run_command(f"python {utils_path}BIOSAMI.py")
    print("BIOS-AMI completed.")

    print("deviceclean")
    run_command(f"python {utils_path}devicecleanV2.py")
    print("deviceclean completed.")

    print("ResetClean")
    run_command(f"python {utils_path}ResetCleanV2.py")
    print("ResetClean completed.")

    print("MonCru")
    run_command(f"python {utils_path}MonCru.py")
    print("MonCru completed.")
    time.sleep(2)

    print("Rename Pc & User")
    run_command(f"python {utils_path}rename.py")
    print("Rename Pc & User completed.")

    print("python logger.py.")
    run_command(f"python {utils_path}logger.py")
    print("logger completed.")

    print(f"Results have been saved")

    print("Riavvio del computer in corso...")
    os.system("shutdown /r /t 1 /f /d p:4:1")


if __name__ == "__main__":
    main()

