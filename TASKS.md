# Your Tasks

The app is a GPA calculator with two parts:

- **Grade table** (left): your classes, credits, and grades, with your GPA on top.
- **Chat box** (right): a bot that answers questions like "What do I need to get a 3.5?"

The GPA math (`lib/gpa.py`) and the bot (`lib/bot.py`) are finished.
Your job is to build the Streamlit parts. Do the tasks in order: each one
builds on what you learned in the one before.

| # | Task | Part | Where | Streamlit topics |
| --- | --- | --- | --- | --- |
| 1 | Summary and table formatting | Grade table | `ui/grade_table.py`: `show_summary()`, `show_table()` | `st.metric`, `st.columns`, `st.column_config` |
| 2 | Add a course | Grade table | `ui/grade_table.py`: `add_course_form()` | `st.form`, `st.selectbox`, session state |
| 3 | Edit courses | Grade table | `ui/grade_table.py`: `edit_courses()` | `st.data_editor`, `st.expander` |
| 4 | Suggestion buttons | Chat box | `ui/chat.py` | `st.button` |
| 5 | Chat polish | Chat box | `ui/chat.py`, `lib/messaging.py` | `st.chat_message`, `st.download_button` |

Tasks 2 and 3 show a 🛠️ box in the app until you build them.

## How to work on a task

1. Find the `TODO(Task N)` comment. It lists exactly what to build.
   The top of the file links to the Streamlit docs you need.
2. Start the app (`./scripts/run.sh` or the **Run app** task). It reloads every time you save.
3. If the task has tests (Tasks 1, 2, 4), run them:

   ```
   uv run pytest tests/test_ui.py
   ```

   They start as `x` (expected failure). When your code works, delete the
   `@todo("Task N")` line above each of that task's tests and run again. They should pass.
4. When you finish a task, run everything: `uv run pytest`. Nothing should say `FAILED`.

## Done when

### 1. Summary and table formatting
- [ ] "GPA", "Credits earned", and "Credits in progress" metrics in one row
- [ ] Classes without a grade say "In progress"
- [ ] Column titles are capitalized, and points show one decimal
- [ ] Grades are colored: A's green, B's blue, C's orange, D and F red
- [ ] Test: `test_credit_metrics`

### 2. Add a course
- [ ] A form with "Course", "Credits", and "Grade" (including "In progress") and an "Add course" button
- [ ] A graded course changes your GPA right away
- [ ] An in-progress course shows in the table but doesn't change your GPA
- [ ] The chat bot knows about the new course ("What if I get an A in Chemistry?")
- [ ] An empty or duplicate course name shows an error and adds nothing
- [ ] Tests: the five `test_add_*` / `test_new_course_*` tests

### 3. Edit courses
- [ ] An "Edit courses" section where you can change credits and grades
- [ ] Grades are picked from a dropdown, not typed
- [ ] You can delete a class and add a new one
- [ ] "Save changes" updates the table and GPA, and saving twice doesn't duplicate anything

### 4. Suggestion buttons
- [ ] A button for each question in `bot.SUGGESTIONS`, in one row
- [ ] Clicking one sends it to the chat and the bot answers
- [ ] Test: `test_suggestion_button_sends_the_question`

### 5. Chat polish
- [ ] At least two items from the `TODO(Task 5)` list in `ui/chat.py`
