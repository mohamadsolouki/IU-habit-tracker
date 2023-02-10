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

    def __str__(self):
        return f"{self.habit_id}: {self.habit_name}"
    
    def __repr__(self):
        return f"{self.habit_id}: {self.habit_name}"

    def get_habit_id(self):
        return self.habit_id

    def get_habit_name(self):
        return self.habit_name
    
    def get_periodicity(self):
        return self.periodicity
    
    def get_creation_date(self):
        return self.creation_date
    
    def get_last_completion_date(self):
        return self.last_completion_date

    def get_number_of_completions(self):
        return self.number_of_completions

    def get_habit_stats(self):
        habit_stats = []
        habit_stats.append(self.get_habit_name())
        habit_stats.append(self.get_periodicity())
        habit_stats.append(self.get_creation_date())
        habit_stats.append(self.get_last_completion_date())
        habit_stats.append(self.get_number_of_completions())
        habit_stats.append(self.get_current_streak())
        habit_stats.append(self.get_longest_streak())
        return habit_stats

    def get_habit_stats_table(self):
        habit_stats = self.get_habit_stats()
        habit_stats_table = tb.tabulate([habit_stats], headers=["Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions", "Current Streak", "Longest Streak"], tablefmt="fancy_grid")
        return habit_stats_table

    def get_habit_stats_table_with_id(self):
        habit_stats = self.get_habit_stats()
        habit_stats.insert(0, self.get_habit_id())
        habit_stats_table = tb.tabulate([habit_stats], headers=["Habit ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions", "Current Streak", "Longest Streak"], tablefmt="fancy_grid")
        return habit_stats_table

    def get_current_streak(self):
        current_streak = 0
        if self.get_last_completion_date() == date.today():
            current_streak = 1
        return current_streak
    
    def get_longest_streak(self):
        longest_streak = 0
        return longest_streak
    
    def mark_habit_as_complete(self):
        self.last_completion_date = date.today()
        self.number_of_completions += 1
        db.update_habit(self)

    def update_habit(self):
        db.update_habit(self)

    
    

class HabitTracker:
    def __init__(self):
        self.habits = []
    
    def add_habit(self, habit):
        self.habits.append(habit)
    
    def get_habits(self):
        return self.habits
    
    def get_habit(self, habit_id):
        for habit in self.habits:
            if habit.get_habit_id() == habit_id:
                return habit
    
    def get_habit_stats(self, habit_id):
        habit = self.get_habit(habit_id)
        habit_stats = habit.get_habit_stats()
        return habit_stats

    def get_habit_stats_table(self, habit_id):
        habit = self.get_habit(habit_id)
        habit_stats_table = habit.get_habit_stats_table()
        return habit_stats_table
    
    def get_habit_stats_table_with_id(self):
        habit_stats_table = []
        for habit in self.habits:
            habit_stats_table.append(habit.get_habit_stats_table_with_id())
        return habit_stats_table




class HabitTrackerCLI:
    def __init__(self):
        self.habit_tracker = HabitTracker()
        self.habit_tracker = self.load_habits()
    
    def load_habits(self):
        habits = db.get_habits()
        for habit in habits:
            self.habit_tracker.add_habit(Habit(habit[0], habit[1], habit[2], habit[3]))
        return self.habit_tracker

    def save_habits(self):
        pass

    def show_habit_stats(self):
        habit_stats_table = self.habit_tracker.get_habit_stats_table_with_id()
        print(habit_stats_table)

    def show_habit_stats_by_id(self):
        habit_id = questionary.text("What is the habit ID?").ask()
        habit_stats_table = self.habit_tracker.get_habit_stats_table(habit_id)
        print(habit_stats_table)

    def mark_habit_as_complete(self):
        habit_id = questionary.text("What is the habit ID?").ask()
        habit = self.habit_tracker.get_habit(habit_id)
        habit.mark_habit_as_complete()
        print(termcolor.colored("Habit marked as complete!", "green"))

    def show_menu(self):
        menu = questionary.select("What would you like to do?", choices=[
            {"name": "Show Habit Stats", "value": "show_habit_stats"},
            {"name": "Show Habit Stats by ID", "value": "show_habit_stats_by_id"},
            {"name": "Mark Habit as Complete", "value": "mark_habit_as_complete"},
            {"name": "Exit", "value": "exit"}
        ]).ask()
        return menu

    def run(self):
        while True:
            menu = self.show_menu()
            if menu == "show_habit_stats":
                self.show_habit_stats()
            elif menu == "show_habit_stats_by_id":
                self.show_habit_stats_by_id()
            elif menu == "mark_habit_as_complete":
                self.mark_habit_as_complete()
            elif menu == "exit":
                break
            else:
                print(termcolor.colored("Invalid option!", "red"))
    

class HabitTrackerDB:
    def __init__(self):
        self.conn = self.create_connection()


    

#  def get_longest_streak(self):
#         completions = db.get_completions(self.habit_id)
#         habit_periodicity = db.get_habit_periodicity(self.habit_id)
#         max_streak = 0
#         current_streak = 0

