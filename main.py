import sys

import questionary
import termcolor

import analyze
import db
import habits as hb

print(termcolor.colored("\n**********************************" , "cyan"))
print(termcolor.colored("Welcome to Habit Tracker APP!" , "white"))
print(termcolor.colored("Use this app to track your habits." , "yellow"))
print(termcolor.colored("***********************************" , "cyan"))

def main():

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
        hb.habits_todo()
        ask_to_continue()
        


    elif action == 'analyze':
        choices = [
        {"name": "Habits overview", "value": "overview"},
        {"name": "Single habit status", "value": "status"},
        {"name": "Streaks analysis", "value": "streak"},
    ]
        action = questionary.select("\nWhat would you like to do?", choices=choices).ask()
        if action == 'overview':
            analyze.habit_overview()
            ask_to_continue()

        elif action == 'status':
            analyze.habit_status()
            ask_to_continue()

        elif action == 'streak':
            analyze.habit_streaks()
            ask_to_continue()


    elif action == 'quit':
        print(termcolor.colored("Looking forward to see you again\n\n", "blue"))
        sys.exit(0)

    else:
        print(termcolor.colored("Invalid option. Please try again!", "red"))

def ask_to_continue():
    continue_ = questionary.confirm("Would you like to continue?").ask()
    if continue_:
        main()
    else:
        print(termcolor.colored("Looking forward to see you again\n\n", "blue"))
        sys.exit(0)

if __name__ == "__main__":
    main()



# def main():
#     db.init_db()

#     choices = [
#         {"name": "Add a habit", "value": "add"},
#         {"name": "Mark a habit as complete", "value": "complete"},
#         {"name": "Delete a habit", "value": "delete"},
#         {"name": "Today habits", "value": "todo"},
#         {"name": "Analyze habits", "value": "analyze"},
#         {"name": "Quit application", "value": "quit"}
#     ]

#     action = questionary.select("\nWhat would you like to do?", choices=choices).ask()

#     if action == 'add':
#         hb.add_habit()
#         ask_to_continue()


#     elif action == 'complete':
#         hb.mark_habit_as_complete()
#         ask_to_continue()


#     elif action == 'delete':
#         hb.delete_habit()
#         ask_to_continue()


#     elif action == 'todo':
#         hb.habits_todo()
#         ask_to_continue()
        


#     elif action == 'analyze':
#         choices = [
#         {"name": "Habits overview", "value": "overview"},
#         {"name": "Single habit status", "value": "status"},
#         {"name": "Streaks analysis", "value": "streak"},
#     ]
#         action = questionary.select("\nWhat would you like to do?", choices=choices).ask()
#         if action == 'overview':
#             analyze.habit_overview()
#             ask_to_continue()

#         elif action == 'status':
#             analyze.habit_status()
#             ask_to_continue()

#         elif action == 'streak':
#             analyze.habit_streaks()
#             ask_to_continue()


#     elif action == 'quit':
#         print(termcolor.colored("Looking forward to see you again\n\n", "blue"))
#         sys.exit(0)

#     else:
#         print(termcolor.colored("Invalid option. Please try again!", "red"))



# def ask_to_continue():
#     go_back = questionary.confirm("Do you want to go back to the main menu?").ask()
#     if go_back:
#         main()
#     else:
#         print(termcolor.colored("Looking forward to see you again\n", "blue"))
#         sys.exit(0)


# if __name__ == "__main__":
#     main()
