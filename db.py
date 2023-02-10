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
    conn.commit()
    close_connection(conn)


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
    periodicity = c.fetchone()[0]
    return periodicity
