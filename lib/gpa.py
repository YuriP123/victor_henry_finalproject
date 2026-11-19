"""GPA calculations.

Plain Python and pandas only, no Streamlit, so every function is easy to test.

The course table has three columns:
    course   name of the class, e.g. "Biology"
    credits  how many credits it's worth, e.g. 4
    grade    letter grade, e.g. "B+". Blank means the class is still in progress.

GPA = sum(grade points x credits) / sum(credits), counting only graded classes.
"""

from __future__ import annotations

import math
from pathlib import Path

import pandas as pd

DATA_PATH = Path(__file__).parent.parent / "data" / "courses.csv"
COLUMNS = ["course", "credits", "grade"]

# Points for each letter grade on a 4.0 scale, best first.
GRADE_POINTS: dict[str, float] = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "F": 0.0,
}

# What to show (and pick in a dropdown) for a class without a grade yet.
IN_PROGRESS = "In progress"


def load_courses(path: Path = DATA_PATH) -> pd.DataFrame:
    """Read the course table from a CSV file."""
    return pd.read_csv(path)


def grade_points(grade: object) -> float | None:
    """Points for a letter grade ("b+" -> 3.3). Blank or unknown -> None."""
    if not isinstance(grade, str):
        return None
    return GRADE_POINTS.get(grade.strip().upper())


def graded(courses: pd.DataFrame) -> pd.DataFrame:
    """Only the classes that have a grade."""
    return courses[courses["grade"].map(grade_points).notna()]


def in_progress(courses: pd.DataFrame) -> pd.DataFrame:
    """Only the classes that don't have a grade yet."""
    return courses[courses["grade"].map(grade_points).isna()]


def quality_points(courses: pd.DataFrame) -> float:
    """Sum of grade points x credits for the graded classes."""
    done = graded(courses)
    return float((done["grade"].map(grade_points) * done["credits"]).sum())


def gpa(courses: pd.DataFrame) -> float | None:
    """GPA of the graded classes, or None if nothing is graded yet."""
    credits = graded(courses)["credits"].sum()
    if credits == 0:
        return None
    return quality_points(courses) / credits


def gpa_if(courses: pd.DataFrame, course: str, grade: str) -> float | None:
    """GPA if ``course`` ended with ``grade`` (for "what if" questions)."""
    changed = courses.copy()
    changed.loc[changed["course"] == course, "grade"] = grade
    return gpa(changed)


def best_possible_gpa(courses: pd.DataFrame) -> float | None:
    """GPA if every class in progress ends with an A."""
    changed = courses.copy()
    changed.loc[changed["grade"].map(grade_points).isna(), "grade"] = "A"
    return gpa(changed)


def points_needed(courses: pd.DataFrame, target: float) -> float | None:
    """Average grade points needed in the in-progress classes to reach ``target``.

    Returns None if no classes are in progress. The result can be above 4.0
    (target out of reach) or 0 and below (target already safe).

    Math: target = (quality_points + needed * credits_left) / all_credits
          so needed = (target * all_credits - quality_points) / credits_left
    """
    credits_left = in_progress(courses)["credits"].sum()
    if credits_left == 0:
        return None
    all_credits = graded(courses)["credits"].sum() + credits_left
    return (target * all_credits - quality_points(courses)) / credits_left


def min_letter(points: float) -> str | None:
    """Lowest letter worth at least ``points``. None if above 4.0."""
    for letter, value in reversed(GRADE_POINTS.items()):
        if value >= points - 1e-9:
            return letter
    return None


def add_points_column(courses: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of the table with a "points" column added."""
    courses = courses.copy()
    courses["points"] = courses["grade"].map(grade_points)
    return courses
