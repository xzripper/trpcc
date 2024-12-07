# TRPCC Dependencies installer.

from os import system

from trpcc_utils import styled, Fore

def install_deps():
    print(styled('TRPCC Dependencies Installer: ', Fore.LIGHTWHITE_EX, bold=True) + 'Installing dependencies...')

    system('pip3 install pyinstaller aiogram colorama \
           keyboard mouse pyperclip \
           playsound==1.2.2 screeninfo pyscreeze \
           pymsgbox pywinctl pyautogui \
           opencv-python psutil getmac')

    print(styled('TRPCC Dependencies Installer: ', Fore.LIGHTWHITE_EX, bold=True) + 'Finished dependencies installation.')

if __name__ == '__main__':
    install_deps()
