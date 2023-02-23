import calendar
from datetime import date, datetime, timedelta
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
    for streak in streaks:
        habit_id = streak[1]
        update_streak(habit_id)
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

    # Check if the habit has been completed within the period to reset the streak


def update_streak(habit_id):
    streaks = db.get_streaks()
    habit = db.get_habit(habit_id)
    for streak in streaks:
        habit_id = streak[1]
        period = habit[2]
        last_completion_date = db.get_last_completion_date(habit_id)
        if last_completion_date:
            last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d').date()
            days_since_last_completion = (date.today() - last_completion_date).days
            if period == 1 and days_since_last_completion > 1:
                db.reset_streak(habit_id)
            elif period == 7 and days_since_last_completion > 7:
                db.reset_streak(habit_id)
            elif period == 30 and days_since_last_completion > 30:
                db.reset_streak(habit_id)


def show_habit_completions(habit_id):
    """
    This function shows a calendar based on last week, last month or specific month in the last year and marks the days
    when the habit has been completed.
    :param habit_id: The id of the habit. (int)
    'last_month', or 'YYYY-MM' where YYYY is the year and MM is the month. (str)
    """
    period = questionary.select("Which period would you like to analyze?", choices=["last week", "last month"]).ask()
    # Determine the start and end dates based on the period
    if period == "last week":
        start_date = date.today() - timedelta(days=7)
        end_date = date.today()
    elif period == "last month":
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
    else:
        start_date = date.today() - timedelta(days=365)
        end_date = date.today()

    start_date = datetime.strftime(start_date, '%Y-%m-%d')
    end_date = datetime.strftime(end_date, '%Y-%m-%d')

    # Get the completion dates for the habit
    rows = db.get_completions_in_range(habit_id, start_date, end_date)


    # Create a dictionary to store the completion dates as keys and values as True
    completion_dates = {}
    for row in rows:
        completion_date = row[0]
        completion_dates[completion_date] = True

    # Get the current year and month
    year = start_date.year
    month = start_date.month

    # Create a calendar for the current month
    cal = calendar.monthcalendar(year, month)

    # Print the header
    print(calendar.month_name[month], year)

    # Print the days of the week
    print("Mo Tu We Th Fr Sa Su")

    # Loop over each week in the calendar
    for week in cal:
        # Loop over each day in the week
        for day in week:
            if day == 0:
                # If the day is 0, print a space
                print("  ", end="")
            else:
                # If the day is not 0, print the day number
                day_str = str(day).rjust(2)
                # Check if the day has a completion
                if f"{year}-{month:02}-{day_str}" in completion_dates:
                    # If it does, print an X
                    print(f"\033[1;32;40m{day_str}\033[0m", end="")
                else:
                    # If it doesn't, print the day number
                    print(day_str, end="")
                print(" ", end="")
        print("")











# def show_habit_completions(habit_id):
#     """
#     This function shows a calendar based on last week, last month or last year and marks the days when the habit has been
#     completed.
#     :param habit_id: The id of the habit. (int)
#     """
#     rows = db.get_habit_completions(habit_id)
#
#     # Create a dictionary to store the completion dates as keys and values as True
#     completion_dates = {}
#     for row in rows:
#         completion_date = row[0]
#         completion_dates[completion_date] = True
#
#     # Get the current year and month
#     now = datetime.now()
#     year = now.year
#     month = now.month
#
#     # Create a calendar for the current month
#     cal = calendar.monthcalendar(year, month)
#
#     # Print the header
#     print(calendar.month_name[month], year)
#
#     # Print the days of the week
#     print("Mo Tu We Th Fr Sa Su")
#
#     # Loop over each week in the calendar
#     for week in cal:
#         # Loop over each day in the week
#         for day in week:
#             if day == 0:
#                 # If the day is 0, print a space
#                 print("  ", end="")
#             else:
#                 # If the day is not 0, print the day number
#                 day_str = str(day).rjust(2)
#                 # Check if the day has a completion
#                 if f"{year}-{month:02}-{day_str}" in completion_dates:
#                     # If it does, print an X
#                     print(f"\033[1;32;40m{day_str}\033[0m", end="")
#                 else:
#                     # If it doesn't, print the day number
#                     print(day_str, end="")
#                 print(" ", end="")
#         print("")





    # completions = db.get_habit_completions(habit_id)
    # habit_completions = []
    #
    # for completion in completions:
    #     completion_date = datetime.strptime(completion[0], '%Y-%m-%d').date()
    #     habit_completions.append([completion_date, "Completed"])
    #
    # print(tb.tabulate(habit_completions, tablefmt="double_grid"))









    #
    #
    # period = questionary.select("Which period would you like to analyze?", choices=["last_week", "last_month", "last_year"]).ask()
    # start_date = None
    # end_date = None
    # # Calculate start and end dates based on period
    # if period == 'last_week':
    #     start_date = date.today() - timedelta(days=7)
    #     end_date = date.today()
    # elif period == 'last_month':
    #     start_date = date.today() - timedelta(days=30)
    #     end_date = date.today()
    # elif period == 'last_year':
    #     start_date = date.today() - timedelta(days=365)
    #     end_date = date.today()
    #
    # start_date = datetime.strftime(start_date, '%Y-%m-%d')
    # end_date = datetime.strftime(end_date, '%Y-%m-%d')
    # # Retrieve completion dates from database
    # completions = db.get_completions_in_range(habit_id, start_date, end_date)
    #
    # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    # # Create a calendar for the selected time period
    # cal = calendar.Calendar()
    # weeks = cal.monthdatescalendar(start_date.year, start_date.month)
    #
    # # Initialize an empty calendar string
    # calendar_str = ''
    #
    # # Loop over each week in the calendar
    # for week in weeks:
    #     # Loop over each day in the week
    #     for day in week:
    #         if day.month != start_date.month:
    #             # Day is not in the current month, print a blank space
    #             calendar_str += '    '
    #         elif day in completions:
    #             # Day is marked as complete, print an X
    #             calendar_str += '[X] '
    #         else:
    #             # Day is not marked as complete, print a dot
    #             calendar_str += '[.] '
    #         # Start a new line after each week
    #     calendar_str += '\n'
    #
    #     # Print the calendar
    # print(calendar_str)