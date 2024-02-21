import os
import winreg as reg
import subprocess


def elimina_txt_in_spoofer_main(disk):
    """
    Cerca ricorsivamente la cartella 'spoofer-main' in tutto il disco specificato e
    elimina tutti i file .txt trovati direttamente all'interno di quella cartella, senza
    toccare i file nelle sottocartelle.

    Args:
    disk (str): Il percorso del disco da scansionare, es: 'C:\\'.
    """
    for root, dirs, files in os.walk(disk):
        if 'spoofer-main' in dirs:
            spoofer_main_path = os.path.join(root, 'spoofer-main')
            print(f"Trovata 'spoofer-main' in: {spoofer_main_path}")
            
            # Ottiene solo i file direttamente all'interno di 'spoofer-main'
            for item in os.listdir(spoofer_main_path):
                full_item_path = os.path.join(spoofer_main_path, item)
                if os.path.isfile(full_item_path) and item.endswith('.txt'):
                    try:
                        os.remove(full_item_path)
                        print(f"File {full_item_path} eliminato con successo.")
                    except Exception as e:
                        print(f"Impossibile eliminare {full_item_path}: {e}")


# Esempio di chiamata della funzione:
elimina_txt_in_spoofer_main('C:\\')






