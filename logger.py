import os

def unisci_files_testo(cartella_input, file_output):
    # Ottiene il percorso corrente di lavoro
    percorso_corrente = os.getcwd()

    # Unisce il percorso corrente con la cartella di input
    percorso_cartella_input = os.path.join(percorso_corrente, cartella_input)

    # Verifica se la cartella di input esiste
    if not os.path.exists(percorso_cartella_input):
        print(f"La cartella '{cartella_input}' non esiste.")
        return

    # Lista tutti i file nella cartella di input
    files_di_testo = [f for f in os.listdir(percorso_cartella_input) if f.endswith('.txt')]

    # Verifica se ci sono file di testo nella cartella
    if not files_di_testo:
        print(f"Nessun file di testo trovato nella cartella '{cartella_input}'.")
        return

    # Unisce il percorso corrente con il percorso del file di output
    percorso_file_output = os.path.join(percorso_cartella_input, file_output)

    # Apre il file di output in modalità scrittura
    with open(percorso_file_output, 'w') as output_file:
        # Cicla attraverso tutti i file di testo nella cartella
        for file_di_testo in files_di_testo:
            # Crea il percorso completo del file di input
            percorso_file_input = os.path.join(percorso_cartella_input, file_di_testo)

            # Apre il file di input in modalità lettura
            with open(percorso_file_input, 'r') as input_file:
                # Scrive il nome del file come separatore
                output_file.write(f"=== {file_di_testo} ===\n\n")
                
                # Legge il contenuto del file di input e lo scrive nel file di output
                output_file.write(input_file.read())

                # Aggiunge una linea vuota come separatore tra i file
                output_file.write('\n\n')

    print(f"I file di testo nella cartella '{cartella_input}' sono stati uniti con successo in '{percorso_file_output}'.")
    
    # Elimina i file originali
    for file_di_testo in files_di_testo:
        percorso_file_input = os.path.join(percorso_cartella_input, file_di_testo)
        os.remove(percorso_file_input)
        print(f"File '{file_di_testo}' eliminato.")

# Esempio di utilizzo con percorsi relativi
cartella_input = os.path.dirname(os.path.abspath(__file__))
file_output = 'unificato.txt'

unisci_files_testo(cartella_input, file_output)

