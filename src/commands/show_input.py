from ..utils import run_command
from ..Terminal import Terminal, close_results_view
import threading
import sublime
import sublime_plugin
from queue import Queue


class FastFuzzyFindShowInputCommand(sublime_plugin.WindowCommand):
    query = ""
    input_panel_view = None

    def get_terminal(self):
        if Terminal.sheet is None or Terminal.sheet.window() is None:
            Terminal.sheet = self.window.new_file(
                flags=sublime.ADD_TO_SELECTION
            )

        return Terminal.sheet

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

        Terminal.is_input_open = True

    def on_done(self, inp: str):
        self.input_panel_view = None
        Terminal.sheet.window().run_command("fast_fuzzy_find_open_line")

    def on_search(self, inp: str):
        if self.query != inp or self.query == "":
            return

        Terminal.is_input_open = False

        # get the first folder for now
        folder = self.window.folders()[0]

        if Terminal.thread is None:
            Terminal.thread_output = Queue()
            Terminal.thread_input = Queue()
            Terminal.thread = threading.Thread(
                target=run_command,
                args=(inp, r'%s' % folder, Terminal.thread_output, Terminal.thread_input)
            )
            Terminal.thread.start()

        POLL_COUNT = 0
        Terminal.sheet.run_command("fast_fuzzy_find_reset_output")

        while True:
            Terminal.thread.join(0.1)

            lines = []
            while Terminal.thread_output and Terminal.thread_output.empty() is False:
                line, ltype = Terminal.thread_output.get()
                lines.append(line.rstrip())

            content = '\n'.join(lines)
            Terminal.sheet.run_command("fast_fuzzy_find_update_output", {"line": content})

            if Terminal.thread.is_alive() is False or POLL_COUNT > 5:
                Terminal.output = []
                Terminal.thread = None
                break
            POLL_COUNT = POLL_COUNT + 1

        lines = Terminal.sheet.lines(sublime.Region(0, Terminal.sheet.size()))
        Terminal.sheet.sel().clear()
        Terminal.sheet.sel().add(lines[0].a)
        self.query = ""
        self.window.focus_view(self.input_panel_view)

    def on_change(self, inp: str):
        if inp == "":
            return
        sublime.set_timeout_async(lambda inp=inp: self.on_search(inp), 150)
        self.query = inp

    def on_cancel(self, *args):
        Terminal.is_input_open = False
        self.input_panel_view = None
        close_results_view()

