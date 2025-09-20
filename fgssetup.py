import os
import time
import colorama
from os import system
from colorama import Fore, Back, Style

# Inicializar colorama
colorama.init(autoreset=True)

print(Fore.CYAN + Style.BRIGHT + "fGs Kali Setup")
print(Fore.YELLOW + "This program is a fast setup tool for Kali")
time.sleep(0.5)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def mainpage():
 while True:
    clear()
    print(Fore.GREEN + "=== Main Menu ===")
    print(Fore.CYAN + "1 - Kali fGs ZSH Setup  | ~/.zshrc | after installation change static username in config file |")
    print(Fore.CYAN + "2 - GNOME Environment Install")
    print(Fore.CYAN + "3 - Set Clean Wallpaper")
    print(Fore.CYAN + "4 - Exit")
    
    escolhamainpage = input(Fore.YELLOW + "Choose an option: ")
    
    if escolhamainpage == "1":
        print(Fore.MAGENTA + "Ok! Starting ZSH setup...")
        print(Fore.RED + "AFTER INSTALLING THE CONFIG FILE IS IN ~/.zshrc")  
        time.sleep(0.5)
        clear()
        os.system("sudo apt update && sudo apt upgrade -y")
        os.system("sudo apt install -y zsh")
        os.system("sudo apt install -y fastfetch")
        os.system("wget -O ~/.zshrc https://github.com/xFGss/Kali-easy-setup/releases/download/v1.0/zshrc.backup.2025-09-19-2354")
        os.system("wget -P ~/.local/share/fonts https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/FiraCode.zip \
&& cd ~/.local/share/fonts \
&& unzip FiraCode.zip \
&& rm FiraCode.zip \
&& fc-cache -fv")
        escolhareboot = input(Fore.YELLOW + "Installation Completed, Reboot now? (y/n): ")
        if escolhareboot.lower() == "y":
            os.system("reboot")
        else:
            input(Fore.GREEN + "Press ENTER to return to main menu...")
            mainpage()
        
    elif escolhamainpage == "2":
        print(Fore.MAGENTA + "Ok, we are gonna setup GNOME Desktop Environment")
        print(Fore.CYAN + "Click ENTER always in first option unless you know what your doing.")
        print(Fore.YELLOW + "Please Wait...")
        time.sleep(1)
        clear()
        os.system("sudo apt update && sudo apt upgrade -y")
        os.system("sudo apt install -y kali-desktop-gnome")
        escolhareboot = input(Fore.YELLOW + "Installation Completed, Reboot now? (y/n): ")
        if escolhareboot.lower() == "y":
            os.system("reboot")    
        input(Fore.GREEN + "Installation Completed, Press ENTER to return to main menu")
        mainpage()

    elif escolhamainpage == "3":
        os.system("wget -O ~/Documents/Wallpaper.jpg https://github.com/xFGss/Kali-easy-setup/releases/download/v1.0/A9OdSK.jpg")
        os.system("gsettings set org.gnome.desktop.background picture-uri 'file://$HOME/Documents/Wallpaper.jpg'")

    elif escolhamainpage == "4":
        print(Fore.RED + "Exiting the program...")
        break

    else:
        print(Fore.RED + "Invalid Option")
        time.sleep(1)
        mainpage()


mainpage()
