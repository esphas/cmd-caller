
import os

import sublime
import sublime_plugin

# support

# log

logfile = 'logs.txt'
lastlogfile = 'logs.last.txt'

prefix = os.path.normpath(os.path.join(os.path.expanduser('~'), 'cmd-caller-'))
logfile = prefix + logfile
lastlogfile = prefix + lastlogfile
if os.path.exists(lastlogfile):
  os.remove(lastlogfile)
if os.path.exists(logfile):
  os.rename(logfile, lastlogfile)

def log(message):
  _log = open(logfile, 'ab+')
  _log.write((message + '\n').encode('utf-8'))
  _log.close()

# load text content to a new sheet
class LoadText(sublime_plugin.TextCommand):

  # load text file
  def load_text(self, edit, title, filename, syntax = None):
    log(self.__class__.__name__ + '#load_text')
    f = self.view.window().new_file()
    f.set_name(title)
    f.settings().set('gutter', False)
    try:
      if os.path.isabs(filename):
        _file = open(filename, 'rb')
        content =  _file.read().decode('utf-8')
        _file.close()
      else:
        content = sublime.load_resource('Packages/cmd-caller/' + filename)
    except OSError:
      print(os.path.isabs(filename))
      content = '\n\n\n--- No Content Available ---\n\n\n'
    f.insert(edit, 0, content)
    if syntax:
      f.set_syntax_file(syntax)
    f.set_read_only(True)
    f.set_scratch(True)

  # load markdown file
  def load_markdown(self, edit, title, filename):
    log(self.__class__.__name__ + '#load_markdown')
    self.load_text(self, edit, title, filename, 'Packages/Markdown/Markdown.sublime-syntax')


class LoadPluginFile(LoadText):

  # load logs
  def load_logs(self, edit, file):
    log(self.__class__.__name__ + '#load_logs')
    super().load_text(edit, 'Cmd Caller - Logs', file)


# load current logs
class CmdCallerLoadLogsCommand(LoadPluginFile):
  def run(self, edit):
    log(self.__class__.__name__)
    super().load_logs(edit, logfile)


# load last logs
class CmdCallerLoadLastLogsCommand(LoadPluginFile):
  def run(self, edit):
    log(self.__class__.__name__)
    super().load_logs(edit, lastlogfile)
    
