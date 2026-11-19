# 🎓 GPA Calculator

A Streamlit app with two parts:

- **Grade table**: your classes, credits, and grades, with your GPA on top.
- **Chat box**: ask about your grades, like "What do I need to get a 3.5?" or
  "What if I get an A in Biology?"

The GPA math, chat bot, state, and messaging are finished. The Streamlit
parts are yours to build: see [TASKS.md](TASKS.md).

## Get started

### Option A: GitHub Codespace (nothing to install)

1. Open the codespace link your instructor shares, or click **Code → Codespaces → Create codespace on main**.
2. Wait for setup to finish. The app starts by itself and opens in a preview tab.
3. If the preview doesn't open, go to the **Ports** tab and open port **8501**.

### Option B: Your own computer

You need [VS Code](https://code.visualstudio.com/) and [Git](https://git-scm.com/downloads).
You do **not** need to install Python. The setup script installs `uv`, which installs the right Python for you.

1. Clone the repo and open the folder in VS Code.
2. Accept the prompt to install the recommended extensions.
3. Open a terminal (**Terminal → New Terminal**) and run setup once:

   | macOS / Linux | Windows (PowerShell) |
   | --- | --- |
   | `./scripts/setup.sh` | `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1` |

4. Start the app:

   | macOS / Linux | Windows (PowerShell) |
   | --- | --- |
   | `./scripts/run.sh` | `powershell -ExecutionPolicy Bypass -File scripts\run.ps1` |

5. Open <http://localhost:8501>. Stop the app with `Ctrl+C`.

You can also run these from VS Code: **Terminal → Run Task…** → *Setup*, *Run app*, or *Run tests*.

The app reloads every time you save a file.

## Project layout

```
streamlit_app.py     The page: grade table on the left, chat box on the right
ui/                  The two parts of the page; this is where your tasks are
  grade_table.py       Tasks 1–3: GPA summary, course table, add and edit courses
  chat.py              Tasks 4–5: the chat box
lib/                 Finished logic (no need to change it)
  state.py             Session state: every key and default value in one place
  messaging.py         Message model and chat rendering
  gpa.py               GPA math: grade points, GPA, what-if, points needed
  bot.py               The chat bot: works out the question and builds an answer
data/courses.csv     Starting classes (replace them with your own)
tests/               Tests (run with: uv run pytest)
scripts/             Setup and run scripts for each OS
```

### How GPA works

Each letter grade is worth points on a 4.0 scale (A = 4.0, A- = 3.7, B+ = 3.3, ... F = 0).
Your GPA is the average of those points, weighted by credits:

```
GPA = sum(points × credits) / sum(credits)
```

Classes without a grade are "in progress" and don't count until they're graded.

Useful functions from `lib/gpa.py`:

```python
gpa.gpa(courses)                    # your GPA, or None if nothing is graded
gpa.graded(courses)                 # only classes with a grade
gpa.in_progress(courses)            # only classes without a grade
gpa.grade_points("B+")              # 3.3
gpa.GRADE_POINTS                    # {"A": 4.0, "A-": 3.7, ...}
gpa.IN_PROGRESS                     # "In progress"
```

### How state works

Streamlit reruns `streamlit_app.py` from top to bottom on every click or message.
Regular variables are reset each time, so anything the app must remember goes in session state:

```python
from lib import state

state.get(state.COURSES)             # read
state.set(state.COURSES, new_table)  # write
state.reset(state.MESSAGES)          # back to default
```

To add new state, add a key and default to `DEFAULTS` in `lib/state.py`.

### How messaging works

```python
from lib import messaging

messaging.add_message("user", "hi")     # store a message
messaging.render_history()              # draw all messages
```

### How the bot works

`bot.reply(prompt, courses)` does three steps:

1. `detect_intent()` matches keywords to decide the kind of question (`help`, `what_if`, `need`, `courses`, `gpa`).
2. `find_course()`, `find_letter()`, and `find_target_gpa()` pull details out of the question.
3. An `answer_*()` function builds the reply.

## Debugging

Press **F5** (or **Run → Start Debugging**) and pick *Debug Streamlit app*.
Set a breakpoint by clicking left of a line number, then send a message in the app.
A good first breakpoint: the first line of `reply()` in `lib/bot.py`.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `uv: command not found` after setup | Close the terminal and open a new one. |
| `permission denied: ./scripts/setup.sh` | Run `bash scripts/setup.sh` instead. |
| `Port 8501 is already in use` | The app is already running. Use that tab, or stop it with `Ctrl+C` in its terminal. |
| VS Code shows import errors | **Ctrl+Shift+P** → *Python: Select Interpreter* → choose the one in `.venv`. |
| Codespace preview is blank | **Ports** tab → right-click 8501 → *Open in Browser*. |
