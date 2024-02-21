import tkinter as tk
from tkinter import scrolledtext, font as tkfont
import subprocess

class App:
    def __init__(self, root):
        self.root = root
        root.title("Automazione Script")
        root.configure(bg='#334257')  # Sfondo della finestra principale

        # Definizione dei font
        self.button_font = tkfont.Font(family="Helvetica", size=8, weight="bold")
        self.text_font = tkfont.Font(family="Consolas", size=10)

        # Percorso della cartella utils
        self.utils_path = "utils/"  # Assicurati che questo percorso sia corretto

        self.create_widgets()

    def run_command(self, command):
        # Aggiunge il percorso della cartella 'utils' al comando
        command_with_path = f"python {self.utils_path}{command}"
        try:
            result = subprocess.run(command_with_path, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
            output = result.stdout if result.stdout else "Completato senza output."
            error = result.stderr if result.stderr else ""
        except subprocess.CalledProcessError as e:
            output = f"Errore durante l'esecuzione: {e.output}"
            error = e.stderr
        self.txt_output.insert(tk.END, f"{command}: {output}\n{error}\n")
        self.txt_output.see(tk.END)

    def create_widgets(self):
        # Frame per l'output a sinistra
        self.frame_output = tk.Frame(self.root, bg='#334257')
        self.frame_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Area di testo con stile personalizzato
        self.txt_output = scrolledtext.ScrolledText(self.frame_output, font=self.text_font, bg='#1E2022', fg='white')
        self.txt_output.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Frame per i pulsanti a destra
        self.frame_buttons = tk.Frame(self.root, bg='#334257')
        self.frame_buttons.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        # Pulsanti per eseguire i comandi singolarmente
        commands = [
            ("Get Serial Number Report", "GetSerial.py"),
            ("Spoof Regedit Win", "foxtrot.py"),
            ("Spoof Volumedisk", "volumedisk.py"),
            ("Spoof Mac-Address", "NmacV2.py"),
            ("SPOOF BIOS AMI", "BIOSAMI.py"),
            ("Clean Win", "ResetCleanV2.py"),
            ("Clean Old Device", "deviceclean.py"),
            ("Clean Old Drive", "driveclean.py"),
        ]

        for text, command in commands:
            button = tk.Button(self.frame_buttons, text=text, command=lambda cmd=command: self.run_command(cmd),
                               font=self.button_font, bg='#476072', fg='white', activebackground='#7A9E9F', relief=tk.RAISED)
            button.pack(pady=2, fill=tk.X)  # Usa fill=tk.X per adattare i pulsanti alla larghezza del frame

        # Pulsante Spoof All e Chiudi
        tk.Button(self.frame_buttons, text="Spoof All", command=self.run_all_commands, font=self.button_font,
                  bg='#FF4C29', fg='white', activebackground='#FF6C4F', relief=tk.RAISED).pack(fill=tk.X, pady=(5, 2))
        tk.Button(self.frame_buttons, text="Chiudi", command=self.root.destroy, font=self.button_font, bg='#FF4C29',
                  fg='white', activebackground='#FF6C4F', relief=tk.RAISED).pack(fill=tk.X)

    def run_all_commands(self):
        commands = [
            "GetSerial.py",
            "foxtrot.py",
            "volumedisk.py",
            "NmacV2.py",
            "BIOSAMI.py",
            "ResetCleanV2.py",
            "deviceclean.py",
            "driveclean.py",
            "logger.py",
            "RestartWin.py",
        ]
        for command in commands:
            self.run_command(command)

def main():
    root = tk.Tk()
    app = App(root)
    root.geometry("800x500")  # Ajusted la dimensione per un layout ottimizzato
    root.mainloop()

if __name__ == "__main__":
    main()

