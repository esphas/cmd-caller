
import os
import subprocess

import sublime
import sublime_plugin

CmdCallerSettings = 'cmd_caller.sublime-settings'
Prefix            = '[CmdCaller]'
BufferUnsaved     = 'Current buffer has not been saved, will use default PWD.'
InvalidCommand    = 'Invalid argument: cmd should be string or array of strings.'
DefaultPWD        = '.'

# append text to view
class AppendTextCommand(sublime_plugin.TextCommand):
  def run(self, edit, text):
    self.view.insert(edit, self.view.size(), text)

# execute one line of command
class CmdCallerCommand(sublime_plugin.WindowCommand):

  # display output message
  def output(self, message):
    message = Prefix + ' ' + message + '\n'
    panel = self.window.find_output_panel('cmd-caller')
    if not panel:
      panel = self.window.create_output_panel('cmd-caller')
    panel.run_command('append_text', {'text': message})
    self.window.run_command('show_panel', {'panel': 'output.cmd-caller'})

  def run(self, cmd):
    # get directory of current view, if it exists
    view = self.window.active_view()
    if not view.file_name():
      self.output(BufferUnsaved)
      pwd = DefaultPWD
    else:
      pwd = os.path.dirname(view.file_name())
    # cmd: [str] and [list of str]
    if isinstance(cmd, list):
      try:
        cmd = ' '.join(cmd)
      except TypeError as e:
        self.output(InvalidCommand)
        return
    elif not isinstance(cmd, str):
      self.output(InvalidCommand)
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
