import sublime
import sublime_plugin


class FastFuzzyFindResetOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit):
        self.view.erase(edit, sublime.Region(0, self.view.size()))
