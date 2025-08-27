import os
import sys
import time
import threading
import subprocess
import keyboard
import msvcrt
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)

# ======== CONFIG =========
BUFFER_TIMEOUT = 0.5  # seconds to wait for multi-digit input
number_buffer = ""
buffer_timer = None
buffer_lock = threading.Lock()
menu_lock = threading.Lock()  # protege desenho do menu contra input simultâneo

# ======== APPS =========
apps = [
    {"id": 1, "name": "Google Chrome", "cmd": "winget install Google.Chrome", "selected": False},
    {"id": 2, "name": "Visual Studio Code", "cmd": "winget install Microsoft.VisualStudioCode", "selected": False},
    {"id": 3, "name": "WinRAR", "cmd": "winget install RARLab.WinRAR", "selected": False},
    {"id": 4, "name": "Spotify", "cmd": "winget install Spotify.Spotify", "selected": False},
    {"id": 5, "name": "Discord", "cmd": "winget install Discord.Discord", "selected": False},
    {"id": 6, "name": "Minecraft Launcher", "cmd": "winget install Mojang.MinecraftLauncher", "selected": False},
    {"id": 7, "name": "Lunar Client", "cmd": "winget install Moonsworth.LunarClient", "selected": False},
    {"id": 8, "name": "Steam", "cmd": "winget install Valve.Steam", "selected": False},
    {"id": 9, "name": "Epic Games Launcher", "cmd": "winget install EpicGames.EpicGamesLauncher", "selected": False},
    {"id": 10, "name": "Java Runtime Environment", "cmd": "winget install Oracle.JavaRuntimeEnvironment", "selected": False},
    {"id": 11, "name": "XAMPP", "cmd": "winget install ApacheFriends.Xampp.8.2", "selected": False},
    {"id": 12, "name": "HeidiSQL", "cmd": "winget install HeidiSQL.HeidiSQL", "selected": False},
    {"id": 13, "name": "Burp Suite Community Edition", "cmd": "winget install PortSwigger.BurpSuite.Community", "selected": False},
    {"id": 14, "name": "AnyDesk", "cmd": "winget install AnyDesk.AnyDesk", "selected": False},
]

# ======== FUNÇÕES ========
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading_animation():
    symbols = ['|', '/', '-', '\\']
    print("\nLoading fGs Easy Reboot...\n")
    for _ in range(6):
        for s in symbols:
            sys.stdout.write("\r" + Fore.CYAN + s + Style.RESET_ALL)
            sys.stdout.flush()
            time.sleep(0.1)
    clear()

def print_menu():
    with menu_lock:  # protege contra input simultâneo
        clear()
        print(Fore.CYAN + "="*50)
        print(Fore.CYAN + "      fGs Easy Reboot - App Installer")
        print(Fore.CYAN + "="*50 + Style.RESET_ALL)
        print("\nSelect the apps you want to install:\n")

        # alinhar colunas
        id_width = 2
        name_width = 30
        status_width = 12

        for i, app in enumerate(apps):
            status = Fore.GREEN + "SELECTED" if app["selected"] else Fore.RED + "UNSELECTED"
            text = f"[{app['id']:<{id_width}}] {app['name']:<{name_width}} ({status}{Style.RESET_ALL})"
            print(text, end="\t")
            if (i + 1) % 3 == 0:
                print()
        print("\n\nPress the number keys to select/deselect apps (multi-digit supported)")
        print("Press 'I' to install selected apps | Press 'Q' to quit")
        if number_buffer:
            print(Fore.CYAN + f"\nTyping: {number_buffer}" + Style.RESET_ALL)

def process_buffer():
    global number_buffer, buffer_timer
    with buffer_lock:
        if number_buffer:
            try:
                num = int(number_buffer)
                for app in apps:
                    if app["id"] == num:
                        app["selected"] = not app["selected"]
                        break
            except ValueError:
                pass
            number_buffer = ""
            buffer_timer = None
    print_menu()  # já está protegido por menu_lock

def handle_key(key):
    global number_buffer, buffer_timer
    with buffer_lock:
        number_buffer += key
        if buffer_timer:
            buffer_timer.cancel()
            buffer_timer = None

        ids_as_str = [str(app["id"]) for app in apps]
        need_wait = any(s.startswith(number_buffer) and len(s) > len(number_buffer) for s in ids_as_str)

        if need_wait:
            buffer_timer = threading.Timer(BUFFER_TIMEOUT, process_buffer)
            buffer_timer.daemon = True
            buffer_timer.start()
        else:
            threading.Thread(target=process_buffer, daemon=True).start()

    print_menu()  # protegido por menu_lock

def run_installation(cmd):
    finished = [False]
    def run_cmd():
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for _ in proc.stdout:
            pass
        proc.wait()
        finished[0] = True
    threading.Thread(target=run_cmd, daemon=True).start()
    return finished

def install_apps():
    with menu_lock:  # bloquear input enquanto instala
        clear()
        selected = [app for app in apps if app["selected"]]
        if not selected:
            print(Fore.YELLOW + "No apps selected for installation." + Style.RESET_ALL)
            time.sleep(2)
            return

        print("Installing selected apps...\n")
        for app in selected:
            print(f"> Installing {app['name']}...")
            finished = run_installation(app["cmd"])
            with tqdm(total=100, desc=f"Installing {app['name']}", unit="%", ncols=80) as bar:
                current = 0
                step = 1
                cap_before_done = 95
                while not finished[0]:
                    if current < cap_before_done:
                        bar.update(step)
                        current += step
                    time.sleep(0.05)
                if current < 100:
                    bar.update(100 - current)
            print(Fore.GREEN + f"{app['name']} installed successfully!\n" + Style.RESET_ALL)
            time.sleep(0.5)
        print(Fore.GREEN + "All installations completed!" + Style.RESET_ALL)
        input("\nPress ENTER to return to the menu...")

    print_menu()

# ======== MAIN LOOP ========
def main():
    global number_buffer
    clear()
    loading_animation()
    keyboard.press_and_release("F11")
    print_menu()  # primeira vez

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8', errors='ignore')
            if key.lower() == 'q':
                break
            elif key.lower() == 'i':
                install_apps()
            elif key.isdigit():
                handle_key(key)

if __name__ == "__main__":
    main()
