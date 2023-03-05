import sqlite3
from datetime import datetime


class Database:
    """
    This class is responsible for creating the database and the tables.
    It also contains methods for connecting and closing the database connection.
    It is used by the other classes to perform CRUD operations on the database.
    It is also used to get data from the database.
    It is used as follows: db = Database() and then db.method() to call a method.
    """

    def __init__(self, name='habits.db'):
        """
        This method initializes the database and the tables.
        :param name: The name of the database.
        """
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.c = self.conn.cursor()
        self.init_db()

    def create_connection(self):
        """
        Create a connection to the database
        """
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        return conn, c

    def close_connection(self, conn):
        """
        Close the connection to the database
        """
        conn.close(self.name)

    def init_db(self):
        """
        This method creates the database and the tables if they don't exist.
        """
        self.c.execute("""CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL,
            periodicity INTEGER NOT NULL,
            creation_date DATE NOT NULL,
            last_completion_date DATE,
            number_of_completions INTEGER DEFAULT 0
            )""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completion_date DATE NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
            )""")
        self.c.execute("""CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            current_streak INTEGER NOT NULL,
            longest_streak INTEGER NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
            )""")
        self.conn.commit()

    def get_habits(self):
        """
        This method returns all the habits in the database as a list of tuples.
        :return: A list of tuples containing all the habits.
        """
        self.c.execute("SELECT * FROM habits")
        habits = self.c.fetchall()
        return habits

    def get_habit(self, habit_id):
        """
        This method returns a habit from the database.
        :param habit_id: The ID of the habit.
        :return: A tuple containing only one habit information.
        """
        self.c.execute("SELECT * FROM habits WHERE id=?", (habit_id,))
        habit = self.c.fetchone()
        return habit

    def get_habit_completions(self, habit_id):
        """
        This method returns all the completions of a habit.
        :param habit_id: The ID of the habit.
        :return: A list of tuples containing all the completions of a habit.
        """
        self.c.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date ASC",
                       (habit_id,))
        completions = self.c.fetchall()
        return completions

    def get_habit_periodicity(self, habit_id):
        """
        This method returns the periodicity of a habit.
        :param habit_id: The ID of the habit.
        :return: The periodicity of the habit.
        """
        self.c.execute("SELECT periodicity FROM habits WHERE id=?", (habit_id,))
        periodicity = self.c.fetchone()[0]
        return periodicity

    def get_streaks(self):
        """
        This method returns all the streaks in the database as a list of tuples.
        :return: A list of tuples containing all the streaks.
        """
        self.c.execute("SELECT * FROM streaks")
        streaks = self.c.fetchall()
        return streaks

    def get_streaks_for_habit(self, habit_id):
        """
        This method returns the streaks of a habit.
        :param habit_id: The ID of the habit.
        :return: A tuple containing the streaks of a habit.
        """
        self.c.execute("SELECT * FROM streaks WHERE habit_id=?", (habit_id,))
        streaks = self.c.fetchone()
        return streaks

    def get_updated_streaks(self, habit_id):
        """
        This method returns the streaks of a habit after updating them.
        :param habit_id: The ID of the habit.
        :return: A tuple containing the streaks of a habit.
        """
        self.update_streak(habit_id)
        self.c.execute("SELECT * FROM streaks WHERE habit_id=?", (habit_id,))
        streaks = self.c.fetchone()
        return streaks

    def get_last_completion_date(self, habit_id):
        """
        This method returns the last completion date of a habit.
        :param habit_id: The ID of the habit.
        :return: The last completion date of the habit.
        """
        self.c.execute("SELECT last_completion_date FROM habits WHERE id=?", (habit_id,))
        last_completion_date = self.c.fetchone()[0]
        return last_completion_date

    def update_streak(self, habit_id):
        """
        This function updates the streak of a habit. If the habit has not been completed within the period, the current
        streak will reset.
        :param habit_id: The ID of the habit.
        :return: None
        """
        streaks = self.get_streaks()
        habit = self.get_habit(habit_id)
        for streak in streaks:
            habit_id = streak[1]
            period = habit[2]
            last_completion_date = self.get_last_completion_date(habit_id)
            if last_completion_date:
                last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d %H:%M:%S')
                days_since_last_completion = (datetime.now() - last_completion_date).days
                if period == 1 and days_since_last_completion > 1:
                    self.reset_streak(habit_id)
                elif period == 7 and days_since_last_completion > 7:
                    self.reset_streak(habit_id)
                elif period == 30 and days_since_last_completion > 30:
                    self.reset_streak(habit_id)

    def reset_streak(self, habit_id):
        """
        This function resets the current streak of a habit.
        """
        self.c.execute("UPDATE streaks SET current_streak=0 WHERE habit_id=?", (habit_id,))
        self.conn.commit()
