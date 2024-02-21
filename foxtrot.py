import winreg
import uuid
import random
import string
import os

class Spoofer:
    @staticmethod
    def log_change(operation, old_value, new_value):
        log_message = f"[SPOOFER] {operation} Changed from {old_value} to {new_value}"
        print(log_message)  # Print to console
        with open("spoofer_log.txt", "a") as log_file:
            log_file.write(log_message + "\n")

    class MachineId:
        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\SQMClient", 0, winreg.KEY_ALL_ACCESS) as key:
                    old_value, _ = winreg.QueryValueEx(key, "MachineId")
                    new_value = "{" + str(uuid.uuid4()) + "}"
                    winreg.SetValueEx(key, "MachineId", 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change("MachineId", old_value, new_value)
                    return True
            except Exception as e:
                print(f"[SPOOFER] Error: {e}")
                return False

    class HardwareGUID:
        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001", 0, winreg.KEY_ALL_ACCESS) as key:
                    old_value, _ = winreg.QueryValueEx(key, "HwProfileGuid")
                    new_value = "{" + str(uuid.uuid4()) + "}"
                    winreg.SetValueEx(key, "HwProfileGuid", 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change("HwProfileGuid", old_value, new_value)
                    return True
            except Exception as e:
                print(f"[SPOOFER] Error: {e}")
                return False

    class MachineGUID:
        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Cryptography", 0, winreg.KEY_ALL_ACCESS) as key:
                    old_value, _ = winreg.QueryValueEx(key, "MachineGuid")
                    new_value = str(uuid.uuid4())
                    winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change("MachineGuid", old_value, new_value)
                    return True
            except Exception as e:
                print(f"[SPOOFER] Error: {e}")
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
            key_path = "SYSTEM\\CurrentControlSet\\Control\\IDConfigDB\\Hardware Profiles\\0001"
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS) as key:
                    # Modify BIOSReleaseDate
                    try:
                        old_bios_date, _ = winreg.QueryValueEx(key, "BIOSReleaseDate")
                    except FileNotFoundError:
                        old_bios_date = "Not Set"
                    new_bios_date = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(2000, 2023)}"
                    winreg.SetValueEx(key, "BIOSReleaseDate", 0, winreg.REG_SZ, new_bios_date)
                    Spoofer.log_change("BIOSReleaseDate", old_bios_date, new_bios_date)

                    # Modify BIOSVersion
                    try:
                        old_bios_version, _ = winreg.QueryValueEx(key, "BIOSVersion")
                    except FileNotFoundError:
                        old_bios_version = "Not Set"
                    new_bios_version = Spoofer.SystemInfo.RandomId(5)
                    winreg.SetValueEx(key, "BIOSVersion", 0, winreg.REG_SZ, new_bios_version)
                    Spoofer.log_change("BIOSVersion", old_bios_version, new_bios_version)

                    # Modify ComputerHardwareId
                    try:
                        old_hardware_id, _ = winreg.QueryValueEx(key, "ComputerHardwareId")
                    except FileNotFoundError:
                        old_hardware_id = "Not Set"

                    new_hardware_id = f"{{{uuid.uuid4()}}}"
                    winreg.SetValueEx(key, "ComputerHardwareId", 0, winreg.REG_SZ, new_hardware_id)
                    Spoofer.log_change("ComputerHardwareId", old_hardware_id, new_hardware_id)

                    return True
            except Exception as e:
                print(f"[SPOOFER] Error modifying SystemInfo: {e}")
                return False

    class SystemInfoExtended:
        @staticmethod
        def random_id(length):
            characters = string.digits
            return ''.join(random.choice(characters) for _ in range(length))

        @staticmethod
        def spoof():
            try:
                # Paths for system and BIOS information in the registry
                system_info_key_path = "HARDWARE\\DESCRIPTION\\System"
                bios_info_key_path = "HARDWARE\\DESCRIPTION\\System\\BIOS"

                # Spoofing system information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as system_key:
                    value_name = "SystemFamily"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(system_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(system_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)
                
                # Spoofing system information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as system_key:
                    value_name = "SystemManufacturer"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(system_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(system_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing system information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as system_key:
                    value_name = "SystemProductName"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(system_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(system_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing system information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as system_key:
                    value_name = "SystemSKU"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(system_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(system_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing system information   
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as system_key:
                    value_name = "SystemVersion"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(system_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(system_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)



                # Spoofing Board information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as bios_key:
                    value_name = "BaseBoardManufacturer"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(bios_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(bios_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing Board information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as bios_key:
                    value_name = "BaseBoardProduct"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(bios_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(bios_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing Board information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as bios_key:
                    value_name = "BaseBoardVersion"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(bios_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(bios_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing Board information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as bios_key:
                    value_name = "BIOSReleaseDate"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(bios_key, value_name)
                    new_value = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(2000, 2023)}"
                    winreg.SetValueEx(bios_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                # Spoofing Board information
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, bios_info_key_path, 0, winreg.KEY_ALL_ACCESS) as bios_key:
                    value_name = "BIOSVendor"
                    old_value = Spoofer.SystemInfoExtended.get_current_value(bios_key, value_name)
                    new_value = Spoofer.SystemInfoExtended.random_id(14)
                    winreg.SetValueEx(bios_key, value_name, 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change(value_name, old_value, new_value)

                return True
            except Exception as e:
                print(f"[SPOOFER] Error modifying extended SystemInfo: {e}")
                return False

        @staticmethod
        def get_current_value(key, value_name):
            try:
                return winreg.QueryValueEx(key, value_name)[0]
            except FileNotFoundError:
                return "Not Set"


    class ProductId:
        @staticmethod
        def get_value():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_READ) as key:
                    value, _ = winreg.QueryValueEx(key, "ProductId")
                    return value
            except Exception as e:
                print(f"[SPOOFER] Error reading ProductId: {e}")
                return "Error"

        @staticmethod
        def spoof():
            old_value = Spoofer.ProductId.get_value()
            new_value = "{}-{}-{}-{}".format(
                ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
                ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)))
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, "ProductId", 0, winreg.REG_SZ, new_value)
                    Spoofer.log_change("ProductId", old_value, new_value)
                    return True
            except Exception as e:
                print(f"[SPOOFER] Error modifying ProductId: {e}")
                return False

    class InstallationID:
        @staticmethod
        def spoof():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", 0, winreg.KEY_ALL_ACCESS) as key:
                    # Attempt to read the old InstallationID value. If it doesn't exist, use a placeholder.
                    try:
                        old_value, _ = winreg.QueryValueEx(key, "InstallationID")
                    except FileNotFoundError:
                        old_value = "Not Set"

                    newInstallationID = str(uuid.uuid4())
                    winreg.SetValueEx(key, "InstallationID", 0, winreg.REG_SZ, newInstallationID)
                    # Log the change of InstallationID.
                    Spoofer.log_change("InstallationID", old_value, newInstallationID)
                    return True
            except Exception as e:
                print(f"[SPOOFER] Error modifying InstallationID: {e}")
                return False

if __name__ == "__main__":
    Spoofer.MachineId.spoof()
    Spoofer.HardwareGUID.spoof()
    Spoofer.MachineGUID.spoof()
    Spoofer.EFIVariables.spoof()
    Spoofer.SystemInfo.spoof()
    Spoofer.SystemInfoExtended.spoof()
    Spoofer.ProductId.spoof()
    Spoofer.InstallationID.spoof()
