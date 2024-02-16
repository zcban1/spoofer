import winreg
import uuid
import random
import ctypes
import sys
import time
import subprocess
import os
import string


class Spoofer:
    class MachineId:        
        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\SQMClient", 0, winreg.KEY_WRITE) as key:
                    new_value = "{" + str(uuid.uuid4()) + "}"
                    winreg.SetValueEx(key, "MachineId", 0, winreg.REG_SZ, new_value)
                    print("[SPOOFER] MachineId Changed to", new_value)
                    return True
            except:
                return False

    class HardwareGUID:

        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", 0, winreg.KEY_WRITE) as key:
                    new_value = "{" + str(uuid.uuid4()) + "}"
                    winreg.SetValueEx(key, "HwProfileGuid", 0, winreg.REG_SZ, new_value)
                    print("[SPOOFER] HwProfileGuid Changed to", new_value)
                    return True
            except:
                return False

    class MachineGUID:
        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Cryptography", 0, winreg.KEY_WRITE) as key:
                    new_value = str(uuid.uuid4())
                    winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_value)
                    print("[SPOOFER] MachineGuid Changed to", new_value)
                    return True
            except:
                return False


    class EFIVariables:

        @staticmethod
        def spoof():
            try:
                efiVariables = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Nsi\\{eb004a03-9b1a-11d4-9123-0050047759bc}\\26", 0, winreg.KEY_WRITE)
                if efiVariables is not None:
                    efiVariableId = str(uuid.uuid4())
                    winreg.SetValueEx(efiVariables, "VariableId", 0, winreg.REG_SZ, efiVariableId)
                    winreg.CloseKey(efiVariables)
                    print("[SPOOFER] EFI Variables - VariableId Changed to", efiVariableId)
                else:
                    print("[SPOOFER] EFI Variables key not found.")
            except:
                print("[SPOOFER] Error accessing EFI Variables in the Registry... Maybe run as admin")


    class SystemInfo:
        @staticmethod
        def RandomId(length):
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for _ in range(length))

        @staticmethod
        def spoof():                
            # Modify BIOSReleaseDate
            dayStr = random.randint(1, 28)
            monthStr = random.randint(1, 12)
            winreg.SetValueEx(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "BIOSReleaseDate", winreg.REG_SZ, f"{dayStr}/{monthStr}/{random.randint(2000, 2023)}")
            print("[SPOOFER] BIOSReleaseDate Information values modified successfully.")   
            # Modify BIOSVersion
            winreg.SetValueEx(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "BIOSVersion", winreg.REG_SZ, Spoofer.SystemInfo.RandomId(10))
            print("[SPOOFER] BIOSVersion Information values modified successfully.")    
            # Modify ComputerHardwareId
            winreg.SetValueEx(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "ComputerHardwareId", winreg.REG_SZ, f"{{{uuid.uuid4()}}}")
            print("[SPOOFER] ComputerHardwareId Information values modified successfully.")     
            # Modify ComputerHardwareIds
            computer_hardware_ids = [str(uuid.uuid4()) for _ in range(3)]
            computer_hardware_ids_str = "\n".join(computer_hardware_ids)
            winreg.SetValueEx(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "ComputerHardwareIds", winreg.REG_SZ, computer_hardware_ids_str)
            print("[SPOOFER] ComputerHardwareIds Information values modified successfully.")     
            # Modify SystemManufacturer
            winreg.SetValueEx(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "SystemManufacturer", winreg.REG_SZ, Spoofer.SystemInfo.RandomId(15))
            print("[SPOOFER] SystemManufacturer Information values modified successfully.")    
            # Modify SystemProductName
            winreg.SetValueEx(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", "SystemProductName", winreg.REG_SZ, Spoofer.SystemInfo.RandomId(6))
                
            print("[SPOOFER] SystemProductName Information values modified successfully.")


    class ProductId:
        regeditPath = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"
        key = "ProductID"

        @staticmethod
        def get_value():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Spoofer.ProductId.regeditPath) as key:
                    value, _ = winreg.QueryValueEx(key, Spoofer.ProductId.key)
                    return str(value)
            except:
                return "ERR"

        @staticmethod
        def set_value(value):
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Spoofer.ProductId.regeditPath, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, Spoofer.ProductId.key, 0, winreg.REG_SZ, value)
                    return True
            except:
                return False
        @staticmethod
        def spoof():
            old_value = Spoofer.ProductId.get_value()
            new_value = "{}-{}-{}-{}".format(''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)),
                                             ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)),
                                             ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)),
                                             ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5)))
            result = Spoofer.ProductId.set_value(new_value)
            if result:
                print("[SPOOFER] Computer ProductID Changed from", old_value, "to", new_value)
            else:
                print("[SPOOFER] Error accessing the Registry... Maybe run as admin")
            return result


    class InstallationID:
        @staticmethod
        def spoof():
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_WRITE) as key:
                newInstallationID = str(uuid.uuid4())
                winreg.SetValueEx(key, "InstallationID", 0, winreg.REG_SZ, newInstallationID)
                print("[SPOOFER] InstallationID Changed to", newInstallationID)
                return True

    class PCName:
        @staticmethod
        def RandomId(length):
            characters = string.ascii_letters + string.digits
            return ''.join(random.choice(characters) for _ in range(length))
        
        @staticmethod
        def spoof():

            randomName = Spoofer.SystemInfo.RandomId(8)  # Generate a random PC name

            # Modify ComputerName keys
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ComputerName", 0, winreg.KEY_WRITE) as computerName:
                winreg.SetValueEx(computerName, "ComputerName", 0, winreg.REG_SZ, randomName)
                winreg.SetValueEx(computerName, "ActiveComputerName", 0, winreg.REG_SZ, randomName)
                winreg.SetValueEx(computerName, "ComputerNamePhysicalDnsDomain", 0, winreg.REG_SZ, "")

            # Modify ActiveComputerName keys
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\ComputerName\\ActiveComputerName", 0, winreg.KEY_WRITE) as activeComputerName:
                winreg.SetValueEx(activeComputerName, "ComputerName", 0, winreg.REG_SZ, randomName)
                winreg.SetValueEx(activeComputerName, "ActiveComputerName", 0, winreg.REG_SZ, randomName)
                winreg.SetValueEx(activeComputerName, "ComputerNamePhysicalDnsDomain", 0, winreg.REG_SZ, "")

            # Modify Tcpip Parameters keys
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters", 0, winreg.KEY_WRITE) as tcpipParams:
                winreg.SetValueEx(tcpipParams, "Hostname", 0, winreg.REG_SZ, randomName)
                winreg.SetValueEx(tcpipParams, "NV Hostname", 0, winreg.REG_SZ, randomName)

            # Modify Tcpip Interfaces keys
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces", 0, winreg.KEY_WRITE) as tcpipInterfaces:
                for interfaceKey in winreg.QueryInfoKey(tcpipInterfaces)[0]:
                    with winreg.OpenKey(tcpipInterfaces, interfaceKey, 0, winreg.KEY_WRITE) as interfaceSubKey:
                        winreg.SetValueEx(interfaceSubKey, "Hostname", 0, winreg.REG_SZ, randomName)
                        winreg.SetValueEx(interfaceSubKey, "NV Hostname", 0, winreg.REG_SZ, randomName)

            print("[SPOOFER] PC Name Changed to", randomName)
            return True




if __name__ == "__main__":

    Spoofer.MachineId.spoof()
    Spoofer.HardwareGUID.spoof()
    Spoofer.MachineGUID.spoof()
    Spoofer.EFIVariables.spoof()
    Spoofer.SystemInfo.spoof()
    Spoofer.ProductId.spoof()
    Spoofer.InstallationID.spoof()
    #Spoofer.PCName.spoof()
