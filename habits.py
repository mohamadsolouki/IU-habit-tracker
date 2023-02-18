import termcolor
import db
from datetime import date, datetime

db = db.Database()


class Habit:
    def __init__(self, habit_id=None, name=None, periodicity=None, completion_date=None):
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.completion_date = completion_date

    def add_habit(self, name, periodicity):
        db.__init__()
        today = date.today()
        db.c.execute("INSERT INTO habits (habit_name, periodicity, creation_date) VALUES (?, ?, ?)",
                     (name, periodicity, today))
        self.habit_id = db.c.lastrowid
        db.c.execute("INSERT INTO streaks (habit_id, current_streak, longest_streak) VALUES (?, ?, ?)",
                     (self.habit_id, 0, 0))
        db.conn.commit()
        db.conn.close()
        print(termcolor.colored("Habit added successfully!", "green"))

    def mark_habit_as_complete(self, habit_id, completion_date):
        db.__init__()
        db.c.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)", (habit_id, completion_date))
        db.c.execute(
            "UPDATE habits SET last_completion_date=?, number_of_completions=number_of_completions+1 WHERE id=?",
            (completion_date, habit_id))
        db.conn.commit()

        # Check if habit has previous completions
        db.c.execute("SELECT last_completion_date FROM habits WHERE id=?", (habit_id,))
        row = db.c.fetchone()
        if not row[0]:
            return

        # Calculate current streak and longest streak
        db.c.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date DESC",
                     (habit_id,))
        rows = db.c.fetchall()
        current_streak = 1
        longest_streak = 1
        prev_date = datetime.strptime(rows[0][0], '%Y-%m-%d').date()
        for row in rows[1:]:
            curr_date = datetime.strptime(row[0], '%Y-%m-%d').date()
            date_diff = (prev_date - curr_date).days
            if date_diff == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            elif date_diff > 1:
                break
            prev_date = curr_date

        # Update streaks table
        db.c.execute("UPDATE streaks SET current_streak=?, longest_streak=? WHERE habit_id=?",
                     (current_streak, longest_streak, habit_id))
        db.conn.commit()
        db.conn.close()
        print(termcolor.colored("Habit has been marked as complete!", "green"))

    def delete_habit(self, habit_id):
        """
        This method deletes a habit from the database.
        """
        db.__init__()
        db.c.execute("""DELETE FROM habits WHERE id = ?""", (self.habit_id,))
        db.c.execute("""DELETE FROM streaks WHERE habit_id = ?""", (self.habit_id,))
        db.c.execute("""DELETE FROM completions WHERE habit_id = ?""", (self.habit_id,))
        db.conn.commit()
        db.conn.close()
        print(termcolor.colored("Habit deleted!", "red"))

        # def add_habit(self):
        #     """
        #     This method adds a habit to the database.
        #     """
        #     self.name = questionary.text("What is the habit name?").ask()
        #     self.periodicity = questionary.select("What is the habit periodicity?", choices=[
        #         {"name": "Daily", "value": 1},
        #         {"name": "Weekly", "value": 7},
        #         {"name": "Monthly", "value": 30}
        #     ]).ask()
        #     conn = db.create_connection()
        #     conn, c = conn
        #     c.execute("""INSERT INTO habits
        #             (habit_name, periodicity, creation_date)
        #             VALUES (?, ?, datetime('now'))
        #             """, (self.name, self.periodicity,))
        #     c.execute("""INSERT INTO streaks
        #             (habit_id, current_streak, longest_streak)
        #             VALUES (?, 0, 0)
        #             """, (c.lastrowid,))
        #     conn.commit()
        #     conn.close()
        #     print(termcolor.colored("Habit added successfully!", "green"))
        #
        # def mark_habit_as_complete(self):
        #     """
        #     This method marks a habit as complete in the database.
        #     """
        #     habits = db.get_habits()
        #     habit_list = []
        #     if len(habits) == 0:
        #         print(termcolor.colored("There are no habits to mark as complete!", "red"))
        #         return
        #     for habit in habits:
        #         habit_list.append(f"{habit[0]}: {habit[1]}")
        #     habit_to_mark = questionary.select("Which habit would you like to mark?", choices=habit_list).ask()
        #     self.id = habit_to_mark.split(":")[0].strip()
        #     conn = db.create_connection()
        #     conn, c = conn
        #     c.execute("""UPDATE habits SET
        #             last_completion_date = datetime('now','localtime'),
        #             number_of_completions = number_of_completions + 1
        #             WHERE id = ?
        #             """, (self.id,))
        #     c.execute("""INSERT INTO completions
        #             (habit_id, completion_date)
        #             VALUES (?, datetime('now','localtime'))
        #             """, (self.id,))
        #     current_streak, longest_streak = analyze.calculate_streak(self.id)
        #     c.execute("""UPDATE streaks SET
        #             current_streak = ?,
        #             longest_streak = ?
        #             WHERE habit_id = ?
        #             """, (current_streak, longest_streak, self.id,))
        #     conn.commit()
        #     conn.close()
        #     print(termcolor.colored("Habit has been marked as complete!", "green"))
