import habits as hb
import db

hb = hb.Habit()
db = db.Database()


def test_add_habit():
    hb.add_habit("Test habit", 1, '2023-01-01')
    assert db.get_habit(1) == (1, "Test habit", 1, '2023-01-01', None, 0)


def test_mark_habit_as_complete_two_consecutive_days():
    hb.mark_habit_as_complete(1, '2023-01-02')
    hb.mark_habit_as_complete(1, '2023-01-03')
    assert db.get_habit_completions(1) == [('2023-01-02',), ('2023-01-03',)]


# test marking a daily habit as complete for 7 days which has current streak of 3 and longest streak of 4
def test_mark_habit_as_complete():
    hb.mark_habit_as_complete(1, "2023-01-08")
    hb.mark_habit_as_complete(1, "2023-01-09")
    hb.mark_habit_as_complete(1, "2023-01-10")
    hb.mark_habit_as_complete(1, "2023-01-11")
    hb.mark_habit_as_complete(1, "2023-01-13")
    hb.mark_habit_as_complete(1, "2023-01-14")
    assert db.get_streaks_for_habit(1) == (1, 1, 2, 4)

