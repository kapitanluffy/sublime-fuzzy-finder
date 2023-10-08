import sublime
import sublime_plugin


class FastFuzzyFindKeybindListener(sublime_plugin.EventListener):
    def on_query_context(self, view: sublime.View, key: str, operator: sublime.QueryOperator, operand: str, match_all: bool):
        if key == "fast_fuzzy_find" and operand is True:
            return True
        return None
