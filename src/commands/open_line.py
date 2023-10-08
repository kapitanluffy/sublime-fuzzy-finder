import sublime
import sublime_plugin
from ..Terminal import Terminal, close_results_view


class FastFuzzyFindOpenLineCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        line = Terminal.sheet.line(Terminal.sheet.sel()[0])
        line = Terminal.sheet.substr(line)
        segments = line.split(':')
        file = ':'.join(segments[:3])
        folder = self.window.folders()[0]
        fullpath = os.path.join(folder, file)
        print("open:", fullpath)
        Terminal.sheet.window().open_file(fullpath, sublime.ENCODED_POSITION)
        close_results_view()
