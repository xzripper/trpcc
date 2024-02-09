# https://github.com/gladykov/rebooter/blob/master/rebooter/__init__.py
# Rebooter LICENSE: <<Do whatever you want to do with it>>.
# Optimized it.

#!/usr/bin/env python
from subprocess import check_output, STDOUT
from sys import platform

def isMac():
  """Are we on mac?"""
  return 'darwin' == platform


def isLin():
  """Are we on linux?"""
  return platform.startswith('linux')


def isWin():
  """Are we on windows?"""
  return platform == 'cygwin' or platform.startswith('win')


class Rebooter():

  def __init__(self, operation='reboot', delay=False, reason=None, force=False):
    """Restarts / shutdowns system

    Args:
      operation - str; one of possible operations: rebobot / shutdown
      delay - int; delay in seconds; will not be executed on Mac OS X
      reason - str; reason why you conduct restart
      force - bool; force operatioon. Risky!
    """

    if operation not in ['reboot', 'shutdown']:
      raise Exception('Unrecognized operation.')

    if isWin():
      command = ['shutdown']
      if operation == 'reboot':
        command.append('/r')
      else:
        command.append('/s')
      if delay:
        command.append('/t')
        command.append(str(delay))
      if reason is not None:
        command.append('/c "%s"' % reason)
      if force:
        command.append('/force')
    elif isMac():
      # On Mac use AppleScript, as shutdown requires root
      if operation == 'reboot':
        operation = 'restart'
      else:
        operation = 'shut down'
      osascript = 'tell app "Finder" to %s' % operation
      command = ['osascript', '-e', osascript]
    elif isLin():
      if force:
        command = ['reboot', '-f']
        if command == ['shutdown']:
          command.append('-p')
      else:
        command = ['shutdown']
        if operation == 'reboot':
          command.append('-r')
        else:
          command.append('-h')
        if not delay:
          command.append('now')
          command.append(reason)
        else:
          # Appending reason as another list item, will spawn:
          # 'Failed to parse time specification'
          command.append('-t %i sec %s' % (delay, reason))
    else:
      raise Exception('Unrecognized system.')

    check_output(command, stderr=STDOUT)
