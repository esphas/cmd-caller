
import os.path

import sublime

# settings

_package_settings = None

def get(key, default = None):
  global _package_settings
  _package_settings = sublime.load_settings('cmd_caller.sublime-settings')
  if not _package_settings:
    return default
  _package_settings = _package_settings.get(sublime.platform())
  if key in _package_settings:
    return _package_settings[key]
  else:
    return default
