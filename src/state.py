import sublime
from typing_extensions import Optional, Dict, Set

FUZZY_FINDER_IO_PANEL_NAME = "fuzzy_finder"

FUZZY_FINDER_INPUT_PANEL_VIEW: Optional[sublime.View] = None
FUZZY_FINDER_SEARCH_PANEL_VIEW: Optional[sublime.View] = None

FUZZY_FINDER_INPUT_PANEL_LISTENERS = {}

FUZZY_FINDER_INPUT_PANEL_BUFFER_IDS: Set[int] = set()

FUZZY_FINDER_QUERY = ""

# Need to handle state independently for each window
class FuzzyFinderState():
    query: Optional[str] = None
    view: Optional[sublime.View] = None
    running: bool = False

    @classmethod
    def setQuery(cls, value: str):
        cls.query = value

    @classmethod
    def getQuery(cls):
        return cls.query

    @classmethod
    def toggle_running(cls, value: bool):
        cls.running = value

    @classmethod
    def is_running(cls):
        return cls.running

    @classmethod
    def set_result_view(cls, view: sublime.View):
        cls.view = view

    @classmethod
    def get_result_view(cls):
        return cls.view

    @classmethod
    def clear_result_view(cls):
        cls.view = None
