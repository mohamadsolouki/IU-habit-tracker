from modules import db, analyze, habits as hb
import sys
from datetime import datetime
import questionary
import termcolor

print(termcolor.colored("\n**********************************", "cyan"))
print(termcolor.colored("Welcome to Habit Tracker APP!", "white"))
print(termcolor.colored("Use this app to track your habits.", "yellow"))
print(termcolor.colored("***********************************", "cyan"))

ask = questionary.confirm("Do you want to use test database with predefined habits?").ask()
if ask is True:
    db.clear_databases()
    db.insert_test_data()
    db = db.Database(test=False)
else:
    db = db.Database(test=False)
    db.init_db()

hb = hb.Habit()


def main():
    """
    This function is the main function of the application, and it is responsible for the main menu and
    the navigation between the different functionalities of the application.
    It also calls the functions that initialize the database and the table.
    It also calls the function that asks the user if he/she wants to continue using the application or not.
    """
    action = questionary.select("\nWhat would you like to do?", choices=[
        {"name": "Add a habit", "value": "add"},
        {"name": "Mark a habit as complete", "value": "complete"},
        {"name": "Delete a habit", "value": "delete"},
        {"name": "Today habits", "value": "todo"},
        {"name": "Analyze habits", "value": "analyze"},
        {"name": "Quit application", "value": "quit"}
    ]).ask()

    if action == 'add':
        name = questionary.text("What is the habit name?").ask()
        periodicity = questionary.select("What is the habit periodicity?", choices=[
            {"name": "Daily", "value": 1},
            {"name": "Weekly", "value": 7},
            {"name": "Monthly", "value": 30}
        ]).ask()
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hb.add_habit(name, periodicity, creation_date)
        ask_to_continue()

    elif action == 'complete':
        habits = db.get_habits()
        habit_list = []
        if len(habits) == 0:
            print(termcolor.colored("There are no habits to mark as complete!", "red"))
            return
        for habit in habits:
            habit_list.append(f"{habit[0]}: {habit[1]}")
        habit_to_mark = questionary.select("Which habit would you like to mark?", choices=habit_list).ask()
        habit_id = habit_to_mark.split(":")[0].strip()
        completion_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        hb.mark_habit_as_complete(habit_id, completion_date)
        ask_to_continue()

    elif action == 'delete':
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
        habit_id = habit_to_delete.split(":")[0].strip()
        hb.delete_habit(habit_id)
        ask_to_continue()

    elif action == 'todo':
        analyze.habits_todo()
        ask_to_continue()

    elif action == 'analyze':
        choices = [
            {"name": "Habits overview", "value": "overview"},
            {"name": "Single habit status", "value": "status"},
            {"name": "Streaks analysis", "value": "streak"},
            {"name": "All completions of a habit", "value": "all"},
            {"name": "Go back to main menu", "value": "back"}]

        action = questionary.select("\nWhat would you like to do?", choices=choices).ask()
        if action == 'overview':
            analyze.habits_overview()
            ask_to_continue()

        elif action == 'status':
            analyze.habit_status()
            ask_to_continue()

        elif action == 'streak':
            analyze.show_habit_streaks()
            ask_to_continue()

        elif action == 'all':
            habits = db.get_habits()
            habit_list = []
            if len(habits) == 0:
                print(termcolor.colored("There are no habits to show!", "red"))
                return
            for habit in habits:
                habit_list.append(f"{habit[0]}: {habit[1]}")
            habit_list.append({"name": "Go back to main menu", "value": "back"})
            selected_habit = questionary.select("Which habit would you like to select?", choices=habit_list).ask()
            if selected_habit == "back":
                return
            habit_id = selected_habit.split(":")[0].strip()
            analyze.show_habit_completions(habit_id)
            ask_to_continue()

        elif action == 'back':
            main()

    elif action == 'quit':
        print(termcolor.colored("Looking forward to see you again\n\n", "blue"))
        sys.exit(0)

    else:
        print(termcolor.colored("Invalid option. Please try again!", "red"))


def ask_to_continue():
    """
    This function asks the user if he/she wants to continue using the application or not
    and calls the main function again if the user wants to continue
    or exits the application if the user does not want to continue.
    """
    continue_ = questionary.confirm("Would you like to continue?").ask()
    if continue_:
        main()
    else:
        print(termcolor.colored("Looking forward to see you again\n\n", "blue"))
        sys.exit(0)


if __name__ == "__main__":
    main()
