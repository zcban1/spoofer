import random
import string
import subprocess

def generate_random_name(length=12):
    charset = string.ascii_letters + string.digits
    return ''.join(random.choice(charset) for _ in range(length))

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode().strip()
    except subprocess.CalledProcessError as e:
        return e.stderr.decode().strip()

# Ottieni il nome corrente del computer
current_computer_name_command = "wmic computersystem get name"
current_computer_name = execute_command(current_computer_name_command).split('\n')[1]

# Ottieni il nome utente corrente
current_user_name_command = "whoami"
current_user_name = execute_command(current_user_name_command).split('\\')[-1]

new_computer_name = generate_random_name()
new_user_name = generate_random_name()

# Rinomina il computer
rename_computer_command = f"wmic computersystem where name='{current_computer_name}' rename {new_computer_name}"
computer_rename_result = execute_command(rename_computer_command)

# Rinomina l'account utente
rename_user_command = f"wmic useraccount where name='{current_user_name}' rename {new_user_name}"
user_rename_result = execute_command(rename_user_command)

print(f"Vecchio nome del computer: {current_computer_name}")
print(f"Nuovo nome del computer: {new_computer_name}")
print(f"Vecchio nome utente: {current_user_name}")
print(f"Nuovo nome utente: {new_user_name}")

# Scrivi i nomi vecchi e nuovi e i risultati dei comandi in un file di testo
with open("nuovi_nomi.txt", "w") as file:
    file.write(f"Vecchio nome del computer: {current_computer_name}\n")
    file.write(f"Nuovo nome del computer: {new_computer_name}\n")
    file.write(f"Vecchio nome utente: {current_user_name}\n")
    file.write(f"Nuovo nome utente: {new_user_name}\n")
    file.write(f"Risultato rinomina computer: {computer_rename_result}\n")
    file.write(f"Risultato rinomina utente: {user_rename_result}\n")
