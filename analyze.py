from datetime import date, datetime, timedelta

import questionary
import tabulate as tb
from termcolor import colored

import db
import habits as hb

def habit_overview():
    habits = db.get_habits()
    habit_list = []

    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_analyze = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_analyze.split(":")[0].strip()

    periodicity = db.get_habit_periodicity(habit_id)
    completions = db.get_completions(habit_id)

    habit_completions = []
    
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])
    
    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")

    habit_status = []

    for completion in habit_completions:
        completion_date = completion[0]
        habit_status.append([completion_date, "Completed"])
        next_completion_date = completion_date + timedelta(days=periodicity)
        habit_status.append([next_completion_date, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")


def show_habit_completions(habit_id):
    completions = db.get_completions(habit_id)
    habit_completions = []

    for completion in completions:
        completion_date = datetime.strptime(completion[1], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])
    
    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")


def habit_status():
    habits = db.get_habits()
    habit_list = []

    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_analyze = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_analyze.split(":")[0].strip()

    periodicity = db.get_habit_periodicity(habit_id)
    completions = db.get_completions(habit_id)

    habit_completions = []
    
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])
    
    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")

    habit_status = []

    for completion in habit_completions:
        completion_date = completion[0]
        habit_status.append([completion_date, "Completed"])
        next_completion_date = completion_date + timedelta(days=periodicity)
        habit_status.append([next_completion_date, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")


def habit_streaks():
    habits = db.get_habits()
    habit_list = []

    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_analyze = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_analyze.split(":")[0].strip()

    periodicity = db.get_habit_periodicity(habit_id)
    completions = db.get_completions(habit_id)

    habit_completions = []
    
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])
    
    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")

    habit_status = []

    for completion in habit_completions:
        completion_date = completion[0]
        habit_status.append([completion_date, "Completed"])
        next_completion_date = completion_date + timedelta(days=periodicity)
        habit_status.append([next_completion_date, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")

    streaks = []

    for status in habit_status:
        if status[1] == "Completed":
            streaks.append(status[0])
        else:
            streaks.append(status[0])
            streaks.append(status[0])
    
    streaks.append(status[0])
    streaks.append(status[0])

    print(streaks)

    streaks_analysis = []

    for i in range(0, len(streaks), 2):
        streak_start = streaks[i]
        streak_end = streaks[i+1]
        streak_length = streak_end - streak_start
        streaks_analysis.append([streak_start, streak_end, streak_length.days])
    
    print(tb.tabulate(streaks_analysis, tablefmt="fancy_grid"))
    print("\n")



def habit_completion_status():
    habits = db.get_habits()
    habit_list = []

    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_analyze = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_analyze.split(":")[0].strip()

    periodicity = db.get_habit_periodicity(habit_id)
    completions = db.get_completions(habit_id)

    habit_completions = []
    
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])
    
    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")

    habit_status = []

    for completion in habit_completions:
        completion_date = completion[0]
        habit_status.append([completion_date, "Completed"])
        next_completion_date = completion_date + timedelta(days=periodicity)
        habit_status.append([next_completion_date, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")

    today = date.today()
    habit_status.append([today, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")

    for status in habit_status:
        if status[0] == today:
            if status[1] == "Completed":
                print(colored("You completed this habit today!", "green"))
            else:
                print(colored("You did not complete this habit today!", "red"))


def habit_completion_status():
    habits = db.get_habits()
    habit_list = []

    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_analyze = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_analyze.split(":")[0].strip()

    periodicity = db.get_habit_periodicity(habit_id)
    completions = db.get_completions(habit_id)

    habit_completions = []
    
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])
    
    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")

    habit_status = []

    for completion in habit_completions:
        completion_date = completion[0]
        habit_status.append([completion_date, "Completed"])
        next_completion_date = completion_date + timedelta(days=periodicity)
        habit_status.append([next_completion_date, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")

    today = date.today()
    habit_status.append([today, "Incomplete"])

    print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
    print("\n")

    for status in habit_status:
        if status[0] == today:
            if status[1] == "Completed":
                print(colored("You completed this habit today!", "green"))
            else:
                print(colored("You did not complete this habit today!", "red"))





# def habits_overview():
#     habits = db.get_habits()
#     headers = ["ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions"]
#     print(tb.tabulate(habits, headers, tablefmt="fancy_grid"))

# def habit_overview():
#     habits = db.get_habits()
#     habit_list = []

#     for habit in habits:
#         habit_list.append(f"{habit[0]}: {habit[1]}")
#     habit_to_analyze = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
#     habit_id = habit_to_analyze.split(":")[0].strip()

#     periodicity = db.get_habit_periodicity(habit_id)
#     completions = db.get_completions(habit_id)

#     habit_completions = []
    
#     for completion in completions:
#         completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
#         habit_completions.append([completion_date, "Completed"])
    
#     print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
#     print("\n")

#     habit_status = []

#     for completion in habit_completions:
#         completion_date = completion[0]
#         habit_status.append([completion_date, "Completed"])
#         next_completion_date = completion_date + timedelta(days=periodicity)
#         habit_status.append([next_completion_date, "Incomplete"])

#     print(tb.tabulate(habit_status, tablefmt="fancy_grid"))
#     print("\n")


# def show_habit_completions(habit_id):
#     completions = db.get_completions(habit_id)
#     habit_completions = []

#     for completion in completions:
#         completion_date = datetime.strptime(completion[1], '%Y-%m-%d %H:%M:%S').date()
#         habit_completions.append([completion_date, "Completed"])
    
#     print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
#     print("\n")



# def habit_status():
#     habits = db.get_habits()
#     habit_list = []

#     for habit in habits:
#         habit_list.append(f"{habit[0]}: {habit[1]}")
#     habit_to_mark = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
#     habit_id = habit_to_mark.split(":")[0].strip()

#     conn = db.create_connection()
#     conn, c = conn
#     c.execute("SELECT * FROM habits WHERE id=?", (habit_id,))
#     habit = c.fetchone()
    
#     habit_name = habit[1]
#     period = habit[2]
#     creation_date = habit[3]
#     last_completion_date = habit[4]
#     if last_completion_date:
#         last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d %H:%M:%S').date()
#     number_of_completions = habit[5]
#     days_since_last_completion = 0

#     if last_completion_date != None:
#         days_since_last_completion = (date.today() - last_completion_date).days

#         if period == 1 and days_since_last_completion > 0:
#             print("You have broken the habit '{}' since it has been {} days since the last completion.\n".format(habit_name, days_since_last_completion))
#             pass
#         elif period == 7 and days_since_last_completion > 7:
#             print("You have broken the habit '{}' since it has been {} days since the last completion.\n".format(habit_name, days_since_last_completion))
#             pass
#         elif period == 30 and days_since_last_completion > 30:
#             print("You have broken the habit '{}' since it has been {} days since the last completion.\n".format(habit_name, days_since_last_completion))
#             pass
#         else:
#             print("You have compeleted your habit within it's period. It's great, keep going!")

#     else:
#         print(f"Habit: {habit_name} has not been completed yet.")
    
#     show_habit_completions(habit_id)
#     print("="*35)
#     print("Habit: {}".format(habit_name))
#     print("Period: {}".format(period))
#     print("Last completion: {}".format(last_completion_date))
#     print("Number of completion(s): {}".format(number_of_completions))
#     print("Days since last completion: {}".format(days_since_last_completion))
#     print("="*35)




# def habit_streaks():
#     habits = db.get_habits()
#     headers = ["ID", "Habit Name", "Periodicity", "Current Streak", "Max Streak"]
#     habit_list = []

#     for habit in habits:
#         habit_id = habit[0]
#         habit_name = habit[1]
#         periodicity = habit[2]
#         current_streak, max_streak = longest_streak(habit_id)
#         habit_list.append([habit_id, habit_name, periodicity, current_streak, max_streak])
    
    
#     print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))



# def longest_streak(habit_id):
#     completions = db.get_completions(habit_id)
#     habit_periodicity = db.get_habit_periodicity(habit_id)
#     max_streak = 0
#     current_streak = 0
#     # if completions == None:
#     #     current_streak = 0
#     # else:
#     #     current_streak = 1


#     for i in range(1, len(completions)):
#         date1 = datetime.strptime(completions[i-1][0], '%Y-%m-%d %H:%M:%S').date()
#         date2 = datetime.strptime(completions[i][0], '%Y-%m-%d %H:%M:%S').date()
#         time_delta = (date2 - date1).days
        
#         if habit_periodicity == 1:
#             if time_delta <= 1:
#                 current_streak += 1
#                 if current_streak > max_streak:
#                     max_streak = current_streak

#             else:
#                 current_streak = 0
                
#         elif habit_periodicity == 7:
#             if time_delta <= 7:
#                 current_streak += 1
#                 if current_streak > max_streak:
#                     max_streak = current_streak
#             else:
#                 current_streak = 0
                
#         elif habit_periodicity == 30:
#             if time_delta <= 30:
#                 current_streak += 1
#                 if current_streak > max_streak:
#                     max_streak = current_streak
#             else:
#                 current_streak = 0
                
#     return current_streak, max_streak



# def analyze_habits(period):
#     habits = db.get_habits()
#     print(colored("Habit name\tCreation date\t\t\tLast completion date\t\tNumber of completions", 'yellow'))
#     for habit in habits:
#         habit_name = habit[1]
#         creation_date = habit[3]
#         last_completion_date = habit[4] if habit[4] else '-'
#         number_of_completions = habit[5]
#         if period == '1':
#             if last_completion_date != '-':
#                 print(colored(f"{habit_name}\t\t{creation_date}\t\t{last_completion_date}\t\t{number_of_completions}", 'green'))
#         else:
#             print(colored(f"{habit_name}\t\t{creation_date}\t\t{last_completion_date}\t\t{number_of_completions}", 'red'))