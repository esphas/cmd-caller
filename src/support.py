
import sublime
import sublime_plugin

# support

class CmdCallerReadmeCommand(sublime_plugin.TextCommand):
  
  def run(self, edit):
    f = self.view.window().new_file()
    f.set_name("Cmd Caller: Readme")
    f.settings().set('gutter', False)
    f.insert(edit, 0, sublime.load_resource('Packages/cmd-caller/README.md'))
    f.set_syntax_file('Packages/Markdown/Markdown.sublime-syntax')
    f.set_read_only(True)
    f.set_scratch(True)
