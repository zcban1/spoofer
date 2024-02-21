import os
import subprocess
import win32gui
import win32con
import time
import pyautogui
import random
import pyperclip
import keyboard

def enum_windows_callback(hwnd, param):
    print(win32gui.GetWindowText(hwnd))

# Function to generate a random 8-character combination of uppercase letters [A, B, C, D, E]
def generate_random_combination():
    return ''.join(random.choice('ABC') for _ in range(9))

def generate_random_combination2():
    return ''.join(random.choice('1234567890') for _ in range(6))

def generate_random_combination3():
    return ''.join(random.choice('ABCDEFG1234567890') for _ in range(12))

# Ottieni il percorso della cartella in cui si trova questo script
script_folder_path = os.path.dirname(os.path.abspath(__file__))
cru_folder_path = os.path.join(script_folder_path, "cru-1.5.2")

# Verifica che la cartella esista
if os.path.exists(cru_folder_path):
    # Avvia l'eseguibile D
    executable_path = os.path.join(cru_folder_path, "CRU.exe")
    if os.path.exists(executable_path):
        subprocess.Popen(executable_path)

        # Attendi un po' per dare tempo all'eseguibile di avviarsi
        time.sleep(1)

        #id 
        pyautogui.click(x=1055, y=320)
        pyautogui.click(button='right',x=965, y=387)
        pyautogui.click(x=1018, y=520)
        # Generate a random 8-character combination of uppercase letters [A, B, C, D, E]
        random_combination = generate_random_combination()
        time.sleep(0.1)
        # Simulate typing the random combination
        keyboard.write(random_combination)
        # Copy the generated combination to the clipboard
        pyperclip.copy(random_combination)


        #id serial
        pyautogui.click(x=1008, y=411)
        pyautogui.click(button='right',x=1008, y=411)
        pyautogui.click(x=1046, y=554)
        random_combination = generate_random_combination2()
        keyboard.write(random_combination)
        pyperclip.copy(random_combination)


        #id serial
        pyautogui.click(x=928, y=546)
        pyautogui.click(button='right',x=928, y=546)
        pyautogui.click(x=991, y=688)
        random_combination = generate_random_combination3()
        keyboard.write(random_combination)
        pyperclip.copy(random_combination)

        #OK
        pyautogui.click(x=914, y=725)
        pyautogui.click(x=1085, y=790)


# Ottieni il percorso della cartella in cui si trova questo script
script_folder_path = os.path.dirname(os.path.abspath(__file__))
cru_folder_path = os.path.join(script_folder_path, "cru-1.5.2")

# Verifica che la cartella esista
if os.path.exists(cru_folder_path):
    # Avvia l'eseguibile D
    executable_path = os.path.join(cru_folder_path, "restart64.exe")
    if os.path.exists(executable_path):
        subprocess.Popen(executable_path)

        time.sleep(5)

        pyautogui.click(x=945, y=571)
        
        



        
