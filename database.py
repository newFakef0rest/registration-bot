import sqlite3

conn = sqlite3.connect('database.db', check_same_thread=False)
sql = conn.cursor()

sql.execute('CREATE TABLE IF NOT EXISTS users '
            '(id INTEGER PRIMARY KEY NOT NULL, '
            'username TEXT NOT NULL, '
            'number TEXT NOT NULL, '
            'location TEXT NOT NULL); ')

def register(id, name, number, location):
    sql.execute('INSERT INTO users VALUES (?, ?, ?, ?);', (id, name, number, location))
    conn.commit()

def check_user(id):
    if sql.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone():
        return True
    else:
        return False

def show_users():
    return sql.execute('SELECT * FROM users').fetchall();

print(show_users())