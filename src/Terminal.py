import queue
import subprocess
import threading
from typing import List, Optional
import sublime


class Terminal:
    sheet: Optional[sublime.View] = None
    output: List[str] = []
    process: Optional[subprocess.Popen] = None
    thread: Optional[threading.Thread] = None
    thread_output: Optional[queue.Queue] = None
    thread_output_proc: Optional[threading.Thread] = None
    thread_error_proc: Optional[threading.Thread] = None
    thread_input: Optional[queue.Queue] = None
    is_input_open = False
    inp = ''


def close_results_view():
    if Terminal.sheet is None:
        return

    def clear_view(_: bool):
        Terminal.sheet = None

    Terminal.sheet.close(clear_view)
