import sqlite3
from datetime import date, datetime


class Database:
    """
    This class is responsible for creating the database and the tables.
    It also contains methods for connecting and closing the database connection.
    It is used by the other classes to perform CRUD operations on the database.
    It is also used to get data from the database.
    It is used as follows: db = Database() and then db.method() to call a method.
    """

    def __init__(self, name='habits.db'):
        self.name = name
        self.conn = sqlite3.connect(self.name)
        self.c = self.conn.cursor()
        self.init_db()

    def create_connection(self):
        conn = sqlite3.connect(self.name)
        c = conn.cursor()
        return conn, c

    def close_connection(self, conn):
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
        :return: list of tuples containing all the habits in the database
        """
        self.c.execute("SELECT * FROM habits")
        habits = self.c.fetchall()
        return habits

    def get_habit(self, habit_id):
        self.c.execute("SELECT * FROM habits WHERE id=?", (habit_id,))
        habit = self.c.fetchone()
        return habit

    def get_habit_completions(self, habit_id):
        self.c.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date ASC",
                       (habit_id,))
        completions = self.c.fetchall()
        return completions

    def get_habit_periodicity(self, habit_id):
        self.c.execute("SELECT periodicity FROM habits WHERE id=?", (habit_id,))
        periodicity = self.c.fetchone()[0]
        return periodicity

    def get_streaks(self):
        self.c.execute("SELECT * FROM streaks")
        streaks = self.c.fetchall()
        return streaks

    def get_streaks_for_habit(self, habit_id):
        self.update_streak(habit_id)
        self.c.execute("SELECT * FROM streaks WHERE habit_id=?", (habit_id,))
        streaks = self.c.fetchone()
        return streaks

    def get_last_completion_date(self, habit_id):
        self.c.execute("SELECT last_completion_date FROM habits WHERE id=?", (habit_id,))
        last_completion_date = self.c.fetchone()[0]
        return last_completion_date

    def reset_streak(self, habit_id):
        self.c.execute("UPDATE streaks SET current_streak=0 WHERE habit_id=?", (habit_id,))
        self.conn.commit()

    def get_completions_in_range(self, habit_id, start_date, end_date):
        """
            Returns a list of completion dates for this habit within the specified range.

            Args:
                habit_id
                start_date (str): Start date in the format YYYY-MM-DD.
                end_date (str): End date in the format YYYY-MM-DD.

            Returns:
                list: A list of completion dates as strings in the format YYYY-MM-DD.
            """
        self.c.execute("""
                    SELECT completion_date
                    FROM completions
                    WHERE habit_id=? AND completion_date BETWEEN ? AND ?
                    ORDER BY completion_date ASC
                """, (habit_id, start_date, end_date))
        rows = self.c.fetchall()
        completions = [row[0] for row in rows]
        return completions

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
                last_completion_date = datetime.strptime(last_completion_date, '%Y-%m-%d').date()
                days_since_last_completion = (date.today() - last_completion_date).days
                if period == 1 and days_since_last_completion > 1:
                    self.reset_streak(habit_id)
                elif period == 7 and days_since_last_completion > 7:
                    self.reset_streak(habit_id)
                elif period == 30 and days_since_last_completion > 30:
                    self.reset_streak(habit_id)
