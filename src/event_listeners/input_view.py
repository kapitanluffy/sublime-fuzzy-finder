from ..commands.show_input import FastFuzzyFindShowInputCommand
from ..state import FUZZY_FINDER_IO_PANEL_NAME, FuzzyFinderState
import sublime
import sublime_plugin

class FastFuzzyInputPanelListener(sublime_plugin.EventListener):
    def on_modified_async(self, view: sublime.View):
        if not view.settings().get("fast_fuzzy_find.input_panel"):
            return

        window = view.window()
        previous_content = FuzzyFinderState.getQuery()
        content = view.substr(sublime.Region(0, view.size()))

        if previous_content == content:
            return

        FuzzyFinderState.setQuery(content)
        sublime.set_timeout_async(lambda: FastFuzzyFindShowInputCommand.on_search(content), 100)

class FastFuzzyResultViewListener(sublime_plugin.ViewEventListener):
    def on_pre_close(self):
        is_result_view = self.view.settings().get("fast_fuzzy_find.result_view", False)
        result_view = FuzzyFinderState.get_result_view()
        window = self.view.window()

        if window is None:
            return

        [_, input_panel] = window.find_io_panel(FUZZY_FINDER_IO_PANEL_NAME)

        if input_panel is not None:
            # Delay shifting focus because it will automatically focus on the next view
            sublime.set_timeout_async(lambda: window.focus_view(input_panel), 100)

        if is_result_view is True:
            self.view.settings().erase("fast_fuzzy_find.result_view")

        if result_view and self.view.id() == result_view.id():
            FuzzyFinderState.clear_result_view()
