# TRPCC Utilities.

from colorama import Fore, Style

from os import system

from platform import system as ps


ICON = '''▄▄▄█████▓ ██▀███   ██▓███   ▄████▄   ▄████▄  
▓  ██▒ ▓▒▓██ ▒ ██▒▓██░  ██▒▒██▀ ▀█  ▒██▀ ▀█  
▒ ▓██░ ▒░▓██ ░▄█ ▒▓██░ ██▓▒▒▓█    ▄ ▒▓█    ▄ 
░ ▓██▓ ░ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒▓▓▄ ▄██▒▒▓▓▄ ▄██▒
  ▒██▒ ░ ░██▓ ▒██▒▒██▒ ░  ░▒ ▓███▀ ░▒ ▓███▀ ░
  ▒ ░░   ░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ░▒ ▒  ░░ ░▒ ▒  ░
    ░      ░▒ ░ ▒░░▒ ░       ░  ▒     ░  ▒   
  ░        ░░   ░ ░░       ░        ░        
            ░              ░ ░      ░ ░      
                           ░        ░'''

def styled(string: str, color: int, bg: int=None, bold: bool=False) -> None:
  return f'{Style.BRIGHT if bold else ""}{color}{bg if bg else ""}{string}{Style.RESET_ALL}'

def print_icon() -> None:
    print('\n' + styled(ICON, Fore.RED, None, True))

def clrscr():
    system('cls' if ps() == 'Windows' else 'clear')
