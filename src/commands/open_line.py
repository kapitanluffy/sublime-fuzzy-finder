import os
import sublime
import sublime_plugin
from ..Terminal import FastFuzzyFinder
from ..state import FUZZY_FINDER_IO_PANEL_NAME, FuzzyFinderState

class FastFuzzyFindOpenLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        window = self.view.window()

        if window is None:
            return

        [_, input_view] = window.find_io_panel(FUZZY_FINDER_IO_PANEL_NAME)
        if input_view is None:
            return

        line = self.view.line(self.view.sel()[0])
        line = self.view.substr(line)
        segments = line.split(':')
        file = ':'.join(segments[:3])
        folder = window.folders()[0]
        fullpath = os.path.abspath(os.path.join(folder, file))

        FastFuzzyFinder.preview_view = window.open_file(
            fullpath,
            sublime.ENCODED_POSITION + sublime.FORCE_GROUP  # pyright: ignore[reportArgumentType]
        )

        FuzzyFinderState.set_result_view(FastFuzzyFinder.preview_view)
        FastFuzzyFinder.preview_view.settings().set("fast_fuzzy_find.result_view", True)

        window.focus_view(input_view)

        new_sheet = FastFuzzyFinder.preview_view.sheet()
        if new_sheet is None:
            return
