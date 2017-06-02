
import os
import subprocess

import sublime
import sublime_plugin

CmdCallerSettings = 'cmd_caller.sublime-settings'

# execute one line of command
class CmdCallerCommand(sublime_plugin.WindowCommand):
  Prefix         = '[CmdCaller]'
  BufferUnsaved  = 'Current buffer has not been saved, will use default PWD.'
  InvalidCommand = 'Invalid argument: cmd should be string or array of strings.'
  DefaultPWD     = '.'

  def run(self, cmd):
    # get directory of current view, if it exists
    view = self.window.active_view()
    if view.file_name() == None:
      sublime.error_message(Prefix + ' ' + BufferUnsaved)
      pwd = DefaultPWD
    else:
      pwd = os.path.dirname(view.file_name())
    # cmd: [str] and [list of str]
    if isinstance(cmd, list):
      try:
        cmd = ' '.join(cmd)
      except TypeError as e:
        sublime.error_message(Prefix + ' ' + InvalidCommand)
        return
    elif not isinstance(cmd, str):
      sublime.error_message(Prefix + ' ' + InvalidCommand)
      return
    # replace variables
    cmd = cmd.replace('%V', pwd)
    # exec
    subprocess.Popen(cmd)


# run specific command
class CmdCallerSpecCommand(sublime_plugin.WindowCommand):
  def run(self, app):
    cmd = sublime.load_settings(CmdCallerSettings).get('apps')[app]['cmd']
    self.window.run_command('cmd_caller', {'cmd': cmd})


# run default command
class CmdCallerDefaultCommand(sublime_plugin.WindowCommand):
  def run(self):
    dft = sublime.load_settings(CmdCallerSettings).get('default')
    self.window.run_command('cmd_caller_spec', {'app': dft})


# run selected command
class CmdCallerListCommand(sublime_plugin.WindowCommand):
  def run(self):
    items = list(sublime.load_settings(CmdCallerSettings).get('apps').keys())
    self.window.show_quick_panel(items, lambda idx: self.on_select(items, idx))

  def on_select(self, items, idx):
    if idx < 0:
      return
    self.window.run_command('cmd_caller_spec', {'app': items[idx]})
