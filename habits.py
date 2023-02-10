from datetime import date, datetime

import questionary
import tabulate as tb
import termcolor

import db

class Habit:
    def __init__(self, habit_id, habit_name, periodicity, creation_date, last_completion_date, number_of_completions):
        self.habit_id = habit_id
        self.habit_name = habit_name
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.last_completion_date = last_completion_date
        self.number_of_completions = number_of_completions


    def add_habit(self):
        habit_name = questionary.text("What is the habit name?").ask()
        period = questionary.select("What is the habit periodicity?", choices=[
                {"name": "Daily", "value": 1},
                {"name": "Weekly", "value": 7},
                {"name": "Monthly", "value": 30}
            ]).ask()
        conn = db.create_connection()
        conn, c = conn
        c.execute("""INSERT INTO habits 
                (habit_name, periodicity, creation_date) 
                VALUES (?, ?, datetime('now'))
                """, (habit_name, period,))
        conn.commit()
        conn.close()
        print(termcolor.colored("Habit added successfully!", "green"))


    def mark_habit_as_complete(self):
        habits = db.get_habits()
        habit_list = []

        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_to_mark = questionary.select("Which habit would you like to mark?", choices=habit_list).ask()
        habit_id = habit_to_mark.split(":")[0].strip()
        conn = db.create_connection()
        conn, c = conn
        c.execute("""UPDATE habits SET 
                last_completion_date = datetime('now','localtime'), 
                number_of_completions = number_of_completions + 1 
                WHERE id = ?
                """, (habit_id,))
        c.execute("""INSERT INTO completions 
                (habit_id, completion_date) 
                VALUES (?, datetime('now', 'localtime'))
                """, (habit_id,))
        conn.commit()
        conn.close()
        print(termcolor.colored("Habit has been marked as complete!", "green"))


    def delete_habit(self):
        habits = db.get_habits()
        habit_list = []

        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_list.append({"name": "Go back to main menu", "value": "back"})
        habit_to_delete = questionary.select("Which habit would you like to delete?", choices=habit_list).ask()

        if habit_to_delete == "back":
            return

        habit_id = habit_to_delete.split(":")[0].strip()
        conn = db.create_connection()
        conn, c = conn
        c.execute("DELETE FROM habits WHERE id=?", (habit_id,))
        conn.commit()
        conn.close()
        print(termcolor.colored("Habit deleted!", "red"))



    def habits_todo(self):
        habits = db.get_habits()
        headers = ["ID", "Habit Name", "Periodicity", "Last Completion"]
        habit_list = []
        today = date.today()
        
        for habit in habits:
            habit_id = habit[0]
            habit_name = habit[1]
            periodicity = habit[2]
            last_completion_date = habit[4]
            last_completion_date_str = last_completion_date.split(" ")[0]
            last_completion_date = datetime.strptime(last_completion_date_str, '%Y-%m-%d').date()
            
            if (today - last_completion_date).days >= periodicity:
                habit_list.append([habit_id, habit_name, periodicity, last_completion_date])
                
        if not habit_list:
            print(termcolor.colored("You don't have any habits to do today!", "red"))
            return
        
        print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))
