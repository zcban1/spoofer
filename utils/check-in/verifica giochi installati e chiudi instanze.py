import os
import winreg as reg
import subprocess

def verifica_installazione_giochi():
    giochi_trovati = {
        "Valorant": False,
        "Fortnite": False,
        "Farlight84": False,
        "PUBG": False,
        "Rust": False,
        "Apex": False  # Assicurati che "Apex" si riferisca al gioco corretto, poiché Apex Legends solitamente si trova su Origin o Steam
    }

    # Percorso per Valorant
    percorso_valorant = "C:\\Riot Games"
    if os.path.exists(percorso_valorant) and "VALORANT" in os.listdir(percorso_valorant):
        giochi_trovati["Valorant"] = True

    # Percorso per i giochi installati tramite Epic Games
    percorso_epic_games = "C:\\Program Files\\Epic Games"  # Modifica se necessario
    if os.path.exists(percorso_epic_games):
        giochi_epic = os.listdir(percorso_epic_games)
        for gioco in ["Fortnite", "Farlight84","PUBG"]:
            if gioco in giochi_epic:
                giochi_trovati[gioco] = True

    # Percorso per i giochi installati tramite Steam
    percorso_steam = "C:\\Program Files (x86)\\Steam\\steamapps\\common"  # Modifica se hai librerie in percorsi diversi
    if os.path.exists(percorso_steam):
        giochi_steam = os.listdir(percorso_steam)
        for gioco in ["Rust", "Apex"]:  # Verifica il nome esatto della cartella per Apex Legends su Steam
            if gioco in giochi_steam:
                giochi_trovati[gioco] = True

    return giochi_trovati


def verifica_e_chiudi_giochi(giochi_trovati):
    for gioco, installato in giochi_trovati.items():
        if installato:
            # Converti il nome del gioco nel nome del processo.
            # Questi nomi di processo sono esempi e potrebbero non corrispondere.
            nome_processo = {
                "Valorant": "Valorant.exe",
                "Fortnite": "FortniteClient-Win64-Shipping.exe",
                "Farlight84": "Farlight84.exe",
                "Rust": "RustClient.exe",
                "Apex": "r5apex.exe"  # Nome processo per Apex Legends su Steam
            }.get(gioco)

            if nome_processo:
                try:
                    # Controlla se il processo è in esecuzione
                    processi = subprocess.check_output(f"tasklist | findstr /I {nome_processo}", shell=True)
                    if nome_processo in str(processi):
                        print(f"{gioco} è in esecuzione. Tentativo di chiusura.")
                        # Chiude il processo
                        subprocess.run(f"taskkill /F /IM {nome_processo}", shell=True, check=True)
                        print(f"{gioco} chiuso con successo.")
                except subprocess.CalledProcessError:
                    # Il processo non è in esecuzione o si è verificato un altro errore
                    print(f"{gioco} non è attualmente in esecuzione o non è stato possibile chiuderlo.")

# Esempio di utilizzo
giochi_installati = verifica_installazione_giochi()
for gioco, installato in giochi_installati.items():
    print(f"{gioco}: {'Installato' if installato else 'Non installato'}")
verifica_e_chiudi_giochi(giochi_installati)
