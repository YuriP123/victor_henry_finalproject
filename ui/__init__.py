"""The two parts of the page, each with a render() function.

grade_table.py  your classes, grades, and GPA (Tasks 1–3)
chat.py         the chat box (Tasks 4–5)
"""

import streamlit as st


def todo(task: str, what: str) -> None:
    """Show a placeholder box where a task will go."""
    st.info(f"**{task}** — {what}", icon="🛠️")
