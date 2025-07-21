import sublime
import sublime_plugin
from ..state import FUZZY_FINDER_IO_PANEL_NAME

class FastFuzzyFindMoveLinesCommand(sublime_plugin.WindowCommand):
    def run(self, **kwargs):
        is_forward = kwargs.get("forward", True)
        [output_view, _] = self.window.find_io_panel(FUZZY_FINDER_IO_PANEL_NAME)

        if output_view is None:
            return

        output_view.run_command("move", {"by": "lines", "forward": is_forward})
