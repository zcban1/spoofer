import os
import subprocess
import time

sleepp=1
def run_command(command, timeout=1):
    try:
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except subprocess.CalledProcessError:
        print(f"Error executing command: {command}")

def main():
    print("python GetSerial.py.")
    run_command("python GetSerial.py")
    time.sleep(sleepp)
    print("GetSerial completed.")    

    print("FOXTROT.")
    run_command("python foxtrot.py")
    time.sleep(sleepp)
    print("FOXTROT completed.")

    print("volumedisk.")
    run_command("python volumedisk.py")
    time.sleep(sleepp)
    print("volumedisk completed.")

    print("NmacV2.")
    run_command("python NmacV2.py")
    time.sleep(sleepp)
    print("Nmac completed.")

    print("BIOS-AMI.")
    run_command("python BIOSAMI.py")
    time.sleep(5)
    print("BIOS-AMI completed.")

    #print("Rename Pc & User")
    #run_command("python rename.py")
    #time.sleep(3)
    #print("Rename Pc & User completed.")

    print("ResetClean")
    run_command("python ResetCleanV2.py")
    time.sleep(sleepp)
    print("ResetClean completed.")

    print("MonCru")
    run_command("python MonCru.py")
    time.sleep(sleepp)
    print("MonCru completed.")

    print("deviceclean")
    run_command("python devicecleanV2.py")
    time.sleep(sleepp)
    print("deviceclean completed.")

    #print("driveclean")
    #run_command("python driveclean.py")
    #time.sleep(sleepp)
    #print("driveclean completed.")

   
    print("python logger.py.")
    run_command("python logger.py")
    time.sleep(sleepp)
    print("logger completed.")

    print(f"Results have been saved")

    print("Riavvio del computer in corso...")
    os.system("shutdown /r /t 0 /f /d p:4:1")


if __name__ == "__main__":
    main()

