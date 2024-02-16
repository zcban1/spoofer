import winreg
import random
import subprocess
import sys

class DualLogger:
    def __init__(self, filepath, mode='w'):
        self.terminal = sys.stdout
        self.log = open(filepath, mode)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # Questo è necessario perché sys.stdout ha un metodo flush() che può essere chiamato internamente
        self.terminal.flush()
        self.log.flush()

class Spoofer:
    class NTaddress:
        regeditPath = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0001"
        key = "NetworkAddress"

        @staticmethod
        def get_value():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Spoofer.NTaddress.regeditPath) as key:
                    value, _ = winreg.QueryValueEx(key, Spoofer.NTaddress.key)
                    return str(value)
            except:
                return "ERR"

        @staticmethod
        def set_value(value):
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Spoofer.NTaddress.regeditPath, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, Spoofer.NTaddress.key, 0, winreg.REG_SZ, value)
                    return True
            except:
                return False

        @staticmethod
        def spoof():
            old_value = Spoofer.NTaddress.get_value()
            parts = old_value.split("-")
            new_parts = parts[:3]
            new_parts.extend("".join(random.choice('0123456789ABCDEF') for _ in range(2)) for _ in range(3))
            new_value = "-".join(new_parts)
            result = Spoofer.NTaddress.set_value(new_value)

            if result:
                print("[SPOOFER] NTaddress Changed from", old_value, "to", new_value)
            else:
                print("[SPOOFER] Error accessing the Registry... Maybe run as admin")

            return result

    class NewInfo:
        regeditPath = r"SYSTEM\ControlSet001\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}\0001"
        value_name = "NetworkAddress"

        @staticmethod
        def key_exists():
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Spoofer.NewInfo.regeditPath) as key:
                    _, _ = winreg.QueryValueEx(key, Spoofer.NewInfo.value_name)
                    return True
            except:
                return False

        @staticmethod
        def create_value(value_data):
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, Spoofer.NewInfo.regeditPath, 0, winreg.KEY_WRITE) as key:
                    winreg.SetValueEx(key, Spoofer.NewInfo.value_name, 0, winreg.REG_SZ, value_data)
                    return True
            except:
                return False

def restart_network_interface(interface_name):
    try:
        subprocess.check_call(f"netsh interface set interface \"{interface_name}\" admin=disable", shell=True)
        subprocess.check_call(f"netsh interface set interface \"{interface_name}\" admin=enable", shell=True)
        print(f"Interfaccia di rete {interface_name} riavviata con successo.")
    except subprocess.CalledProcessError as e:
        print(f"Errore nel riavvio dell'interfaccia di rete: {e}")


if __name__ == "__main__":
    sys.stdout = DualLogger("Nmac_log.txt")
    sys.stderr = sys.stdout  # Reindirizza anche stderr al nostro DualLogger

    if not Spoofer.NewInfo.key_exists():
        try:
            getmac_output = subprocess.check_output(["getmac"]).decode("utf-8")
            mac_address = getmac_output.split("\n")[3].split()[0]
            if Spoofer.NewInfo.create_value(mac_address):
                print(f"Custom network address value created with MAC address: {mac_address}")
            else:
                print("Failed to create custom network address value.")
        except subprocess.CalledProcessError:
            print("Failed to retrieve MAC address using getmac.")
    else:
        print("Custom network address value already exists.")

    # Prova a spoofare l'indirizzo MAC
    Spoofer.NTaddress.spoof()
    ##restart interfaces
    interface_name = "Ethernet"  # Sostituisci con il nome effettivo della tua interfaccia
    restart_network_interface(interface_name)
