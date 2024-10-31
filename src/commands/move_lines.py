import sublime
import sublime_plugin
from ..Terminal import FastFuzzyFinder


class FastFuzzyFindMoveLinesCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        is_forward = kwargs.get("forward", True)
        FastFuzzyFinder.search_result_view.run_command("move", {"by": "lines", "forward": is_forward})
