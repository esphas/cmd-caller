
import os.path

import sublime
import sublime_plugin

from .support import log

# settings

def get(key, default = None):
  log('settings.get:\n\tkey: ' + key + '\n\tdefault: None')
  _package_settings = sublime.load_settings('cmd_caller.sublime-settings')
  if not _package_settings:
    log('\tget: default')
    return default
  _package_settings = _package_settings.get(sublime.platform())
  if key in _package_settings:
    log('\tget: ' + str(_package_settings[key]))
    return _package_settings[key]
  else:
    log('\tget: default')
    return default


class CmdCallerEditSettingsCommand(sublime_plugin.WindowCommand):
  def run(self):
    log(self.__class__.__name__)
    base_file = '${packages}/cmd-caller/settings/cmd_caller.sublime-settings'
    default = '{\n\t"' + sublime.platform() + '": {\n\t\t$0\n\t}\n}'
    self.window.run_command('edit_settings', {"base_file": base_file, "default": default})


class CmdCallerEditKeyBindingsCommand(sublime_plugin.WindowCommand):
  def run(self):
    log(self.__class__.__name__)
    relapth = 'cmd-caller/keybinds/Default (' + sublime.platform().capitalize() + ').sublime-keymap'
    base_file = '${packages}/' + relapth
    default = sublime.load_resource('Packages/' + relapth)
    self.window.run_command('edit_settings', {"base_file": base_file, "default": default})
