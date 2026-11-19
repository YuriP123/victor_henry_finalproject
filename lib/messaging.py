"""Chat messaging helpers.

A conversation is a list of ``Message`` objects stored in session state
(see ``lib/state.py``). This module adds messages and renders them with
``st.chat_message``. The bot's answers come from ``lib/bot.py``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

import streamlit as st

from lib import state

Role = Literal["user", "assistant"]


@dataclass
class Message:
    """One chat message."""

    role: Role
    content: str
    sent_at: datetime = field(default_factory=datetime.now)


# --- Storing messages -------------------------------------------------------


def get_messages() -> list[Message]:
    """Return the conversation so far, oldest first."""
    return state.get(state.MESSAGES)


def add_message(role: Role, content: str) -> Message:
    """Append a message to the conversation and return it."""
    message = Message(role=role, content=content)
    get_messages().append(message)
    return message


def clear_messages() -> None:
    """Delete the whole conversation."""
    state.reset(state.MESSAGES)


# --- Displaying messages ----------------------------------------------------


def render_message(message: Message) -> None:
    """Draw one message in the chat window."""
    with st.chat_message(message.role):
        st.markdown(message.content)
        # TODO(Task 5): optional polish, e.g. the time it was sent:
        #   st.caption(message.sent_at.strftime("%H:%M"))


def render_history() -> None:
    """Draw every message in the conversation."""
    for message in get_messages():
        render_message(message)
