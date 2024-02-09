# Telegram client.

# AIOgram & Asyncio.
from aiogram import Bot, Dispatcher

from aiogram.types import Message, BotCommand, FSInputFile

from aiogram.filters.command import Command

from asyncio import run

# Generic remote-control imports.
from time import strftime

from platform import platform, system, release, version, architecture, processor

from screeninfo import get_monitors

from getpass import getuser

from subprocess import getoutput

from os import remove, startfile, sep

from os.path import exists, isfile, isdir

from glob import glob

from shutil import rmtree, make_archive, move as s_move

from socket import gethostname, gethostbyname

from keyboard import send, write

from mouse import click, move, RIGHT, LEFT, MIDDLE

from ctypes import windll

from threading import Thread

from pyscreeze import screenshot

from rebooter import Rebooter

from pymsgbox import alert

from pyperclip import copy

from playsound import playsound

from pywinctl import getActiveWindow

from pyautogui import press as pg_press

from cv2 import VideoCapture, imwrite

# PyInstaller (add-binary).
import sys


# Create net BotCommand utility.
def bot_command(command: str, description: str) -> BotCommand:
    return BotCommand(command=command, description=description)

# Help & about message.
help_msg = '''**Generic commands**:
/start - Start bot.
/help - Get help.
/about - Get about.

**System commands**:
/sysinfo - Get system information.
/syscom - Pass command to console and get output. Can cause TelegramBadRequest error if output is too big.

**Work with files**:
/insertfile (DIRECTORY) - Insert file into directory. After passing command you should send file you want to insert.
/getfile (FILE) - Get file by path.
/getdir (DIRECTORY) - Get directory as ZIP.
/dir (DIRECTORY) - Get directory content. Can cause TelegramBadRequest error if output is too big.
/exists (FILE/DIRECTORY) - Is file/directory exists.
/delete (FILE/DIRECTORY) - Delete file/directory.
/startfile (FILE) - Start file.

**Hardware (keyboard, mouse, monitor)**:
/sendkeys (KEYS) - Press keys. Hotkeys and multiple key pressing at once supported: `alt+tab,win+space`.
/type (TEXT) - Type text.
/mousebutton (BUTTON) - Click mouse button. Buttons: 1 - Right, 2 - Left, 3 - Middle.
/setmousepos (X) (Y) - Set cursor position.
/enablemonitor - Enable monitor. Very unstable.
/disablemonitor - Disable monitor. Very unstable.

**Screenshots**:
/screenshot - Make screenshot.

**Power**:
/shutdown - Shutdown PC.
/reboot - Reboot PC.

**Python**:
/evalpython (CODE(EXPRESSION)) - Evaluate Python expression. Can evaluate pretty big code if you can write one-liners.

**Time**:
/date - Get local PC date.

**Message Boxes**:
/msgbox [TITLE] [TEXT] - Show messsage box.

**Clipboard**:
/copy (TEXT) - Copy text to clipboard.

**Sounds**:
/playsound - Play sound from controller side. After passing command you should send MP3/WAV file to play sound.
/playlocalsound (PATH) - Play sound from client side.

**Windows**:
/getactivewindow - Get active window name, title, HWND.
/closeactivewindow - Close active window.

**Volume**:
/upvolume (AMOUNT) - Increase volume.
/downvolume (AMOUNT) - Decrease volume.

**Webcamera**:
/webcamimage (INDEX) - Capture image from web camera. Indexes start from 0 and end when all available web cameras end.

**Bot commands**:
/alive - Is bot alive.
/cancelloads - Cancel all file loads. Use it to cancel file loads after using `playsound`, or `insertfile`.

TRPCC V1.0 By xzripper.
'''

about_msg = '<a href="https://github.com/xzripper/trpcc">TRPCC</a> V1.0 By <a href="https://github.com/xzripper">xzripper</a>.'

