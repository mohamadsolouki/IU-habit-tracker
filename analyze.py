from datetime import date, datetime, timedelta
import questionary
import tabulate as tb
import termcolor
from dateutil.utils import today

import db

db = db.Database()


def habits_todo():
    """
    This function prints the habits that are due today.
    """
    habits = db.get_habits()
    headers = ["ID", "Habit Name", "Periodicity", "Last Completion"]
    habit_list = []
    today = date.today()
    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]
        periodicity = habit[2]
        last_completion_date = habit[4]
        if last_completion_date is None:
            habit_list.append([habit_id, habit_name, periodicity, "Never"])
            continue
        last_completion_date_str = last_completion_date.split(" ")[0]
        last_completion_date = datetime.strptime(last_completion_date_str, '%Y-%m-%d').date()
        if (today - last_completion_date).days >= periodicity:
            habit_list.append([habit_id, habit_name, periodicity, last_completion_date])
    if not habit_list:
        print(termcolor.colored("You don't have any habits to do today!", "red"))
        return
    print(tb.tabulate(habit_list, headers, tablefmt="fancy_grid"))


def habits_overview():
    """
    This function prints the habits overview.
    """
    habits = db.get_habits()
    headers = ["ID", "Habit Name", "Periodicity", "Creation Date", "Last Completion Date", "Number of Completions"]
    print(tb.tabulate(habits, headers, tablefmt="fancy_grid"))


def habit_status():
    """
    This function prints the status of a habit.
    """
    habits = db.get_habits()
    habit_list = []

    if len(habits) == 0:
        print(termcolor.colored("You don't have any habits yet!", "red"))
        return

    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_mark = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_mark.split(":")[0].strip()

    habit = db.get_habit(habit_id)
    habit_name = habit[1]
    period = habit[2]
    creation_date = habit[3]
    last_completion_date = habit[4]
    if last_completion_date:
        last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d %H:%M:%S').date()
    number_of_completions = habit[5]
    days_since_last_completion = 0

    if last_completion_date is not None:
        days_since_last_completion = (date.today() - last_completion_date).days

        if period == 1 and days_since_last_completion > 0:
            print("You have broken the habit '{}' since it has been {} days since the last completion.\n".format(
                habit_name, days_since_last_completion))
            pass
        elif period == 7 and days_since_last_completion > 7:
            print("You have broken the habit '{}' since it has been {} days since the last completion.\n".format(
                habit_name, days_since_last_completion))
            pass
        elif period == 30 and days_since_last_completion > 30:
            print("You have broken the habit '{}' since it has been {} days since the last completion.\n".format(
                habit_name, days_since_last_completion))
            pass
        else:
            print("You have completed your habit within it's period. It's great, keep going!")

    else:
        print(f"Habit: {habit_name} has not been completed yet.")

    print("=" * 35)
    print("Habit: {}".format(habit_name))
    print("Period: {}".format(period))
    print("Last completion: {}".format(last_completion_date))
    print("Number of completion(s): {}".format(number_of_completions))
    print("Days since last completion: {}".format(days_since_last_completion))
    print("=" * 35)


def show_habit_streaks():
    """
    This function prints the streaks of all habits.
    :return:
    """
    habits = db.get_habits()
    streaks = db.get_streaks()
    headers = ["habit_id", "habit_name", "periodicity", "current_streak", "max_streak"]
    show_list = []
    streak_list = []

    for streak in streaks:
        habit_id = streak[1]
        current_streak = streak[2]
        max_streak = streak[3]
        streak_list.append([habit_id, current_streak, max_streak])

    for habit in habits:
        habit_id = habit[0]
        habit_name = habit[1]
        periodicity = habit[2]
        for streak in streak_list:
            if streak[0] == habit_id:
                show_list.append([habit_id, habit_name, periodicity, streak[1], streak[2]])
                break

    print(tb.tabulate(show_list, headers, tablefmt="fancy_grid"))


def calculate_streak(habit_id):
    completions = db.get_habit_completions(habit_id)
    habit_periodicity = db.get_habit_periodicity(habit_id)
    habit_completions = []

    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append(completion_date)

    habit_completions.sort()
    current_streak = 0
    max_streak = 0
    for i in range(len(habit_completions)):
        if i == 0:
            current_streak = 1
            max_streak = 1
            continue
        if (habit_completions[i] - habit_completions[i - 1]).days < habit_periodicity:
            current_streak += 1
            if current_streak > max_streak:
                max_streak = current_streak
        else:
            current_streak = 1

    return current_streak, max_streak







def show_habit_completions(habit_id):
    completions = db.get_habit_completions(habit_id)
    habit_completions = []

    for completion in completions:
        completion_date = datetime.strptime(completion[1], '%Y-%m-%d %H:%M:%S').date()
        habit_completions.append([completion_date, "Completed"])

    print(tb.tabulate(habit_completions, tablefmt="fancy_grid"))
    print("\n")
