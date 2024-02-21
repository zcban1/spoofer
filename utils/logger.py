import os

def unisci_files_testo_in_spoofer_main(disk, file_output):
    # Cerca la cartella 'spoofer-main' nel disco specificato
    spoofer_main_path = None
    for root, dirs, files in os.walk(disk):
        if 'spoofer-main' in dirs:
            spoofer_main_path = os.path.join(root, 'spoofer-main')
            print(f"Trovata 'spoofer-main' in: {spoofer_main_path}")
            break

    # Verifica se 'spoofer-main' è stata trovata
    if spoofer_main_path is None:
        print("Cartella 'spoofer-main' non trovata.")
        return

    # Lista tutti i file di testo nella cartella 'spoofer-main'
    files_di_testo = [f for f in os.listdir(spoofer_main_path) if f.endswith('.txt')]

    # Verifica se ci sono file di testo
    if not files_di_testo:
        print("Nessun file di testo trovato nella cartella 'spoofer-main'.")
        return

    # Crea il percorso completo al file di output
    percorso_file_output = os.path.join(spoofer_main_path, file_output)

    # Unisce i file di testo
    with open(percorso_file_output, 'w') as output_file:
        for file_di_testo in files_di_testo:
            percorso_file_input = os.path.join(spoofer_main_path, file_di_testo)
            with open(percorso_file_input, 'r') as input_file:
                output_file.write(f"=== {file_di_testo} ===\n\n")
                output_file.write(input_file.read())
                output_file.write('\n\n')

    print(f"I file di testo nella cartella 'spoofer-main' sono stati uniti in '{percorso_file_output}'.")

    # Opzionale: Elimina i file originali dopo l'unione, tranne 'unificato.txt'
    for file_di_testo in files_di_testo:
        # Verifica che il file corrente non sia il file di output 'unificato.txt'
        if file_di_testo != file_output:  # Assicurati che 'file_output' contenga il nome del file di output, ad esempio 'unificato.txt'
            percorso_file_input = os.path.join(spoofer_main_path, file_di_testo)
            os.remove(percorso_file_input)
            print(f"File '{file_di_testo}' eliminato.")


# Esempio di utilizzo
disk = 'C:\\'  # Percorso per il disco C:
file_output = 'unificato.txt'
unisci_files_testo_in_spoofer_main(disk, file_output)



