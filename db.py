import sqlite3

def create_connection():
    conn = sqlite3.connect('habits.db')
    c = conn.cursor()
    return conn, c

def close_connection(conn):
    conn.close()

def init_db():
    conn, c = create_connection()
    c.execute("""CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_name TEXT NOT NULL,
        periodicity INTEGER NOT NULL,
        creation_date DATE NOT NULL,
        last_completion_date DATE, 
        number_of_completions INTEGER DEFAULT 0
        )""")
    c.execute("""CREATE TABLE IF NOT EXISTS completions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        completion_date DATE NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
        )""")
    c.execute("""CREATE TABLE IF NOT EXISTS streaks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        current_streak INTEGER NOT NULL,
        longest_streak INTEGER NOT NULL,
        streak_start_date DATE NOT NULL,
        streak_end_date DATE NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits(id)
        )""")
    conn.commit()
    close_connection(conn)

def add_habit(habit_name, periodicity):
    conn, c = create_connection()
    c.execute("INSERT INTO habits (habit_name, periodicity, creation_date) VALUES (?, ?, ?)", (habit_name, periodicity, date.today()))
    conn.commit()
    close_connection(conn)

def add_completion(habit_id):
    conn, c = create_connection()
    c.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, ?)", (habit_id, date.today()))
    c.execute("UPDATE habits SET number_of_completions = number_of_completions + 1 WHERE id=?", (habit_id,))
    c.execute("UPDATE habits SET last_completion_date = ? WHERE id=?", (date.today(), habit_id))
    conn.commit()
    close_connection(conn)

def delete_habit(habit_id):
    conn, c = create_connection()
    c.execute("DELETE FROM habits WHERE id=?", (habit_id,))
    c.execute("DELETE FROM completions WHERE habit_id=?", (habit_id,))
    c.execute("DELETE FROM streaks WHERE habit_id=?", (habit_id,))
    conn.commit()
    close_connection(conn)

def delete_completion(habit_id, completion_date):
    conn, c = create_connection()
    c.execute("DELETE FROM completions WHERE habit_id=? AND completion_date=?", (habit_id, completion_date))
    c.execute("UPDATE habits SET number_of_completions = number_of_completions - 1 WHERE id=?", (habit_id,))
    conn.commit()
    close_connection(conn)

def delete_all_completions(habit_id):
    conn, c = create_connection()
    c.execute("DELETE FROM completions WHERE habit_id=?", (habit_id,))
    c.execute("UPDATE habits SET number_of_completions = 0 WHERE id=?", (habit_id,))
    conn.commit()
    close_connection(conn)

def get_habits():
    conn, c = create_connection()
    c.execute("SELECT * FROM habits")
    habits = c.fetchall()
    close_connection(conn)
    return habits

def get_habit_name(habit_id):
    conn, c = create_connection()
    c.execute("SELECT habit_name FROM habits WHERE id=?", (habit_id,))
    habit_name = c.fetchone()
    close_connection(conn)
    return habit_name[0]

def get_habit_periodicity(habit_id):
    conn, c = create_connection()
    c.execute("SELECT periodicity FROM habits WHERE id=?", (habit_id,))
    periodicity = c.fetchone()
    close_connection(conn)
    return periodicity[0]

def get_habit_creation_date(habit_id):
    conn, c = create_connection()
    c.execute("SELECT creation_date FROM habits WHERE id=?", (habit_id,))
    creation_date = c.fetchone()
    close_connection(conn)
    return creation_date[0]

def get_habit_last_completion_date(habit_id):
    conn, c = create_connection()
    c.execute("SELECT last_completion_date FROM habits WHERE id=?", (habit_id,))
    last_completion_date = c.fetchone()
    close_connection(conn)
    return last_completion_date[0] 

def get_habit_number_of_completions(habit_id):
    conn, c = create_connection()
    c.execute("SELECT number_of_completions FROM habits WHERE id=?", (habit_id,))
    number_of_completions = c.fetchone()
    close_connection(conn)
    return number_of_completions[0]


def get_completions(habit_id):
    conn, c = create_connection()
    c.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date ASC", (habit_id,))
    completions = c.fetchall()
    close_connection(conn)
    return completions


