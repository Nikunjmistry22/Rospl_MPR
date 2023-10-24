import sqlite3

# Connect to the database (creates a new one if it doesn't exist)
conn = sqlite3.connect('connectify_db.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Define your table and columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS qr_details (
        message text
    )
''')
# Commit the changes and close the connection
conn.commit()
conn.close()
