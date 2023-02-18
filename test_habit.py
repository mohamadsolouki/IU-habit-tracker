import pytest
from datetime import date, timedelta
import habits
import db

db = db.Database()


def test_streak_calculation():
    # Create a HabitTracker object and add a new habit
    habit_tracker = habits.Habit()
    habit_tracker.add_habit("Test habit", 1)

    # Mark the habit as complete for the past 10 days
    today = date.today()
    for i in range(10):
        completion_date = today - timedelta(days=i)
        habit_tracker.mark_habit_as_complete(1, completion_date)

    # Check that the current streak is 10 and the longest streak is also 10
    db.__init__()
    db.c.execute("SELECT current_streak, longest_streak FROM streaks WHERE habit_id=?", (1,))
    row = db.c.fetchone()
    assert row[0] == 10
    assert row[1] == 10

    # Mark the habit as incomplete for the last 3 days
    for i in range(3):
        completion_date = today - timedelta(days=i)
        habit_tracker.mark_habit_as_complete(1, completion_date)

    # Check that the current streak is now 0 and the longest streak is still 10
    db.__init__()
    db.c.execute("SELECT current_streak, longest_streak FROM streaks WHERE habit_id=?", (1,))
    row = db.c.fetchone()
    assert row[0] == 0
    assert row[1] == 10
    # habit = habit_tracker.get_habit_by_name("Test habit")
    # assert habit.current_streak == 0
    # assert habit.longest_streak == 10
