import sqlite3

# Create a new database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Execute the SQL command to add the new column
cursor.execute('ALTER TABLE goods ADD COLUMN is_in_box BOOLEAN DEFAULT FALSE;')

# Commit the changes
conn.commit()

# Close the database connection
conn.close()