import termcolor
import db
from datetime import datetime

db = db.Database()


class Habit:
    def __init__(self, habit_id=None, name=None, periodicity=None, creation_date=None, completion_date=None):
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_date = completion_date

    def add_habit(self, name, periodicity, creation_date):
        db.__init__()
        db.c.execute("INSERT INTO habits (habit_name, periodicity, creation_date) VALUES (?, ?, ?)",
                     (name, periodicity, creation_date))
        self.habit_id = db.c.lastrowid
        db.c.execute("INSERT INTO streaks (habit_id, current_streak, longest_streak) VALUES (?, ?, ?)",
                     (self.habit_id, 0, 0))
        db.conn.commit()
        db.conn.close()
        print(termcolor.colored("Habit added successfully!", "green"))

    def mark_habit_as_complete(self, habit_id, completion_date):
        db.__init__()
        self.habit_id = habit_id
        self.completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        last_completion_date = db.get_habit(self.habit_id)[4]
        periodicity = db.get_habit_periodicity(self.habit_id)
        if last_completion_date:
            last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d').date()
            if (self.completion_date - last_completion_date).days < periodicity:
                print(termcolor.colored("Habit has already been marked as complete within it's period!", "red"))
                return
        db.c.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)",
                     (self.habit_id, self.completion_date))
        db.c.execute(
            "UPDATE habits SET last_completion_date=?, number_of_completions=number_of_completions+1 WHERE id=?",
            (self.completion_date, self.habit_id))
        db.conn.commit()

        # Check if habit has previous completions
        db.c.execute("SELECT last_completion_date FROM habits WHERE id=?", (self.habit_id,))
        row = db.c.fetchone()
        if not row[0]:
            return

        # Calculate current streak and longest streak
        db.c.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date DESC LIMIT 2",
                     (self.habit_id,))
        rows = db.c.fetchall()
        completion_list = []
        for row in rows:
            completion_list.append(datetime.strptime(row[0], '%Y-%m-%d').date())
        current_streak = db.get_streaks_for_habit(self.habit_id)[2]
        longest_streak = db.get_streaks_for_habit(self.habit_id)[3]
        if len(completion_list) == 1:
            current_streak = 1
            longest_streak = 1
        else:
            prev_date = completion_list[1]
            current_date = completion_list[0]
            if (current_date - prev_date).days <= periodicity:
                current_streak += 1
                if current_streak > longest_streak:
                    longest_streak = current_streak
            else:
                current_streak = 1

        # Update streaks table
        db.c.execute("UPDATE streaks SET current_streak=?, longest_streak=? WHERE habit_id=?",
                     (current_streak, longest_streak, self.habit_id))
        db.conn.commit()
        db.conn.close()
        print(termcolor.colored("Habit has been marked as complete!", "green"))

    def delete_habit(self, habit_id):
        """
        This method deletes a habit from the database.
        """
        db.__init__()
        self.habit_id = habit_id
        db.c.execute("""DELETE FROM habits WHERE id = ?""", (self.habit_id,))
        db.c.execute("""DELETE FROM streaks WHERE habit_id = ?""", (self.habit_id,))
        db.c.execute("""DELETE FROM completions WHERE habit_id = ?""", (self.habit_id,))
        db.conn.commit()
        db.conn.close()
        print(termcolor.colored("Habit deleted!", "red"))
