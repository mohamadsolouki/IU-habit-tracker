import sys
import questionary
import termcolor
import analyze
import db
import habits as hb

hb = hb.Habit()
db = db.Database()

print(termcolor.colored("\n**********************************", "cyan"))
print(termcolor.colored("Welcome to Habit Tracker APP!", "white"))
print(termcolor.colored("Use this app to track your habits.", "yellow"))
print(termcolor.colored("***********************************", "cyan"))


def main():
    """
    This function is the main function of the application, and it is responsible for the main menu and
    the navigation between the different functionalities of the application.
    It also calls the functions that initialize the database and the table.
    It also calls the function that asks the user if he/she wants to continue using the application or not.
    """
    db.init_db()
    
    choices = [
        {"name": "Add a habit", "value": "add"},
        {"name": "Mark a habit as complete", "value": "complete"},
        {"name": "Delete a habit", "value": "delete"},
        {"name": "Today habits", "value": "todo"},
        {"name": "Analyze habits", "value": "analyze"},
        {"name": "Quit application", "value": "quit"}
    ]

    action = questionary.select("\nWhat would you like to do?", choices=choices).ask()

    if action == 'add':
        hb.add_habit()
        ask_to_continue()

    elif action == 'complete':
        hb.mark_habit_as_complete()
        ask_to_continue()

    elif action == 'delete':
        hb.delete_habit()
        ask_to_continue()

    elif action == 'todo':
        analyze.habits_todo()
        ask_to_continue()

    elif action == 'analyze':
        choices = [
            {"name": "Habits overview", "value": "overview"},
            {"name": "Single habit status", "value": "status"},
            {"name": "Streaks analysis", "value": "streak"},
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
