from ..utils import run_command
from ..Terminal import FastFuzzyFinder, close_results_view
import threading
import sublime
import sublime_plugin
from queue import Queue


class FastFuzzyFindShowInputCommand(sublime_plugin.WindowCommand):
    query = ""
    input_panel_view = None

    def get_terminal(self):
        if FastFuzzyFinder.sheet is None or FastFuzzyFinder.sheet.window() is None:
            FastFuzzyFinder.sheet = self.window.new_file(
                flags=sublime.ADD_TO_SELECTION
            )

        return FastFuzzyFinder.sheet

    def run(self):
        terminal_sheet = self.get_terminal()

        # content = HTML.format(body=' '.join(Terminal.output))
        # terminal_sheet.set_contents(content)

        view = self.window.active_view()

        if view is None:
            return

        sheet = view.sheet()
        tsheet = terminal_sheet.sheet()

        if sheet is None or tsheet is None:
            return

        # self.window.select_sheets([sheet, tsheet])
        # self.window.focus_view(view)

        terminal_sheet.set_scratch(True)
        terminal_sheet.set_name("Fuzzy Find 🔍")
        self.input_panel_view = self.window.show_input_panel("Fuzzy Find", "", self.on_done, self.on_change, self.on_cancel)
        self.input_panel_view.settings().set("fast_fuzzy_find", True)

        FastFuzzyFinder.is_input_open = True

    def on_done(self, inp: str):
        self.input_panel_view = None
        FastFuzzyFinder.sheet.window().run_command("fast_fuzzy_find_open_line")

    def on_search(self, inp: str):
        if self.query != inp or self.query == "":
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
        FastFuzzyFinder.sheet.run_command("fast_fuzzy_find_reset_output")

        while True:
            FastFuzzyFinder.thread.join(0.1)

            lines = []
            while FastFuzzyFinder.thread_output and FastFuzzyFinder.thread_output.empty() is False:
                line, ltype = FastFuzzyFinder.thread_output.get()
                lines.append(line.rstrip())

            content = '\n'.join(lines)
            FastFuzzyFinder.sheet.run_command("fast_fuzzy_find_update_output", {"line": content})

            if FastFuzzyFinder.thread.is_alive() is False or POLL_COUNT > 5:
                FastFuzzyFinder.output = []
                FastFuzzyFinder.thread = None
                break
            POLL_COUNT = POLL_COUNT + 1

        lines = FastFuzzyFinder.sheet.lines(sublime.Region(0, FastFuzzyFinder.sheet.size()))
        FastFuzzyFinder.sheet.sel().clear()
        FastFuzzyFinder.sheet.sel().add(lines[0].a)
        self.query = ""
        self.window.focus_view(self.input_panel_view)

    def on_change(self, inp: str):
        if inp == "":
            return
        sublime.set_timeout_async(lambda inp=inp: self.on_search(inp), 150)
        self.query = inp

    def on_cancel(self, *args):
        FastFuzzyFinder.is_input_open = False
        self.input_panel_view = None
        close_results_view()

