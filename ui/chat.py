"""The chat box: ask the bot about your grades. Tasks 4–5.

Streamlit topics: st.chat_message, st.chat_input, st.button, st.container
Docs: https://docs.streamlit.io/develop/api-reference/chat
"""

import pandas as pd
import streamlit as st

from lib import bot, messaging


def send(prompt: str, courses: pd.DataFrame) -> None:
    """Add your message and the bot's answer to the conversation."""
    messaging.add_message("user", prompt)
    messaging.add_message("assistant", bot.reply(prompt, courses))


def render(courses: pd.DataFrame) -> None:
    title_col, clear_col = st.columns([3, 1], vertical_alignment="bottom")
    title_col.subheader("Chat")
    if clear_col.button("Clear chat"):
        messaging.clear_messages()

    # Create the message box first and fill it last, so a new message shows
    # up in the same run it was sent.
    chat_box = st.container(height=450)

    prompt = st.chat_input("e.g. What do I need to get a 3.5?")

    # TODO(Task 4): suggestion buttons.
    #   Show one st.button per question in bot.SUGGESTIONS, in one row
    #   (st.columns). Clicking one sends it as if you typed it:
    #       if st.button(question): prompt = question

    if prompt:
        send(prompt, courses)

    with chat_box:
        if not messaging.get_messages():
            st.info(bot.HELP_TEXT)
        messaging.render_history()

    # TODO(Task 5): polish the chat. Pick at least two:
    #   - custom avatars: st.chat_message(role, avatar="🧑‍🎓") in lib/messaging.py
    #   - the time under each message with st.caption (lib/messaging.py)
    #   - a st.caption under the box with how many messages have been sent
    #   - a st.download_button that saves the conversation as a .txt file