# List of all available commands.
commands = [
    bot_command('/start', 'Start bot.'),
    bot_command('/help', 'Get all available commands.'),
    bot_command('/about', 'About TRPCC.'),
    bot_command('/sysinfo', 'Generic system information.'),
    bot_command('/syscom', 'Pass a command to console and get output (if there is any output).'),
    bot_command('/insertfile', 'Insert file into directory.'),
    bot_command('/getfile', 'Get file from client side by path.'),
    bot_command('/getdir', 'Get directory.'),
    bot_command('/dir', 'Get files in directory.'),
    bot_command('/exists', 'Does specified path exists.'),
    bot_command('/delete', 'Delete specified file/directory.'),
    bot_command('/startfile', 'Start file.'),
    bot_command('/sendkeys', 'Send keyboard keys.'),
    bot_command('/type', 'Type text.'),
    bot_command('/mousebutton', 'Click mouse button.'),
    bot_command('/setmousepos', 'Set cursor position.'),
    bot_command('/enablemonitor', 'Enable monitor.'),
    bot_command('/disablemonitor', 'Disable monitor.'),
    bot_command('/screenshot', 'Make a screenshot.'),
    bot_command('/shutdown', 'Shutdown PC.'),
    bot_command('/reboot', 'Reboot PC.'),
    bot_command('/evalpython', 'Evaluate Python code..'),
    bot_command('/date', 'Get PC date.'),
    bot_command('/copy', 'Copy text.'),
    bot_command('/msgbox', 'Show message box.'),
    bot_command('/playsound', 'Play sound from controller side.'),
    bot_command('/playlocalsound', 'Play sound from client side.'),
    bot_command('/getactivewindow', 'Get active window.'),
    bot_command('/closeactivewindow', 'Close active window.'),
    bot_command('/upvolume', 'Add volume.'),
    bot_command('/downvolume', 'Down volume.'),
    bot_command('/webcamimage', 'Capture image from web cam.'),
    bot_command('/alive', 'Is client side alive.'),
    bot_command('/cancelloads', 'Cancel all files load.'),
]

# Alert that bot is running.
alert('A1', 'A1')

# Get token.
_token_meipass = sys._MEIPASS + sep + 'TOKEN'

if not isfile(_token_meipass):
    alert('PyInstaller ERROR: Token is not included.', 'TRPCC::Client::Token')

    exit(1)

with open(_token_meipass, 'r') as _token:
    token = _token.read()

if token == '':
    alert('User ERROR: Missing token.', 'TRPCC::Client::Token')

    exit(1)

# Move to autostart.
_name_meipass = sys._MEIPASS + sep + 'NAME'

if not isfile(_name_meipass):
    alert('PyInstaller ERROR: Name is not included.', 'TRPCC::Client::Name')

    exit(1)

with open(_name_meipass, 'r') as _name:
    name = _name.read()

if name == '':
    alert('User ERROR: Missing name.', 'TRPCC::Client::Name')

    exit(1)

s_move(f'{name}.exe', f'C:\\Users\\{getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{name}.exe')

# Alert that bot is running.
alert('A2', 'A2')

# Initialize bot & dispatcher.
bot = Bot(token)

dp = Dispatcher()

# States.
_bot_waits_for_audio = [False]
_bot_waits_for_file = [False]

_file_path = [None]

# Start handler.
@dp.message(Command('start'))
async def start(message: Message) -> None:
    await bot.set_my_commands(commands)

    await bot.send_photo(message.from_user.id, 'https://github.com/xzripper/trpcc/blob/main/icon.png?raw=true', caption=f'🟢 TRPCC activated.\n\n✅ Client side connected.\n✅ Remote controller connected.\n\n<i>{strftime("%Yy %mm %dd %Hh %Mm %Ss")}</i> (client).\n\nType /help to get all commands.', parse_mode='HTML')

# Help handler.
@dp.message(Command('help'))
async def help_(message: Message) -> None:
    await bot.send_message(message.from_user.id, help_msg, parse_mode='Markdown')

# About handler.
@dp.message(Command('about'))
async def about(message: Message) -> None:
    await bot.send_message(message.from_user.id, about_msg, parse_mode='HTML')

# Generic system information.
@dp.message(Command('sysinfo'))
async def sysinfo(message: Message) -> None:
    try:
        monitor = [_monitor for _monitor in get_monitors() if _monitor.is_primary][0]

        info = f'''Client generic system information:
<pre>Platform: {platform()}
System: {system()}
System release: {release()}
System version: {version()}
System bits: {architecture()[0]}
System processor: {processor()}
Monitor information: X:{monitor.x} Y:{monitor.y} W:{monitor.width} WMM:{monitor.width_mm} H:{monitor.height} HMM:{monitor.height_mm} Name:{monitor.name} Primary:True
IP: {gethostbyname(gethostname())}
PC Username: {getuser()}
</pre>'''

        await bot.send_message(message.from_user.id, info, parse_mode='HTML')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `sysinfo` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Pass command to console.
