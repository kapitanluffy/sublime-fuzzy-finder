import queue
import subprocess
import threading
from typing import List, Optional
import sublime


class FastFuzzyFinder:
    query: str
    search_result_view: Optional[sublime.View] = None
    input_panel_view: Optional[sublime.View] = None
    preview_view: Optional[sublime.View] = None
    preview_view_path: Optional[str] = None
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
    if FastFuzzyFinder.search_result_view is None:
        return

    def clear_view(_: bool):
        FastFuzzyFinder.search_result_view = None

    FastFuzzyFinder.search_result_view.close(clear_view)