#         for i in range(1, len(completions)):
#             date1 = datetime.strptime(completions[i-1][0], '%Y-%m-%d %H:%M:%S').date()
#             date2 = datetime.strptime(completions[i][0], '%Y-%m-%d %H:%M:%S').date()
#             time_delta = (date2 - date1).days
            
#             if habit_periodicity == 1:
#                 if time_delta <= 1:
#                     current_streak += 1
#                     if current_streak > max_streak:
#                         max_streak = current_streak

#                 else:
#                     current_streak = 0
                    
#             elif habit_periodicity == 7:
#                 if time_delta <= 7:
#                     current_streak += 1
#                     if current_streak > max_streak:
#                         max_streak = current_streak
#                 else:
#                     current_streak = 0
                    
#             elif habit_periodicity == 30:
#                 if time_delta <= 30:
#                     current_streak += 1
#                     if current_streak > max_streak:
#                         max_streak = current_streak
#                 else:
#                     current_streak = 0
                    
#         return current_streak, max_streak

#     def get_current_streak(self):
#         completions = db.get_completions(self.habit_id)
#         habit_periodicity = db.get_habit_periodicity(self.habit_id)
#         current_streak = 0

#         for i in range(1, len(completions)):
#             date1 = datetime.strptime(completions[i-1][0], '%Y-%m-%d %H:%M:%S').date()
#             date2 = datetime.strptime(completions[i][0], '%Y-%m-%d %H:%M:%S').date()
#             time_delta = (date2 - date1).days
            
#             if habit_periodicity == 1:
#                 if time_delta <= 1:
#                     current_streak += 1
#                 else:
#                     current_streak = 0
                    
#             elif habit_periodicity == 7:
#                 if time_delta <= 7:
#                     current_streak += 1
#                 else:
#                     current_streak = 0
                    
#             elif habit_periodicity == 30:
#                 if time_delta <= 30:
#                     current_streak += 1
#                 else:
#                     current_streak = 0
                    
#         return current_streak


    # def add_habit(self):
    #     habit_name = questionary.text("What is the habit name?").ask()
    #     period = questionary.select("What is the habit periodicity?", choices=[
    #             {"name": "Daily", "value": 1},
    #             {"name": "Weekly", "value": 7},
    #             {"name": "Monthly", "value": 30}
    #         ]).ask()
    #     conn = db.create_connection()
    #     conn, c = conn
    #     c.execute("""INSERT INTO habits 
    #             (habit_name, periodicity, creation_date) 
    #             VALUES (?, ?, datetime('now'))
    #             """, (habit_name, period,))
    #     conn.commit()
    #     conn.close()
    #     print(termcolor.colored("Habit added successfully!", "green"))


    # def mark_habit_as_complete(self):
    #     habits = db.get_habits()
    #     habit_list = []

    #     for habit in habits:
    #         habit_list.append(f"{habit[0]}: {habit[1]}")
    #     habit_to_mark = questionary.select("Which habit would you like to mark?", choices=habit_list).ask()
    #     habit_id = habit_to_mark.split(":")[0].strip()
    #     conn = db.create_connection()
    #     conn, c = conn
    #     c.execute("""UPDATE habits SET 
    #             last_completion_date = datetime('now','localtime'), 
    #             number_of_completions = number_of_completions + 1 
    #             WHERE id = ?
    #             """, (habit_id,))
    #     c.execute("""INSERT INTO completions 
    #             (habit_id, completion_date) 
    #             VALUES (?, datetime('now', 'localtime'))
    #             """, (habit_id,))
    #     conn.commit()
    #     conn.close()
    #     print(termcolor.colored("Habit has been marked as complete!", "green"))


    # def delete_habit(self):
    #     habits = db.get_habits()
    #     habit_list = []

    #     for habit in habits:
    #         habit_list.append(f"{habit[0]}: {habit[1]}")
    #     habit_list.append({"name": "Go back to main menu", "value": "back"})
    #     habit_to_delete = questionary.select("Which habit would you like to delete?", choices=habit_list).ask()

    #     if habit_to_delete == "back":
    #         return

    #     habit_id = habit_to_delete.split(":")[0].strip()
    #     conn = db.create_connection()
    #     conn, c = conn
    #     c.execute("DELETE FROM habits WHERE id=?", (habit_id,))
    #     conn.commit()
    #     conn.close()
    #     print(termcolor.colored("Habit deleted!", "red"))



    # def habits_todo(self):
    #     habits = db.get_habits()
    #     headers = ["ID", "Habit Name", "Periodicity", "Last Completion"]
    #     habit_list = []
    #     today = date.today()
        
    #     for habit in habits:
    #         habit_id = habit[0]
    #         habit_name = habit[1]
    #         periodicity = habit[2]
    #         last_completion_date = habit[4]
    #         last_completion_date_str = last_completion_date.split(" ")[0]
    #         last_completion_date = datetime.strptime(last_completion_date_str, '%Y-%m-%d').date()
            
    #         if (today - last_completion_date).days >= periodicity:
    #             habit_list.append([habit_id, habit_name, periodicity, last_completion_date])
                
    #     if not habit_list:
    #         print(termcolor.colored("You don't have any habits to do today!", "red"))
    #         return
        
    #     print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))
