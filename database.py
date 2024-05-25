import sqlite3

###  MESSAGE DATABASE FUNCTIONS  ###
def setup_message_database(DB_NAME):
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

###  LEADERBOARD DATABASE FUNCTIONS  ###

def setup_leaderboard_database(DB_NAME):
    """
    Sets up the leaderboard database.

    This function connects to the specified SQLite database and creates the `leaderboard` table if it does not already exist.
    The `users` table contains two columns:
        - `user_id`: An integer representing the unique ID of the user.
        - `premium_ceiling_count`: An integer representing the user's premium ceiling.

    Parameters:
    DB_NAME (str): The name of the SQLite database file. If the file does not exist, it will be created.

    Returns:
    None
    """
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS leaderboard (user_id INTEGER, premium_ceiling_count INTEGER)''')
        conn.commit()

def increase_premium_ceiling_count(DB_NAME, user_id):
    """
    Increases the premium ceiling count for a user.
    
    Parameters:
    DB_NAME (str): The name of the SQLite database file.
    user_id (int): The Discord ID of the user.

    Returns:
    None
    """
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM leaderboard WHERE user_id=?", (user_id,))
        user = c.fetchone()
        if user:
            c.execute("UPDATE leaderboard SET premium_ceiling_count = premium_ceiling_count + 1 WHERE user_id=?", (user_id,))
        else:
            c.execute("INSERT INTO leaderboard (user_id, premium_ceiling_count) VALUES (?, 1)", (user_id,))
        conn.commit()

def set_premium_ceiling_count(DB_NAME, user_id, count):
    """Sets the premium ceiling count for a user."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM leaderboard WHERE user_id=?", (user_id,))
        user = c.fetchone()
        if user:
            c.execute("UPDATE leaderboard SET premium_ceiling_count = ? WHERE user_id=?", (count, user_id))
        else:
            c.execute("INSERT INTO leaderboard (user_id, premium_ceiling_count) VALUES (?, ?)", (user_id, count))
        conn.commit()

def get_premium_ceiling_count(user_id, DB_NAME = "leaderboard.db"):
    """Gets the premium ceiling count for a user."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM leaderboard WHERE user_id=?", (user_id,))
        user = c.fetchone()
        if user:
            return user[1]
        else:
            return 0
        
def get_top_users(DB_NAME = "leaderboard.db", limit = 5):
    """Returns the top users with the most premium ceilings."""
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM leaderboard ORDER BY premium_ceiling_count DESC LIMIT ?", (limit,))
        return c.fetchall()