@dp.message(Command('syscom'))
async def syscom(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/syscom [COMMAND] <- Missing command.')

            return

        await bot.send_message(message.from_user.id, f'Evaluating command and getting output...')

        output = getoutput(' '.join(args[1:]))

        await bot.send_message(message.from_user.id, f'Command output:\n`{output}`', parse_mode='Markdown')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `syscom` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Insert file into directory.
@dp.message(Command('insertfile'))
async def insertfile(message: Message) -> None:
    args = message.text.split()

    if len(args) <= 1:
        await bot.send_message(message.from_user.id, '/insertfile [PATH] <- Missing path.')

        return

    _file_path[0] = ' '.join(args[1:])

    if not exists(_file_path[0]):
        await bot.send_message(message.from_user.id, '❌ No specified path found.')

        return

    if _bot_waits_for_file[0]:
        await bot.send_message(message.from_user.id, '❌ Already waiting for file..')

        return

    _bot_waits_for_file[0] = True

    await bot.send_message(message.from_user.id, '❗ Send file.')

@dp.message(lambda message: message.document)
async def load_and_insert(message: Message) -> None: # Continuation of `insertfile`.
    try:
        if not _bot_waits_for_file[0]:
            await bot.send_message(message.from_user.id, '❌ Don\'t need file at this moment..')

            return

        sep = '' if _file_path[0].endswith('\\') or _file_path[0].endswith('/') else '/'

        path = f'{_file_path[0]}{sep}{message.document.file_name}'

        await bot.download(message.document.file_id, path)

        _bot_waits_for_file[0] = False

        _file_path[0] = None

        await bot.send_message(message.from_user.id, f'✅ Inserted {message.document.file_name} into {path}.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `insertfile` command (-> load_and_insert): `{str(exception.args)}` [{exception.__class__.__name__}].')

# Get file from client side by path.
@dp.message(Command('getfile'))
async def getfile(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/getfile [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await bot.send_message(message.from_user.id, '❌ Failed to find specified file by path.')

            return

        if not isfile(path):
            await bot.send_message(message.from_user.id, '❌ Expected file.')

            return

        await bot.send_document(message.from_user.id, FSInputFile(path))
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `getfile` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Get directory from client side by path.
@dp.message(Command('getdir'))
async def getdir(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/getfile [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await bot.send_message(message.from_user.id, '❌ Failed to find specified file by path.')

            return

        if not isdir(path):
            await bot.send_message(message.from_user.id, '❌ Expected directory.')

            return

        await bot.send_message(message.from_user.id, '🔃 Making archive from folder (may take few seconds).')

        make_archive('directory', 'zip', path)

        await bot.send_document(message.from_user.id, FSInputFile('directory.zip'))

        remove('directory.zip')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `getdir` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Get files in directory.
@dp.message(Command('dir'))
async def dir_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/dir [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await bot.send_message(message.from_user.id, '❌ Failed to find specified path.')

            return

        if not isdir(path):
            await bot.send_message(message.from_user.id, '❌ Expected directory.')

            return

        files = glob(path + '/*', recursive=True)

        await bot.send_message(message.from_user.id, '\n'.join(files))
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `dir` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Is file exists.
@dp.message(Command('exists'))
async def exists_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/exists [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        await bot.send_message(message.from_user.id, '✅ Exists.' if exists(path) else '❌ Not exists.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `exists` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Delete file/folder.
@dp.message(Command('delete'))
async def delete(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/delete [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await bot.send_message(message.from_user.id, '❌ Failed to find specified path.')

            return

        if isdir(path):
            rmtree(path)

        elif isfile(path):
            remove(path)

        await bot.send_message(message.from_user.id, f'✅ Tried to delete `{path}`.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `delete` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

@dp.message(Command('startfile'))
async def startfile_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/startfile [PATH] <- Missing path.')

            return

        path = ' '.join(args[1:])

        if not exists(path):
            await bot.send_message(message.from_user.id, '❌ Failed to find specified path.')

            return

        startfile(path)

        await bot.send_message(message.from_user.id, f'`{path}` started.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `startfile` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Press keyboard keys.
@dp.message(Command('sendkeys'))
async def sendkeys(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/sendkeys [KEYS] <- Missing keys.')

            return

        send(args[1])

        await bot.send_message(message.from_user.id, f'〽 Sending {args[1]}...')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `sendkeys` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Type text.
@dp.message(Command('type'))
async def type_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/type [TEXT] <- Missing text.')

            return

        await bot.send_message(message.from_user.id, f'〽 Typing {" ".join(args[1:])}...')

        write(' '.join(args[1:]))
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `type` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Click mouse button.
@dp.message(Command('mousebutton'))
async def mousebutton(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/mousebutton [BUTTON] <- Missing button.')

            return

        buttons = {'1': RIGHT, '2': LEFT, '3': MIDDLE}

        if args[1] in buttons:
            click(buttons[args[1]])

            await bot.send_message(message.from_user.id, f'✅ Clicked {buttons[args[1]]} button.')

        else:
            await bot.send_message(message.from_user.id, f'❌ Invalid button.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `mousebutton` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Click mouse button.
@dp.message(Command('setmousepos'))
async def setmousepos(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 2:
            await bot.send_message(message.from_user.id, '/setmousepos [X] [Y] <- Missing X or Y.')

            return

        if not args[1].isdigit() or not args[2].isdigit():
            await bot.send_message(message.from_user.id, '❌ Coordinates should be integer.')

            return

        move(int(args[1]), int(args[2]))

        await bot.send_message(message.from_user.id, f'✅ Moved cursor to {args[1]}, {args[2]}.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `setmousepos` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Enable monitor.
@dp.message(Command('enablemonitor'))
async def enablemonitor(message: Message) -> None:
    try:
        Thread(target=lambda: windll.user32.SendMessageW(65535, 274, 61808, -1)).start()

        await bot.send_message(message.from_user.id, '✅ Signal to enable monitor sent. [UNSTABLE].')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `enablemonitor` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Disable monitor.
@dp.message(Command('disablemonitor'))
async def disablemonitor(message: Message) -> None:
    try:
        Thread(target=lambda: windll.user32.SendMessageW(65535, 274, 61808, 2)).start()

        await bot.send_message(message.from_user.id, '✅ Signal to disable monitor sent. [UNSTABLE].')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `disablemonitor` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Make a screenshot.
@dp.message(Command('screenshot'))
async def screenshot_(message: Message) -> None:
    try:
        screenshot('trpcc_shot.png')

        await bot.send_photo(message.from_user.id, FSInputFile('trpcc_shot.png'))

        remove('trpcc_shot.png')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `screenshot` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Shutdown PC.
@dp.message(Command('shutdown'))
async def shutdown(message: Message) -> None:
    try:
        await bot.send_message(message.from_user.id, '✅ Shutdowning...')

        Rebooter('shutdown')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `shutdown` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Reboot PC.
@dp.message(Command('reboot'))
async def reboot(message: Message) -> None:
    try:
        await bot.send_message(message.from_user.id, '✅ Rebooting...')

        Rebooter()
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `reboot` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Evaluate Python code.
@dp.message(Command('evalpython'))
async def evalpython(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/evalpython [CODE] <- Missing code.')

            return

        await bot.send_message(message.from_user.id, 'Output: ' + str(eval(' '.join(args[1:]))))
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `evalpython` command: `{str(exception.args)}` [{exception.__class__.__name__}] (Error can happen while evaluating your code).')

# Get PC date.
@dp.message(Command('date'))
async def date(message: Message) -> None:
    await bot.send_message(message.from_user.id, strftime('Local PC Time:\n\n%Y.%m.%d/%H:%M:%S\n\nYear: %Y\nMonth: %m\nDay: %d\n\nHours: %H\nMinutes: %M\nSeconds: %S'))

# Show message box.
@dp.message(Command('msgbox'))
async def msgbox(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 2:
            await bot.send_message(message.from_user.id, '/msgbox [TEXT] [TITLE] <- Missing text or title.')

            return

        await bot.send_message(message.from_user.id, '✅ Showing message box...')

        Thread(target=lambda: alert(args[1], args[2])).start()
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `msgbox` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Copy text.
@dp.message(Command('copy'))
async def copy_(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/copy [TEXT] <- Missing text.')

            return

        copy(' '.join(args[1:]))

        await bot.send_message(message.from_user.id, '✅ Copied text successfully!')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `copy` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Play sound from controller side.
@dp.message(Command('playsound'))
async def playsound_(message: Message) -> None:
    if _bot_waits_for_audio[0]:
        await bot.send_message(message.from_user.id, '❌ Already waiting for audio..')

        return

    _bot_waits_for_audio[0] = True

    await bot.send_message(message.from_user.id, '❗ Send an MP3/WAV file.')

@dp.message(lambda message: message.audio)
async def load_and_play(message: Message) -> None: # Continuation of `playsound`.
    try:
        if not _bot_waits_for_audio[0]:
            await bot.send_message(message.from_user.id, '❌ Don\'t need audio at this moment..')

            return

        if message.audio.mime_type not in ['audio/mpeg', 'audio/wav']:
            await bot.send_message(message.from_user.id, '❌ Not MP3/WAV.')

            _bot_waits_for_audio[0] = False

            return

        await bot.download(message.audio.file_id, message.audio.file_name)

        playsound(message.audio.file_name, False)

        remove(message.audio.file_name)

        _bot_waits_for_audio[0] = False

        await bot.send_message(message.from_user.id, '✅ Playing sound...')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `playsound` command (-> load_and_play): `{str(exception.args)}` [{exception.__class__.__name__}].')

# Play sound from client side.
@dp.message(Command('playlocalsound'))
async def playlocalsound(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/playlocalsound [SOUND] <- Missing sound.')

            return

        path = ' '.join(args[1:])

        if not path.endswith('.mp3') and not path.endswith('.wav'):
            await bot.send_message(message.from_user.id, '❌ MP3/WAV required.')

            return

        if not exists(path):
            await bot.send_message(message.from_user.id, '❌ Failed to find specified audio.')

            return

        playsound(path, False)

        await bot.send_message(message.from_user.id, '✅ Playing sound...')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `playlocalsound` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Get active window.
@dp.message(Command('getactivewindow'))
async def get_active_window(message: Message) -> None:
    try:
        active_window = getActiveWindow()

        await bot.send_message(message.from_user.id, f'〽 Active window: {active_window.getAppName()} "{active_window.title}" (HWND: {active_window._hWnd}).')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `getactivewindow` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Close active window.
@dp.message(Command('closeactivewindow'))
async def close_active_window(message: Message) -> None:
    try:
        active_window = getActiveWindow()

        title = f'{active_window.getAppName()} "{active_window.title}"'

        active_window.close()

        await bot.send_message(message.from_user.id, f'〽 Closing {title}...')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `getactivewindow` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Up volume.
@dp.message(Command('upvolume'))
async def upvolume(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/upvolume [AMOUNT] <- Missing amount.')

            return

        if not args[1].isdigit():
            await bot.send_message(message.from_user.id, '❌ Expected amount as a digit.')

            return

        for _ in range(int(args[1])):
            pg_press('volumeup')

        await bot.send_message(message.from_user.id, f'✅ Volume increased by {args[1]}.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `upvolume` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Down volume.
@dp.message(Command('downvolume'))
async def downvolume(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/downvolume [AMOUNT] <- Missing amount.')

            return

        if not args[1].isdigit():
            await bot.send_message(message.from_user.id, '❌ Expected amount as a digit.')

            return

        for _ in range(int(args[1])):
            pg_press('volumedown')

        await bot.send_message(message.from_user.id, f'✅ Volume decreased by {args[1]}.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `downvolume` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Capture image from web cam.
@dp.message(Command('webcamimage'))
async def webcamimage(message: Message) -> None:
    try:
        args = message.text.split()

        if len(args) <= 1:
            await bot.send_message(message.from_user.id, '/webcamimage [WEBCAMINDEX] <- Missing webcam index.')

            return

        if not args[1].isdigit():
            await bot.send_message(message.from_user.id, '❌ Expected index as a digit.')

            return

        await bot.send_message(message.from_user.id, 'Capturing image...')

        camera = VideoCapture(int(args[1]))

        result, image = camera.read()

        if result:
            imwrite('webcam.png', image)

            await bot.send_photo(message.from_user.id, FSInputFile('webcam.png'))

            remove('webcam.png')

        else:
            await bot.send_message(message.from_user.id, '❌ No image detected. Try other webcam index.')
    except Exception as exception:
        await bot.send_message(message.from_user.id, f'Failed to evaluate `webcamimage` command: `{str(exception.args)}` [{exception.__class__.__name__}].')

# Is bot alive.
@dp.message(Command('alive'))
async def alive(message: Message) -> None:
    await bot.send_message(message.from_user.id, '✅ Alive.')

@dp.message(Command('cancelloads'))
async def cancelloads(message: Message) -> None:
    _bot_waits_for_audio[0] = False
    _bot_waits_for_file[0] = False

    _file_path[0] = None

    await bot.send_message(message.from_user.id, '✅ Cancelled all file loads!')

# Main function.
async def main():
    await dp.start_polling(bot)

# Run.
if __name__ == '__main__':
    run(main())
