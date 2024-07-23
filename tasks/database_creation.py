import sqlite3

def create_tables():
    conn = sqlite3.connect('book_recommendations.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            description TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friendships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            friend_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            content TEXT,
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            score REAL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pageranks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER,
            rank REAL,
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word_id INTEGER,
            document_id INTEGER,
            FOREIGN KEY (word_id) REFERENCES words(id),
            FOREIGN KEY (document_id) REFERENCES documents(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_document_id INTEGER,
            target_document_id INTEGER,
            FOREIGN KEY (source_document_id) REFERENCES documents(id),
            FOREIGN KEY (target_document_id) REFERENCES documents(id)
        )
    ''')

    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('book_recommendations.db')
    cursor = conn.cursor()

    # Sample data
    users = [('Alice',), ('Bob',)]
    books = [('Python Programming', 'John Doe', 'A book about Python programming.')]
    friendships = [(1, 2)]
    documents = [(1, 'This is a sample document about Python Programming.')]
    recommendations = [(1, 1, 4.5)]
    pageranks = [(1, 0.8)]
    words = [('python',), ('programming',)]
    locations = [(1, 1), (2, 1)]
    links = [(1, 1)]

    cursor.executemany("INSERT INTO users (name) VALUES (?)", users)
    cursor.executemany("INSERT INTO books (title, author, description) VALUES (?, ?, ?)", books)
    cursor.executemany("INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)", friendships)
    cursor.executemany("INSERT INTO documents (book_id, content) VALUES (?, ?)", documents)
    cursor.executemany("INSERT INTO recommendations (user_id, book_id, score) VALUES (?, ?, ?)", recommendations)
    cursor.executemany("INSERT INTO pageranks (document_id, rank) VALUES (?, ?)", pageranks)
    cursor.executemany("INSERT INTO words (word) VALUES (?)", words)
    cursor.executemany("INSERT INTO locations (word_id, document_id) VALUES (?, ?)", locations)
    cursor.executemany("INSERT INTO links (source_document_id, target_document_id) VALUES (?, ?)", links)

    conn.commit()
    conn.close()

def query_data():
    conn = sqlite3.connect('book_recommendations.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("Users:", users)

    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("Books:", books)

    cursor.execute("SELECT * FROM recommendations")
    recommendations = cursor.fetchall()
    print("Recommendations:", recommendations)

    conn.close()

if __name__ == "__main__":
    create_tables()
    insert_data()
    query_data()
