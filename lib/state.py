"""Session state helpers.

Streamlit reruns the whole script every time the user interacts with the page.
Normal Python variables are reset on each rerun, so anything the app needs to
remember (chat history, settings, counters) lives in ``st.session_state``.

This module keeps every state key and its default value in one place, so the
rest of the app never has to guess a key name or check whether it exists.

Each browser tab gets its own session state. Two people using the app at the
same time do NOT see each other's state.
"""

from __future__ import annotations

import copy
from typing import Any

import streamlit as st

# --- State keys -------------------------------------------------------------
# Use these constants instead of typing strings, so a typo fails loudly.
MESSAGES = "messages"  # list[Message]: the chat conversation
COURSES = "courses"  # pandas DataFrame: your classes and grades (loaded on first run)
EDITOR_VERSION = "editor_version"  # int: bumped to reset the course editor (Task 3)

# --- Defaults ---------------------------------------------------------------
# Every key the app uses, with the value it starts with.
# Add new keys here when you add features.
DEFAULTS: dict[str, Any] = {
    MESSAGES: [],
    COURSES: None,
    EDITOR_VERSION: 0,
}


def init_state() -> None:
    """Set any missing keys to their default value.

    Call this once at the top of ``streamlit_app.py``. Keys that already exist
    are left alone, so values survive reruns.
    """
    for key, default in DEFAULTS.items():
        if key not in st.session_state:
            # deepcopy so sessions never share the same list/dict object
            st.session_state[key] = copy.deepcopy(default)


def get(key: str) -> Any:
    """Return the current value for ``key``."""
    if key not in DEFAULTS:
        raise KeyError(f"Unknown state key {key!r}. Add it to DEFAULTS in lib/state.py.")
    if key not in st.session_state:
        st.session_state[key] = copy.deepcopy(DEFAULTS[key])
    return st.session_state[key]


def set(key: str, value: Any) -> None:  # noqa: A001 - mirrors get()
    """Store ``value`` under ``key``."""
    if key not in DEFAULTS:
        raise KeyError(f"Unknown state key {key!r}. Add it to DEFAULTS in lib/state.py.")
    st.session_state[key] = value


def reset(key: str | None = None) -> None:
    """Put one key (or every key, if ``key`` is None) back to its default."""
    keys = [key] if key is not None else list(DEFAULTS)
    for k in keys:
        set(k, copy.deepcopy(DEFAULTS[k]))
