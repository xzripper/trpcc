# Utilities.

from colorama import Fore, Back, Style


CENTER = '\t\t\t'

def styled(string: str, color: int, bg: int=None, bold: bool=False) -> None:
    return f'{Style.BRIGHT if bold else ""}{color}{bg if bg else ""}{string}{Fore.WHITE}{Back.BLACK if bg else ""}{Style.RESET_ALL if bold else ""}'

def print_icon() -> None:
    with open('generic/icon', 'r') as _icon:
        print(styled(_icon.read(), Fore.RED, None, True))
