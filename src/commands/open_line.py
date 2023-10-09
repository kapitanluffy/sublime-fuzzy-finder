import os
import sublime
import sublime_plugin
from ..Terminal import FastFuzzyFinder


class FastFuzzyFindOpenLineCommand(sublime_plugin.WindowCommand):
    def run(self):
        if FastFuzzyFinder.sheet is None:
            return

        result_sheet = FastFuzzyFinder.sheet.sheet()
        if result_sheet is None:
            return

        line = FastFuzzyFinder.sheet.line(FastFuzzyFinder.sheet.sel()[0])
        line = FastFuzzyFinder.sheet.substr(line)
        segments = line.split(':')
        file = ':'.join(segments[:3])
        folder = self.window.folders()[0]
        fullpath = os.path.abspath(os.path.join(folder, file))

        if FastFuzzyFinder.preview_view_path == fullpath:
            return

        if FastFuzzyFinder.preview_view is not None:
            def _(_):
                FastFuzzyFinder.preview_view = None
            FastFuzzyFinder.preview_view.close(_)

        FastFuzzyFinder.preview_view_path = fullpath
        FastFuzzyFinder.preview_view = self.window.open_file(
            fullpath,
            sublime.ENCODED_POSITION + sublime.FORCE_GROUP + sublime.FORCE_CLONE + sublime.SEMI_TRANSIENT + sublime.ADD_TO_SELECTION
        )
        new_sheet = FastFuzzyFinder.preview_view.sheet()

        if new_sheet is None:
            return

        self.window.focus_sheet(result_sheet)
