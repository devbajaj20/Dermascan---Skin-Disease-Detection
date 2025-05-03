import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop the existing users table
cursor.execute('DROP TABLE IF EXISTS users')

# Recreate users table without the email field
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
