import sublime
import sublime_plugin


class FastFuzzyFindUpdateOutputCommand(sublime_plugin.TextCommand):
    def run(self, edit: sublime.Edit, **kwargs):
        line = kwargs.get("line", None)
        if line is None:
            return
        self.view.insert(edit, 0, line)
