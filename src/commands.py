
import os.path
import subprocess

import sublime
import sublime_plugin

from . import settings

# append text to view
class AppendTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, text):
    self.view.insert(edit, self.view.size(), text)

# execute one line of command
class CmdCaller(sublime_plugin.WindowCommand):

  # display output message
  def output(self, message):
    message = '[CmdCaller] ' + message + '\n'
    panel = self.window.find_output_panel('cmd-caller')
    if not panel:
      panel = self.window.create_output_panel('cmd-caller')
    panel.run_command('append_text', {'text': message})
    self.window.run_command('show_panel', {'panel': 'output.cmd-caller'})

  # display error message with cmd string
  def error(self, message, cmd):
    self.output(message + ':\n\t' + cmd)

  def get_settings(self, key, default = None):
    return settings.get(key, default)

  # run cmd
  def run_with_cmd(self, cmd):
    # get directory of current view, if it exists
    view = self.window.active_view()
    if not view.file_name():
      self.output('Current buffer has not been saved, will use default PWD')
      pwd = '.'
    else:
      pwd = os.path.dirname(view.file_name())
    # cmd: [str] and [list of str]
    if isinstance(cmd, list):
      cmd = ' '.join(str(c) for c in cmd)
    elif not isinstance(cmd, str):
      self.error('Invalid argument: cmd should be a string or an array', cmd)
      return
    # replace variables
    cmd = cmd.replace('%V', pwd)
    # exec
    try:
      subprocess.Popen(cmd)
    except FileNotFoundError:
      self.error('Cannot execute command', cmd)

  # run with app key
  def run_with_key(self, key):
    cmd = self.get_settings('apps')[key]['cmd']
    self.run_with_cmd(cmd)


# run default command
class CmdCallerDefaultCommand(CmdCaller):
  def run(self):
    dft = self.get_settings('default')
    super().run_with_key(dft)


# open a panel and run selected command
class CmdCallerListCommand(CmdCaller):
  def run(self):
    apps = self.get_settings('apps')
    self.keys = list(apps.keys())
    items = list(apps[key]['name'] if 'name' in apps[key] else key for key in self.keys)
    self.window.show_quick_panel(items, self.on_select)

  def on_select(self, idx):
    if idx < 0:
      return
    super().run_with_key(self.keys[idx])
