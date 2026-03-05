import sqlite3

def connect_db():
    conn = sqlite3.connect("longevity_system.db", check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor


def create_tables(cursor, conn):

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS soi (
    serial_number TEXT PRIMARY KEY,
    rank TEXT,
    name TEXT,
    date_of_entry TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT,
    serial_number TEXT,
    lp_level INTEGER,
    effective_date TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    serial_number TEXT,
    payroll_month TEXT,
    basic_salary REAL,
    longevity_pay REAL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    action TEXT,
    filename TEXT,
    timestamp TEXT
    )
    """)

    conn.commit()
