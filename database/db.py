import sqlite3

DB_FILE = "users.db"




def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        phone TEXT,
        lesson TEXT,
        week TEXT,
        hours TEXT,
        remaining_lessons TEXT,
        payments TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS homework (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        homework TEXT,
        send_time TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        schedule TEXT,
        time_schedule TEXT,
        extra_schedule TEXT
    )
    """)

    conn.commit()
    conn.close()



def register_user(user_id: int, username: str, password: str, phone: str, lesson: str, week: str, hours: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, username, password, phone, lesson, week, hours) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, username, password, phone, lesson, week, hours)
    )
    conn.commit()
    conn.close()


def is_user_registered(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def username_check(username: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def password_check(username: str, password: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id FROM users WHERE username = ? AND password = ?",
        (username, password)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None


def login_user(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET logged_in = 1 WHERE user_id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()


def is_logged_in(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT logged_in FROM users WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result and result[0] == 1



def add_homework(user_id: int, homework_url: str, send_time: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO homework (user_id, homework, send_time) VALUES (?, ?, ?)",
        (user_id, homework_url, send_time)
    )
    conn.commit()
    conn.close()


def get_homeworks_all_users():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username, h.homework, h.send_time
        FROM homework h
        JOIN users u ON h.user_id = u.user_id
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_homework_user(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT homework FROM homework WHERE user_id = ?",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def add_student(username, phone, lesson, hours, week, payments=""):
    remaining_lessons = lesson 
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, phone, lesson, hours, week, remaining_lessons, payments)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, phone, lesson, hours, week, remaining_lessons, payments))
    conn.commit()
    conn.close()


def get_count_students():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(user_id) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_all_students():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_all_students_ordered():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users ORDER BY username")
    rows = cursor.fetchall()
    conn.close()
    return rows



def save_schedule(user_id: int, username: str, schedule_days: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE schedule SET username = ?, schedule = ? WHERE user_id = ?",
        (username, schedule_days, user_id)
    )

    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO schedule (user_id, username, schedule) VALUES (?, ?, ?)",
            (user_id, username, schedule_days)
        )

    conn.commit()
    conn.close()


def get_user_schedule(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT schedule FROM schedule WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def get_user_data(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, phone FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def is_user_has_schedule(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM schedule WHERE user_id = ?",
        (user_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None




def add_extra_schedule(user_id: int, extra_schedule: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE schedule SET extra_schedule = ? WHERE user_id = ?",
        (extra_schedule, user_id)
    )

    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO schedule (user_id, extra_schedule) VALUES (?, ?)",
            (user_id, extra_schedule)
        )

    conn.commit()
    conn.close()


def get_user_extra_schedule(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT extra_schedule FROM schedule WHERE user_id = ?",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def check_user_id(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM schedule WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def get_all_users_schedule():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT u.username, s.schedule, s.extra_schedule
        FROM users u
        LEFT JOIN schedule s ON u.user_id = s.user_id
        ORDER BY u.username
    """)
    rows = cursor.fetchall() 
    conn.close()
    return rows

def add_schedule_individual(user_id: int, schedule: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schedule SET schedule = ? WHERE user_id = ?",
        (schedule, user_id)
    )
    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO schedule (user_id, schedule) VALUES (?, ?)",
            (user_id, schedule)
        )
    conn.commit()
    conn.close()


def add_time_schedule(user_id: int, time_schedule: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE schedule SET time_schedule = ? WHERE user_id = ?",
        (time_schedule, user_id)
    )
    if cursor.rowcount == 0:
        cursor.execute(
            "INSERT INTO schedule (user_id, time_schedule) VALUES (?, ?)",
            (user_id, time_schedule)
        )
    conn.commit()
    conn.close()
    
def get_user_profile(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT username, phone, lesson, hours, week, remaining_lessons, payments
    FROM users
    WHERE user_id = ?
    """, (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user 


def get_student_schedule(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT schedule, extra_schedule
    FROM schedule
    WHERE user_id = ?
    """, (user_id,))
    schedule = cursor.fetchone()
    conn.close()
    return schedule



def decrement_remaining_lessons(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT remaining_lessons FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        return None

    remaining = result[0]  

  
    if remaining is None:
        cursor.execute("SELECT lesson FROM users WHERE user_id = ?", (user_id,))
        lesson = cursor.fetchone()[0]
        remaining = int(lesson)
    else:
        remaining = int(remaining)

    if remaining > 0:
        remaining -= 1
        cursor.execute("UPDATE users SET remaining_lessons = ? WHERE user_id = ?", (remaining, user_id))
        conn.commit()

    conn.close()
    return remaining


def confirm_payment(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT payments FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None 

    old_status = row[0]

    new_status = "оплачено"

    cursor.execute(
        "UPDATE users SET payments = ? WHERE user_id = ?",
        (new_status, user_id)
    )
    conn.commit()
    conn.close()

    return new_status




def check_payment_status(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT remaining_lessons, payments FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return None

    remaining_lessons, payments = row

    if int(remaining_lessons) == 0:
        new_status = "не оплачено"
        cursor.execute("UPDATE users SET payments = ? WHERE user_id = ?", (new_status, user_id))
        conn.commit()
        conn.close()
        return new_status

    conn.close()
    return payments
    

def select_lessons(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT lesson FROM users WHERE user_id = ?", (user_id,))
    lesson = cursor.fetchone()[0]
    conn.close()
    return lesson



def get_user_name(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE user_id = ?", (user_id,))
    username = cursor.fetchone()[0]
    conn.close()
    return username