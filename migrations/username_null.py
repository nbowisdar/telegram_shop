import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Rename the existing table
cursor.execute("ALTER TABLE User RENAME TO User_old;")

# Create a new table with the desired changes
cursor.execute("""
    CREATE TABLE User (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        register_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        banned INTEGER DEFAULT 0
    );
""")

# Copy data from the old table to the new table
cursor.execute("INSERT INTO User (user_id, username, register_time, banned) SELECT user_id, username, register_time, banned FROM User_old;")

# Drop the old table
cursor.execute("DROP TABLE User_old;")

# Commit the changes and close the connection
conn.commit()
conn.close()

