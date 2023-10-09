from .src.Terminal import FastFuzzyFinder, close_results_view
import sublime
import sublime_plugin


class FastFuzzyFindKeybindListener(sublime_plugin.EventListener):
    def on_query_context(
        self,
        view: sublime.View,
        key: str,
        operator: sublime.QueryOperator,
        operand: str,
        match_all: bool
    ):
        if key.startswith("fast_fuzzy_find"):
            return True
        return None


class FastFuzzyFindViewListener(sublime_plugin.ViewEventListener):
    def on_close(self):
        is_results_panel = self.view.settings().get("fast_fuzzy_find.results_panel", None)
        if is_results_panel is not None:
            close_results_view()
            if FastFuzzyFinder.input_panel_view is not None:
                sublime.active_window().run_command("hide_panel", {"cancel": True})
                FastFuzzyFinder.input_panel_view = None
