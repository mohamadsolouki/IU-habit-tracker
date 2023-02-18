import questionary
import termcolor
import analyze
import db

db = db.Database()


class Habit:
    def __init__(self, id=None, name=None, periodicity=None):
        self.id = id
        self.name = name
        self.periodicity = periodicity

    def add_habit(self):
        """
        This method adds a habit to the database.
        """
        self.name = questionary.text("What is the habit name?").ask()
        self.periodicity = questionary.select("What is the habit periodicity?", choices=[
            {"name": "Daily", "value": 1},
            {"name": "Weekly", "value": 7},
            {"name": "Monthly", "value": 30}
        ]).ask()
        conn = db.create_connection()
        conn, c = conn
        c.execute("""INSERT INTO habits 
                (habit_name, periodicity, creation_date) 
                VALUES (?, ?, datetime('now'))
                """, (self.name, self.periodicity,))
        c.execute("""INSERT INTO streaks
                (habit_id, current_streak, longest_streak)
                VALUES (?, 0, 0)
                """, (c.lastrowid,))
        conn.commit()
        conn.close()
        print(termcolor.colored("Habit added successfully!", "green"))

    def mark_habit_as_complete(self):
        """
        This method marks a habit as complete in the database.
        """
        habits = db.get_habits()
        habit_list = []
        if len(habits) == 0:
            print(termcolor.colored("There are no habits to mark as complete!", "red"))
            return
        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_to_mark = questionary.select("Which habit would you like to mark?", choices=habit_list).ask()
        self.id = habit_to_mark.split(":")[0].strip()
        conn = db.create_connection()
        conn, c = conn
        c.execute("""UPDATE habits SET 
                last_completion_date = datetime('now','localtime'), 
                number_of_completions = number_of_completions + 1
                WHERE id = ?
                """, (self.id,))
        c.execute("""INSERT INTO completions
                (habit_id, completion_date)
                VALUES (?, datetime('now','localtime'))
                """, (self.id,))
        current_streak, longest_streak = analyze.calculate_streak(self.id)
        c.execute("""UPDATE streaks SET
                current_streak = ?,
                longest_streak = ?
                WHERE habit_id = ?
                """, (current_streak, longest_streak, self.id,))
        conn.commit()
        conn.close()
        print(termcolor.colored("Habit has been marked as complete!", "green"))

    def delete_habit(self):
        """
        This method deletes a habit from the database.
        """
        habits = db.get_habits()
        habit_list = []
        if len(habits) == 0:
            print(termcolor.colored("There are no habits to delete!", "red"))
            return
        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_list.append({"name": "Go back to main menu", "value": "back"})
        habit_to_delete = questionary.select("Which habit would you like to delete?", choices=habit_list).ask()
        if habit_to_delete == "back":
            return
        self.id = habit_to_delete.split(":")[0].strip()
        conn = db.create_connection()
        conn, c = conn
        c.execute("""DELETE FROM habits WHERE id = ?""", (self.id,))
        c.execute("""DELETE FROM streaks WHERE habit_id = ?""", (self.id,))
        c.execute("""DELETE FROM completions WHERE habit_id = ?""", (self.id,))
        conn.commit()
        conn.close()

        print(termcolor.colored("Habit deleted!", "red"))