def get_habits():
    conn, c = create_connection()
    c.execute("SELECT * FROM habits")
    habits = c.fetchall()
    close_connection(conn)
    return habits


def get_habit_periodicity(habit_id):
    conn, c = create_connection()
    c.execute("SELECT periodicity FROM habits WHERE id=?", (habit_id,))
    periodicity = c.fetchone()
    close_connection(conn)
    return periodicity[0]


def get_habit_name(habit_id):
    conn, c = create_connection()
    c.execute("SELECT habit_name FROM habits WHERE id=?", (habit_id,))
    habit_name = c.fetchone()
    close_connection(conn)
    return habit_name[0]


def get_habit_creation_date(habit_id):
    conn, c = create_connection()
    c.execute("SELECT creation_date FROM habits WHERE id=?", (habit_id,))
    creation_date = c.fetchone()
    close_connection(conn)
    return creation_date[0]


def get_habit_last_completion_date(habit_id):
    conn, c = create_connection()
    c.execute("SELECT last_completion_date FROM habits WHERE id=?", (habit_id,))
    last_completion_date = c.fetchone()
    close_connection(conn)
    return last_completion_date[0]


def get_habit_number_of_completions(habit_id):
    conn, c = create_connection()
    c.execute("SELECT number_of_completions FROM habits WHERE id=?", (habit_id,))
    number_of_completions = c.fetchone()
    close_connection(conn)
    return number_of_completions[0]


def add_habit(habit_name, periodicity):
    conn, c = create_connection()
    c.execute("INSERT INTO habits (habit_name, periodicity, creation_date) VALUES (?, ?, date('now'))", (habit_name, periodicity))
    conn.commit()
    close_connection(conn)


def add_completion(habit_id):
    conn, c = create_connection()
    c.execute("INSERT INTO completions (habit_id, completion_date) VALUES (?, date('now'))", (habit_id,))
    c.execute("UPDATE habits SET number_of_completions = number_of_completions + 1, last_completion_date = date('now') WHERE id=?", (habit_id,))
    conn.commit()
    close_connection(conn)


def delete_habit(habit_id):
    conn, c = create_connection()
    c.execute("DELETE FROM habits WHERE id=?", (habit_id,))
    conn.commit()
    close_connection(conn)


def delete_completion(habit_id, completion_date):
    conn, c = create_connection()
    c.execute("DELETE FROM completions WHERE habit_id=? AND completion_date=?", (habit_id, completion_date))
    c.execute("UPDATE habits SET number_of_completions = number_of_completions - 1 WHERE id=?", (habit_id,))
    conn.commit()
    close_connection(conn)


# def create_connection():
#     conn = sqlite3.connect('habits.db')
#     c = conn.cursor()
#     return conn, c

# def close_connection(conn):
#     conn.close()

# def init_db():
#     conn, c = create_connection()
#     c.execute("""CREATE TABLE IF NOT EXISTS habits (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         habit_name TEXT NOT NULL,
#         periodicity INTEGER NOT NULL,
#         creation_date DATE NOT NULL,
#         last_completion_date DATE, 
#         number_of_completions INTEGER DEFAULT 0
#         )""")
#     c.execute("""CREATE TABLE IF NOT EXISTS completions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         habit_id INTEGER NOT NULL,
#         completion_date DATE NOT NULL,
#         FOREIGN KEY (habit_id) REFERENCES habits(id)
#         )""")
#     conn.commit()
#     close_connection(conn)


# def get_completions(habit_id):
#     conn, c = create_connection()
#     c.execute("SELECT completion_date FROM completions WHERE habit_id=? ORDER BY completion_date ASC", (habit_id,))
#     completions = c.fetchall()
#     close_connection(conn)
#     return completions


# def get_habits():
#     conn, c = create_connection()
#     c.execute("SELECT * FROM habits")
#     habits = c.fetchall()
#     close_connection(conn)
#     return habits


# def get_habit_periodicity(habit_id):
#     conn, c = create_connection()
#     c.execute("SELECT periodicity FROM habits WHERE id=?", (habit_id,))
#     periodicity = c.fetchone()[0]
#     return periodicity
