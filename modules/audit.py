from datetime import datetime

def log_action(cursor, conn, user, action, filename):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO audit_log (username, action, filename, timestamp)
    VALUES (?, ?, ?, ?)
    """, (user, action, filename, timestamp))

    conn.commit()
