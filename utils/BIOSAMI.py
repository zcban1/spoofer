import os
import subprocess
import random
import tempfile

def generate_random_digits(length=15):
    # Genera una stringa di 'length' cifre casuali
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)
    return None

def create_and_run_batch_file(directory, commands):
    # Verifica se la directory esiste
    if not os.path.isdir(directory):
        print(f"La cartella '{directory}' non esiste.")
        return

    # Cambia la directory corrente
    os.chdir(directory)

    # Crea un file batch temporaneo
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.bat', dir=directory) as batch_file:
        for command in commands:
            batch_file.write(command + "\n")
        # Aggiungi un comando per chiudere il cmd alla fine
        batch_file.write("exit\n")
        batch_file_path = batch_file.name

    # Funzione per eliminare il file batch dopo l'esecuzione
    def delete_temp_batch():
        os.remove(batch_file_path)

    # Esegui il file batch e chiudi il cmd dopo l'esecuzione
    process = subprocess.Popen(["cmd", "/C", batch_file_path], close_fds=True)
    process.wait()  # Aspetta che il processo cmd finisca
    delete_temp_batch()  # Elimina il file batch

file_to_find = "AMIDEWINx64.EXE"
starting_path = "C:\\"  # Cambia questo percorso se vuoi iniziare la ricerca in un'altra posizione

path_to_file = find_file(file_to_find, starting_path)

if path_to_file:
    print(f"Trovato {file_to_find} in {path_to_file}")
    path_to_directory = os.path.dirname(path_to_file)

    # Genera le combinazioni casuali
    random_digits_SS = generate_random_digits()
    random_digits_BS = generate_random_digits()
    random_digits_CS = generate_random_digits()
    random_digits_PSN = generate_random_digits()

    # Comandi da eseguire nel cmd
    commands_to_run = [
        "AMIDEWINx64.EXE /ALL PreLog.txt",
        "AMIDEWINx64.EXE /SU AUTO",
        f"AMIDEWINx64.EXE /SS {random_digits_SS}",
        f"AMIDEWINx64.EXE /BS {random_digits_BS}",
        f"AMIDEWINx64.EXE /CS {random_digits_CS}",
        f"AMIDEWINx64.EXE /PSN {random_digits_PSN}",
        "AMIDEWINx64.EXE /ALL PostLog.txt",
    ]

    # Crea ed esegui il file batch
    create_and_run_batch_file(path_to_directory, commands_to_run)

    print("/SS generata:", random_digits_SS)
    print("/SU generata:", random_digits_SS)
    print("/BS generata:", random_digits_BS)
    print("/CS generata:", random_digits_CS)
    print("/PSN generata:", random_digits_PSN)
else:
    print(f"{file_to_find} non trovato.")



