import queue
import subprocess
import threading
from typing import List, Optional
from typing_extensions import Dict, Set

import sublime

class FastFuzzyFinder:
    query: str
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
