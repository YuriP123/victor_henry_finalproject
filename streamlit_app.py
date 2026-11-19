"""GPA Calculator: your grade table on the left, a chat box on the right."""

import streamlit as st

from lib import gpa, state
from ui import chat, grade_table

st.set_page_config(page_title="GPA Calculator", page_icon="🎓", layout="wide")

# Must run before anything reads session state.
state.init_state()

# Load the starting classes once per session. Keeping them in session state
# means classes you add in the app survive reruns.
if state.get(state.COURSES) is None:
    state.set(state.COURSES, gpa.load_courses())

courses = state.get(state.COURSES)

st.title("🎓 GPA Calculator")
table_col, chat_col = st.columns([3, 2], gap="large")

with table_col:
    grade_table.render(courses)  # Tasks 1–3

with chat_col:
    chat.render(courses)  # Tasks 4–5
