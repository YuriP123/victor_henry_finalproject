"""The GPA bot: answers chat questions about your courses.

How a reply is built:
  1. detect_intent()  works out what kind of question it is ("gpa", "need", ...)
  2. find_* helpers   pull details out of the question (course, letter, target GPA)
  3. an answer_*()    function builds the reply for that intent

To teach the bot a new kind of question:
  add keywords to INTENT_KEYWORDS, write an answer_*() function,
  and connect them in reply().
"""

from __future__ import annotations

import re

import pandas as pd

from lib import gpa

HELP_TEXT = """I can answer questions about your grades. Try:
- "What's my GPA?"
- "What do I need to get a 3.5?"
- "What if I get an A in Biology?"
- "Which classes are in progress?"

Add or change courses in the table and I'll use the new grades."""

# Example questions. The chat can show these as one-click buttons (Task 4).
SUGGESTIONS = [
    "What's my GPA?",
    "What do I need to get a 3.5?",
    "What if I get an A in Biology?",
]

# Words that signal each kind of question. They're checked in this order and
# the first match wins, so more specific intents come first.
INTENT_KEYWORDS: dict[str, list[str]] = {
    "help": ["help", "what can you do"],
    "what_if": ["what if", "if i get", "if i got"],
    "need": ["need", "reach", "to get a"],
    "courses": ["in progress", "classes", "courses", "left"],
    "gpa": ["gpa", "average", "doing", "grades"],
}


# --- Understanding the question --------------------------------------------


def detect_intent(prompt: str) -> str | None:
    """Return the first intent whose keywords appear in ``prompt``."""
    text = prompt.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return None


def find_target_gpa(prompt: str) -> float | None:
    """The GPA asked about, e.g. "get a 3.5" -> 3.5."""
    match = re.search(r"\d+(?:\.\d+)?", prompt)
    return float(match.group()) if match else None


def find_letter(prompt: str) -> str | None:
    """The letter grade asked about, e.g. "get a B+" -> "B+"."""
    words = re.findall(r"[a-z]+[+-]?", prompt.lower())
    for i, word in enumerate(words[:-1]):
        nxt = words[i + 1].upper()
        if word not in ("get", "got", "an", "a") or nxt not in gpa.GRADE_POINTS:
            continue
        # In "get a B" the "a" is an article, not the letter A.
        if nxt == "A" and i + 2 < len(words) and words[i + 2].upper() in gpa.GRADE_POINTS:
            continue
        return nxt
    return None


def find_course(prompt: str, courses: list[str]) -> str | None:
    """The course named in ``prompt``: full name, or a word of 4+ letters from it."""
    text = prompt.lower()
    words = set(re.findall(r"[a-z]+", text))
    for course in courses:
        if course.lower() in text:
            return course
    for course in courses:
        if any(len(w) >= 4 and w in words for w in re.findall(r"[a-z]+", course.lower())):
            return course
    return None


# --- Building answers -------------------------------------------------------


def answer_gpa(courses: pd.DataFrame) -> str:
    current = gpa.gpa(courses)
    if current is None:
        return "You don't have any graded classes yet. Add a class with a grade to the table."
    credits = gpa.graded(courses)["credits"].sum()
    left = len(gpa.in_progress(courses))
    answer = f"Your GPA is **{current:.2f}** across {credits:g} graded credits."
    if left:
        answer += f" {left} class{'es are' if left > 1 else ' is'} still in progress."
    return answer


def answer_need(courses: pd.DataFrame, prompt: str) -> str:
    target = find_target_gpa(prompt)
    if target is None:
        return 'What GPA are you aiming for? For example: "What do I need to get a 3.5?"'
    if not 0 <= target <= 4:
        return "GPAs go from 0.0 to 4.0. Pick a target in that range."
    needed = gpa.points_needed(courses, target)
    if needed is None:
        current = gpa.gpa(courses)
        return f"All your classes have grades, so your GPA is final at {current:.2f}."
    names = ", ".join(gpa.in_progress(courses)["course"])
    if needed > 4:
        best = gpa.best_possible_gpa(courses)
        return f"A {target:.2f} isn't reachable this term. Straight A's in {names} would get you to {best:.2f}."
    if needed <= 0:
        return f"You'll stay above {target:.2f} whatever grades you get in {names}."
    return (
        f"To reach a {target:.2f} GPA you need to average {needed:.2f} grade points in "
        f"{names}. That means **{gpa.min_letter(needed)}** or better on average."
    )


def answer_what_if(courses: pd.DataFrame, prompt: str) -> str:
    course = find_course(prompt, courses["course"].tolist())
    letter = find_letter(prompt)
    if course is None:
        return "Which class? Use its name from the table, e.g. \"What if I get an A in Biology?\""
    if letter is None:
        return f'Which grade? For example: "What if I get a B+ in {course}?"'
    new = gpa.gpa_if(courses, course, letter)
    current = gpa.gpa(courses)
    answer = f"With a {letter} in {course}, your GPA would be **{new:.2f}**"
    return answer + (f" (it's {current:.2f} now)." if current is not None else ".")


def answer_courses(courses: pd.DataFrame) -> str:
    left = gpa.in_progress(courses)
    if left.empty:
        return "All your classes have grades."
    lines = [f"- {row.course} ({row.credits:g} credits)" for row in left.itertuples()]
    return "Classes still in progress:\n" + "\n".join(lines)


# --- Putting it together ----------------------------------------------------


def reply(prompt: str, courses: pd.DataFrame) -> str:
    """Return the bot's answer to ``prompt`` about the course table."""
    intent = detect_intent(prompt)
    if intent == "help":
        return HELP_TEXT
    if intent == "what_if":
        return answer_what_if(courses, prompt)
    if intent == "need":
        return answer_need(courses, prompt)
    if intent == "courses":
        return answer_courses(courses)
    if intent == "gpa":
        return answer_gpa(courses)
    return "Sorry, I didn't understand that. Type **help** to see what I can do."
