
import os
import subprocess

import sublime
import sublime_plugin

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


class CmdCallerSpecCommand(sublime_plugin.WindowCommand):
  def run(self, app):
    cmd = sublime.load_settings('cmd_caller.sublime-settings').get('apps')[app]['cmd']
    self.window.run_command('cmd_caller', {'cmd': cmd})


class CmdCallerDefaultCommand(sublime_plugin.WindowCommand):
  def run(self):
    dft = sublime.load_settings('cmd_caller.sublime-settings').get('default')
    self.window.run_command('cmd_caller_spec', {'app': dft})
