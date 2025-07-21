from typing_extensions import override

from ..state import FUZZY_FINDER_IO_PANEL_NAME, FuzzyFinderState

from ..utils import run_ripgrep_command
from ..Terminal import FastFuzzyFinder
import threading
import sublime
import sublime_plugin
from queue import Queue

class FastFuzzyFindShowInputCommand(sublime_plugin.WindowCommand):
    def __init__(self, window: sublime.Window):
        self.query: str = ""
        super().__init__(window)

    @override
    def run(self):
        [output_view, input_view] = self.window.find_io_panel(FUZZY_FINDER_IO_PANEL_NAME)

        if output_view is None or input_view is None:
            [output_view, input_view] = self.window.create_io_panel(FUZZY_FINDER_IO_PANEL_NAME, self.on_done)

        output_view.set_scratch(True)
        output_view.set_name("Live Grep 🔍")
        output_view.settings().set("word_wrap", False)
        output_view.settings().set("fast_fuzzy_find.results_panel", True)

        input_view.settings().set("fast_fuzzy_find.input_panel", True)
        FastFuzzyFinder.is_input_open = True

        self.window.run_command("show_panel", { "panel": f"output.{FUZZY_FINDER_IO_PANEL_NAME}" })

        # Autoselect the previous search for seamless input
        entire_region = sublime.Region(0, input_view.size())
        input_view.sel().clear()
        input_view.sel().add(entire_region)

    def on_done(self, inp: str):
        [output_panel, input_view] = self.window.find_io_panel(FUZZY_FINDER_IO_PANEL_NAME)

        if input_view is None or output_panel is None:
            return

        # content = input_view.substr(sublime.Region(0, input_view.size()))
        # FuzzyFinderState.toggle_running(True)
        input_view.run_command("fast_fuzzy_find_update_output", {"line": inp})
        output_panel.run_command("fast_fuzzy_find_open_line")
        pass

    @classmethod
    def on_search(cls, inp: str):
        FUZZY_FINDER_QUERY = FuzzyFinderState.getQuery()
        [output_view, input_view] = sublime.active_window().find_io_panel(FUZZY_FINDER_IO_PANEL_NAME)

        if output_view is None or input_view is None:
            return

        if FuzzyFinderState.is_running() is True:
            return

        if FUZZY_FINDER_QUERY != inp or FUZZY_FINDER_QUERY == "":
            return

        FastFuzzyFinder.is_input_open = False

        # get the first folder for now
        folders = sublime.active_window().folders()
        folder = folders[0] if folders.__len__() > 0 else None

        if folder is None:
            return

        FuzzyFinderState.toggle_running(True)
        print("fuzzy run!")

        if FastFuzzyFinder.thread is None:
            FastFuzzyFinder.thread_output = Queue()
            FastFuzzyFinder.thread_input = Queue()
            FastFuzzyFinder.thread = threading.Thread(
                target=run_ripgrep_command,
                args=(inp, r'%s' % folder, FastFuzzyFinder.thread_output, FastFuzzyFinder.thread_input)
            )
            FastFuzzyFinder.thread.start()

        POLL_COUNT = 0
        output_view.run_command("fast_fuzzy_find_reset_output")

        while True:
            FastFuzzyFinder.thread.join(0.1)

            lines = []
            while FastFuzzyFinder.thread_output and FastFuzzyFinder.thread_output.empty() is False:
                line, ltype = FastFuzzyFinder.thread_output.get()
                lines.append(line.rstrip())

            content = '\n'.join(lines)
            output_view.run_command("fast_fuzzy_find_update_output", {"line": content})

            if FastFuzzyFinder.thread.is_alive() is False or POLL_COUNT > 5:
                FastFuzzyFinder.output = []
                FastFuzzyFinder.thread = None
                break
            POLL_COUNT = POLL_COUNT + 1

        lines = output_view.lines(sublime.Region(0, output_view.size()))
        output_view.sel().clear()
        output_view.sel().add(lines[0].a)
        sublime.active_window().focus_view(input_view)
        sublime.set_timeout_async(lambda: FuzzyFinderState.toggle_running(False), 100)
