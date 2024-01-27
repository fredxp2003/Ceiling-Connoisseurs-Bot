import sqlite3

def setup_database(DB_NAME):
    """Creates the database if it doesn't exist and creates the table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS posted_messages (message_id INTEGER)''')
        conn.commit()

def is_posted(DB_NAME, message_id):
    """Checks if a message id has already been posted."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM posted_messages WHERE message_id=?", (message_id,))
        return c.fetchone() is not None

def insert_message_id(DB_NAME, message_id):
    """Inserts message id into the database."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO posted_messages (message_id) VALUES (?)", (message_id,))
        conn.commit()