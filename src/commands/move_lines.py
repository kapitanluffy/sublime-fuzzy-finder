import sublime
import sublime_plugin
from ..Terminal import Terminal


class FastFuzzyFindMoveLinesCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        is_forward = kwargs.get("forward", True)
        Terminal.sheet.run_command("move", {"by": "lines", "forward": is_forward})
