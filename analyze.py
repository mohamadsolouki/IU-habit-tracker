from datetime import date, datetime
import questionary
import tabulate as tb
import termcolor
import db
import habits as hb

db = db.Database()
hb = hb.Habit()


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
        # If the habit has never been completed, add it to the list
        if last_completion_date is None:
            habit_list.append([habit_id, habit_name, periodicity, "Never"])
            continue
        last_completion_date_str = last_completion_date.split(" ")[0]
        last_completion_date = datetime.strptime(last_completion_date_str, '%Y-%m-%d').date()
        # If the habit has been completed today, skip it
        if (today - last_completion_date).days >= periodicity:
            habit_list.append([habit_id, habit_name, periodicity, last_completion_date])
    # If there are no habits to do today, print a message and return
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
    # If there are no habits, print a message and return
    if len(habits) == 0:
        print(termcolor.colored("You don't have any habits yet!", "red"))
        return
    # If there are habits, add them to the habit list
    for habit in habits:
        habit_list.append(f"{habit[0]}: {habit[1]}")
    habit_to_mark = questionary.select("Which habit would you like to analyze?", choices=habit_list).ask()
    habit_id = habit_to_mark.split(":")[0].strip()
    # Get the habit from the database
    habit = db.get_habit(habit_id)
    habit_name = habit[1]
    period = habit[2]
    last_completion_date = habit[4]
    if last_completion_date:
        last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d').date()
    number_of_completions = habit[5]
    days_since_last_completion = 0
    # Check if the habit has been completed within the period
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
    # If the habit has not been completed yet, print a message
    else:
        print(f"Habit: {habit_name} has not been completed yet.")
    # Print the habit status
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


def show_habit_completions(habit_id):
    """
    This function prints the completions of a habit.
    :param habit_id: The ID of the habit.
    :return: None
    """
    # get the habit completions from the database
    completions = db.get_habit_completions(habit_id)
    habit = db.get_habit(habit_id)
    habit_completions = []
    habit_name = habit[1]
    print(f"Completions of habit *{habit_name}* in the last 30 days:")

    # print the habit completions in last month in a table format using tabulate library
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d').date()
        if (date.today() - completion_date).days <= 30:
            habit_completions.append([completion_date])
    headers = ["date of habit completion"]
    print(tb.tabulate(habit_completions, headers, tablefmt="fancy_grid"))

    # calculate the number of completions in the last 7 days
    completions_in_last_7_days = 0
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d').date()
        if (date.today() - completion_date).days <= 7:
            completions_in_last_7_days += 1
    print(f"Number of completions in the last 7 days: {completions_in_last_7_days}")

    # calculate the number of completions in the last 30 days
    completions_in_last_30_days = 0
    for completion in completions:
        completion_date = datetime.strptime(completion[0], '%Y-%m-%d').date()
        if (date.today() - completion_date).days <= 30:
            completions_in_last_30_days += 1
    print(f"Number of completions in the last 30 days: {completions_in_last_30_days}")
