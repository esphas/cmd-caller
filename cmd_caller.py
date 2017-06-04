
import os
import subprocess

import sublime
import sublime_plugin

# append text to view
class AppendTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, text):
    self.view.insert(edit, self.view.size(), text)

# execute one line of command
class CmdCaller(sublime_plugin.WindowCommand):
  Prefix            = '[CmdCaller]'
  BufferUnsaved     = 'Current buffer has not been saved, will use default PWD'
  InvalidCommand    = 'Invalid argument: cmd should be a string or an array'
  CannotExec        = 'Cannot execute command'
  DefaultPWD        = '.'
  SettingsFile      = 'cmd_caller.sublime-settings'

  # display output message
  def output(self, message):
    message = self.Prefix + ' ' + message + '\n'
    panel = self.window.find_output_panel('cmd-caller')
    if not panel:
      panel = self.window.create_output_panel('cmd-caller')
    panel.run_command('append_text', {'text': message})
    self.window.run_command('show_panel', {'panel': 'output.cmd-caller'})

  def error(self, message, cmd):
    self.output(message + ':\n\t' + cmd)

  # load settings
  def settings(self):
    return sublime.load_settings(self.SettingsFile)

  def run(self, cmd):
    # get directory of current view, if it exists
    view = self.window.active_view()
    if not view.file_name():
      self.output(BufferUnsaved)
      pwd = self.DefaultPWD
    else:
      pwd = os.path.dirname(view.file_name())
    # cmd: [str] and [list of str]
    if isinstance(cmd, list):
      cmd = ' '.join(str(c) for c in cmd)
    elif not isinstance(cmd, str):
      self.error(self.InvalidCommand, cmd)
      return
    # replace variables
    cmd = cmd.replace('%V', pwd)
    # exec
    try:
      subprocess.Popen(cmd)
    except FileNotFoundError:
      self.error(self.CannotExec, cmd)


# run specific command
class CmdCallerSpec(CmdCaller):
  def run(self, app):
    cmd = self.settings().get('apps')[app]['cmd']
    super().run(cmd)


# run default command
class CmdCallerDefaultCommand(CmdCallerSpec):
  def run(self):
    dft = self.settings().get('default')
    super().run(dft)


# run selected command
class CmdCallerListCommand(CmdCallerSpec):
  def run(self):
    items = list(item['name'] for item in self.settings().get('apps').values())
    self.window.show_quick_panel(items, lambda idx: self.on_select(items, idx))

  def on_select(self, items, idx):
    if idx < 0:
      return
    super().run(items[idx])
