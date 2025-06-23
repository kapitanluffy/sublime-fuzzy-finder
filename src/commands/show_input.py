from ..utils import run_command
from ..Terminal import FastFuzzyFinder, close_results_view
import threading
import sublime
import sublime_plugin
from queue import Queue


class FastFuzzyFindShowInputCommand(sublime_plugin.WindowCommand):
    query = ""

    def run(self):
        if FastFuzzyFinder.search_result_view is not None:
            self.window.focus_view(FastFuzzyFinder.search_result_view)

        if FastFuzzyFinder.search_result_view is None or FastFuzzyFinder.search_result_view.window() is None:
            FastFuzzyFinder.search_result_view = self.window.new_file()

        view = self.window.active_view()

        if view is None:
            return

        sheet = view.sheet()
        tsheet = FastFuzzyFinder.search_result_view.sheet()

        if sheet is None or tsheet is None:
            return

        FastFuzzyFinder.search_result_view.set_scratch(True)
        FastFuzzyFinder.search_result_view.set_name("Live Grep 🔍")
        FastFuzzyFinder.search_result_view.settings().set("word_wrap", False)
        FastFuzzyFinder.input_panel_view = self.window.show_input_panel("Fuzzy Find", "", self.on_done, self.on_change, self.on_cancel)
        FastFuzzyFinder.input_panel_view.settings().set("fast_fuzzy_find.input_panel", True)
        FastFuzzyFinder.search_result_view.settings().set("fast_fuzzy_find.results_panel", True)

        FastFuzzyFinder.is_input_open = True

    def on_done(self, inp: str):
        FastFuzzyFinder.input_panel_view = None
        FastFuzzyFinder.search_result_view.window().run_command("fast_fuzzy_find_open_line")

    def on_search(self, inp: str):
        if FastFuzzyFinder.query != inp or FastFuzzyFinder.query == "":
            return

        FastFuzzyFinder.is_input_open = False

        # get the first folder for now
        folder = self.window.folders()[0]

        if FastFuzzyFinder.thread is None:
            FastFuzzyFinder.thread_output = Queue()
            FastFuzzyFinder.thread_input = Queue()
            FastFuzzyFinder.thread = threading.Thread(
                target=run_command,
                args=(inp, r'%s' % folder, FastFuzzyFinder.thread_output, FastFuzzyFinder.thread_input)
            )
            FastFuzzyFinder.thread.start()

        POLL_COUNT = 0
        FastFuzzyFinder.search_result_view.run_command("fast_fuzzy_find_reset_output")

        while True:
            FastFuzzyFinder.thread.join(0.1)

            lines = []
            while FastFuzzyFinder.thread_output and FastFuzzyFinder.thread_output.empty() is False:
                line, ltype = FastFuzzyFinder.thread_output.get()
                lines.append(line.rstrip())

            content = '\n'.join(lines)
            FastFuzzyFinder.search_result_view.run_command("fast_fuzzy_find_update_output", {"line": content})

            if FastFuzzyFinder.thread.is_alive() is False or POLL_COUNT > 5:
                FastFuzzyFinder.output = []
                FastFuzzyFinder.thread = None
                break
            POLL_COUNT = POLL_COUNT + 1

        lines = FastFuzzyFinder.search_result_view.lines(sublime.Region(0, FastFuzzyFinder.search_result_view.size()))
        FastFuzzyFinder.search_result_view.sel().clear()
        FastFuzzyFinder.search_result_view.sel().add(lines[0].a)
        self.window.focus_view(FastFuzzyFinder.input_panel_view)

    def on_change(self, inp: str):
        if inp == "":
            return
        FastFuzzyFinder.query = inp
        sublime.set_timeout_async(lambda inp=inp: self.on_search(inp), 150)

    def on_cancel(self, *args):
        FastFuzzyFinder.is_input_open = False
        FastFuzzyFinder.input_panel_view = None
