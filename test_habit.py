import habits as hb
import db

hb = hb.Habit()
db = db.Database()


# test adding 5 predefined habits
def test_add_habit():
    hb.add_habit("Study", 1, '2023-01-01')
    hb.add_habit("Workout", 1, '2023-01-05')
    hb.add_habit("Swim", 7, '2023-01-08')
    hb.add_habit("Programming", 1, '2023-01-04')
    hb.add_habit("Travel", 30, '2023-01-02')
    assert db.get_habit(1) == (1, "Study", 1, '2023-01-01', None, 0)
    assert db.get_habit(2) == (2, "Workout", 1, '2023-01-05', None, 0)
    assert db.get_habit(3) == (3, "Swim", 7, '2023-01-08', None, 0)
    assert db.get_habit(4) == (4, "Programming", 1, '2023-01-04', None, 0)
    assert db.get_habit(5) == (5, "Travel", 30, '2023-01-02', None, 0)


# test marking a daily habit as complete for 2 consecutive days
def test_mark_daily_as_complete_two_consecutive_days():
    hb.mark_habit_as_complete(1, '2023-01-02')
    hb.mark_habit_as_complete(1, '2023-01-03')
    assert db.get_habit_completions(1) == [('2023-01-02',), ('2023-01-03',)]


def test_mark_daily_as_complete_five_consecutive_days():
    hb.mark_habit_as_complete(1, '2023-02-02')
    hb.mark_habit_as_complete(1, '2023-02-03')
    hb.mark_habit_as_complete(1, '2023-02-04')
    hb.mark_habit_as_complete(1, '2023-02-05')
    hb.mark_habit_as_complete(1, '2023-02-06')
    # assert db.get_habit_completions(1) == [('2023-01-02',), ('2023-01-03',)]


# test marking a weekly habit as complete for 3 consecutive weeks
def test_mark_weekly_as_complete_three_consecutive_weeks():
    hb.mark_habit_as_complete(3, '2023-01-11')
    hb.mark_habit_as_complete(3, '2023-01-18')
    hb.mark_habit_as_complete(3, '2023-01-24')
    assert db.get_habit_completions(3) == [('2023-01-11',), ('2023-01-18',), ('2023-01-24',)]


# test marking a daily habit as complete for 7 days which has current streak of 3 and longest streak of 4
def test_mark_habit_as_complete():
    hb.mark_habit_as_complete(1, "2023-01-08")
    hb.mark_habit_as_complete(1, "2023-01-09")
    hb.mark_habit_as_complete(1, "2023-01-10")
    hb.mark_habit_as_complete(1, "2023-01-11")
    hb.mark_habit_as_complete(1, "2023-01-13")
    hb.mark_habit_as_complete(1, "2023-01-14")
    assert db.get_streaks_for_habit(1) == (1, 1, 2, 4)


def test_delete_habit():
    hb.delete_habit(1)
    assert db.get_habit(1) is None


def test_get_habit():
    assert db.get_habit(2) == (2, "Workout", 1, '2023-01-05', None, 0)
    assert db.get_habit(3) == (3, "Swim", 7, '2023-01-08', None, 0)
    assert db.get_habit(4) == (4, "Programming", 1, '2023-01-04', None, 0)
    assert db.get_habit(5) == (5, "Travel", 30, '2023-01-02', None, 0)
