"""The grade table: your classes, credits, grades, and GPA. Tasks 1–3.

Streamlit topics: st.metric, st.dataframe, st.form, st.data_editor, session state
Docs: https://docs.streamlit.io/develop/api-reference/data/st.metric
      https://docs.streamlit.io/develop/api-reference/data/st.dataframe
      https://docs.streamlit.io/develop/api-reference/execution-flow/st.form
      https://docs.streamlit.io/develop/api-reference/data/st.data_editor

Your classes live in session state (state.COURSES). Change them there and the
table, GPA, and chat bot all update on the next rerun.
"""

import pandas as pd
import streamlit as st

from lib import gpa, state  # noqa: F401  (you'll use state)
from ui import todo


def render(courses: pd.DataFrame) -> None:
    st.subheader("My grades")
    show_summary(courses)
    show_table(courses)
    add_course_form()
    edit_courses()


def show_summary(courses: pd.DataFrame) -> None:
    """Numbers at the top: GPA and credits."""
    current = gpa.gpa(courses)
    st.metric("GPA", "—" if current is None else f"{current:.2f}")

    # TODO(Task 1a): put two more metrics next to the GPA, in one row.
    #   - Use three columns: gpa_col, done_col, left_col = st.columns(3)
    #     and move the GPA metric into gpa_col (gpa_col.metric(...)).
    #   - "Credits earned": total credits of graded classes
    #       gpa.graded(courses)["credits"].sum()
    #   - "Credits in progress": total credits of classes with no grade yet
    #       gpa.in_progress(courses)["credits"].sum()


def show_table(courses: pd.DataFrame) -> None:
    """Draw the course table."""
    table = gpa.add_points_column(courses)

    # TODO(Task 1b): make the table easier to read. Do all three:
    #   1. Show "In progress" instead of a blank grade.
    #        table["grade"] = table["grade"].fillna(gpa.IN_PROGRESS)
    #   2. Pass column_config= to st.dataframe:
    #        - capitalized titles: "Course", "Credits", "Grade", "Points"
    #        - "credits" as st.column_config.NumberColumn with format="%d"
    #        - "points" as st.column_config.NumberColumn with format="%.1f"
    #   3. Color the "grade" column: A's green, B's blue, C's orange, D and F red.
    #      Hint: table.style.map(color_function, subset=["grade"]),
    #      where color_function returns a CSS string like "color: green".
    st.dataframe(table, hide_index=True, width="stretch")


def add_course_form() -> None:
    """A form to add a class and its grade."""
    # TODO(Task 2): build the form.
    #   - st.form("add_course", clear_on_submit=True) containing:
    #       st.text_input("Course")
    #       st.number_input("Credits", min_value=1, max_value=6, value=3)
    #       st.selectbox("Grade", [gpa.IN_PROGRESS, *gpa.GRADE_POINTS])
    #       st.form_submit_button("Add course")
    #   - When submitted:
    #       - empty name, or a course already in the table -> st.error(...)
    #       - otherwise build the new row. Store grade None for "In progress".
    #         Add it to state.get(state.COURSES) with
    #         pd.concat(..., ignore_index=True), save it with
    #         state.set(state.COURSES, ...), then call st.rerun()
    #   Hint: st.columns(3) puts the three inputs in one row.
    todo("Task 2", "A form to add a class and its grade.")


def edit_courses() -> None:
    """Change or delete classes already in the table."""
    # TODO(Task 3): let the user fix their classes.
    #   - In st.expander("Edit courses"), show
    #       edited = st.data_editor(
    #           state.get(state.COURSES),
    #           num_rows="dynamic",
    #           key=f"editor_{state.get(state.EDITOR_VERSION)}",
    #           column_config={...},
    #       )
    #   - In column_config, make "grade" a dropdown:
    #       st.column_config.SelectboxColumn("Grade", options=list(gpa.GRADE_POINTS))
    #     and "credits" a NumberColumn with min_value=1, max_value=6, step=1.
    #   - Add st.button("Save changes"). When clicked:
    #       state.set(state.COURSES, edited)
    #       state.set(state.EDITOR_VERSION, state.get(state.EDITOR_VERSION) + 1)
    #       st.rerun()
    #   Why the version number? The editor remembers the edits you made. A new
    #   key gives you a fresh editor, so old edits aren't applied twice.
    todo("Task 3", "Edit or delete classes with st.data_editor.")
