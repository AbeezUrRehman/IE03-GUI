import sqlite3

def connect_db():
    conn = sqlite3.connect('db/book_recommendations.db')
    return conn

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        book_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagerank (
        urlid INTEGER PRIMARY KEY,
        rank REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS url (
        rowid INTEGER PRIMARY KEY,
        url TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS word (
        rowid INTEGER PRIMARY KEY,
        word TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS location (
        wordid INTEGER,
        urlid INTEGER,
        FOREIGN KEY (wordid) REFERENCES word(rowid),
        FOREIGN KEY (urlid) REFERENCES url(rowid)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS link (
        source INTEGER,
        target INTEGER,
        FOREIGN KEY (source) REFERENCES url(rowid),
        FOREIGN KEY (target) REFERENCES url(rowid)
    )
    ''')

    conn.commit()
    conn.close()

def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    sample_books = [
        ("Book 1", "Author 1"),
        ("Book 2", "Author 2"),
        ("Book 3", "Author 3")
    ]
    
    sample_users = [
        ("User 1",),
        ("User 2",),
        ("User 3",)
    ]

    cursor.executemany('''
    INSERT INTO books (title, author) VALUES (?, ?)
    ''', sample_books)

    cursor.executemany('''
    INSERT INTO users (name) VALUES (?)
    ''', sample_users)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_sample_data()