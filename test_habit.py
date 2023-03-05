import habits as hb
import db

hb = hb.Habit()
db = db.Database("test.db")


def get_db(name="test.db"):
    return db.Database(name)


# test adding 6 predefined habits
def test_add_habit():
    hb.add_habit("Study", 1, '2023-01-01 01:00:00', "test.db")
    hb.add_habit("Workout", 1, '2023-01-05 01:00:00', "test.db")
    hb.add_habit("Swim", 7, '2023-01-08 01:00:00', "test.db")
    hb.add_habit("Programming", 1, '2023-01-04 01:00:00', "test.db")
    hb.add_habit("Travel", 30, '2023-01-02 01:00:00', "test.db")
    assert db.get_habit(1) == (1, "Study", 1, '2023-01-01 01:00:00', None, 0)
    assert db.get_habit(2) == (2, "Workout", 1, '2023-01-05 01:00:00', None, 0)
    assert db.get_habit(3) == (3, "Swim", 7, '2023-01-08 01:00:00', None, 0)
    assert db.get_habit(4) == (4, "Programming", 1, '2023-01-04 01:00:00', None, 0)
    assert db.get_habit(5) == (5, "Travel", 30, '2023-01-02 01:00:00', None, 0)


# test marking a daily habit as complete for 2 consecutive days
def test_mark_daily_as_complete_two_consecutive_days():
    hb.mark_habit_as_complete(1, '2023-01-02 01:00:00', "test.db")
    hb.mark_habit_as_complete(1, '2023-01-03 01:00:00', "test.db")
    assert db.get_habit_completions(1) == [('2023-01-02 01:00:00',), ('2023-01-03 01:00:00',)]


def test_mark_daily_as_complete_five_consecutive_days():
    hb.mark_habit_as_complete(2, '2023-02-02 01:00:00', "test.db")
    hb.mark_habit_as_complete(2, '2023-02-03 01:00:00', "test.db")
    hb.mark_habit_as_complete(2, '2023-02-04 01:00:00', "test.db")
    hb.mark_habit_as_complete(2, '2023-02-05 01:00:00', "test.db")
    hb.mark_habit_as_complete(2, '2023-02-06 01:00:00', "test.db")
    assert db.get_habit_completions(2) == [('2023-02-02 01:00:00',), ('2023-02-03 01:00:00',), ('2023-02-04 01:00:00',),
                                           ('2023-02-05 01:00:00',), ('2023-02-06 01:00:00',)]


# test marking a weekly habit as complete for 3 consecutive weeks
def test_mark_weekly_as_complete_three_consecutive_weeks():
    hb.mark_habit_as_complete(3, '2023-01-11 01:00:00')
    hb.mark_habit_as_complete(3, '2023-01-18 01:00:00')
    hb.mark_habit_as_complete(3, '2023-01-24 01:00:00')
    assert db.get_habit_completions(3) == [('2023-01-11 01:00:00',), ('2023-01-18 01:00:00',), ('2023-01-24 01:00:00',)]


# test marking a daily habit as complete for 6 times which has current streak of 0 and longest streak of 4
def test_mark_habit_as_complete():
    hb.mark_habit_as_complete(4, "2023-01-08 01:00:00", "test.db")
    hb.mark_habit_as_complete(4, "2023-01-09 01:00:00", "test.db")
    hb.mark_habit_as_complete(4, "2023-01-10 01:00:00", "test.db")
    hb.mark_habit_as_complete(4, "2023-01-11 01:00:00", "test.db")
    hb.mark_habit_as_complete(4, "2023-01-13 01:00:00", "test.db")
    hb.mark_habit_as_complete(4, "2023-01-14 01:00:00", "test.db")
    assert db.get_updated_streaks(4) == (4, 4, 0, 4)


# test deleting a habit
def test_delete_habit():
    hb.delete_habit(1, "test.db")
    assert db.get_habit(1) is None


def test_get_habit():
    assert db.get_habit(2) == (2, "Workout", 1, '2023-01-05 01:00:00', None, 0)
    assert db.get_habit(3) == (3, "Swim", 7, '2023-01-08 01:00:00', None, 0)
    assert db.get_habit(4) == (4, "Programming", 1, '2023-01-04 01:00:00', None, 0)
    assert db.get_habit(5) == (5, "Travel", 30, '2023-01-02 01:00:00', None, 0)
