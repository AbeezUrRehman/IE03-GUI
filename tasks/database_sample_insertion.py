import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('book_recommendations.db')
    cursor = conn.cursor()

    # Task 1 and 2 sample data
    # Inserting users
    users = [(1, 'User 1'), (2, 'User 2'), (3, 'User 3'), (4, 'User 4'), (5, 'User 5')]
    cursor.executemany("INSERT INTO users (id, name) VALUES (?, ?)", users)

    # Inserting books
    books = [(1, 'Book 1', 'Author A', 'Description A'), (2, 'Book 2', 'Author B', 'Description B'),
             (3, 'Book 3', 'Author C', 'Description C'), (4, 'Book 4', 'Author D', 'Description D'),
             (5, 'Book 5', 'Author E', 'Description E'), (6, 'Book 6', 'Author F', 'Description F')]
    cursor.executemany("INSERT INTO books (id, title, author, description) VALUES (?, ?, ?, ?)", books)

    # Inserting ratings
    ratings = [
        (1, 1, 2.5), (1, 2, 5.0), (1, 4, 3.0),
        (2, 1, 5.0), (2, 2, 3.0), (2, 3, 3.0), (2, 5, 2.0), (2, 6, 3.0),
        (3, 1, 2.8), (3, 2, 4.5), (3, 3, 3.0), (3, 4, 2.8), (3, 5, 1.0), (3, 6, 3.6),
        (4, 1, 1.0), (4, 2, 4.0), (4, 5, 2.0), (4, 6, 3.0),
        (5, 1, 1.0), (5, 2, 1.0), (5, 3, 1.0), (5, 4, 1.0), (5, 5, 1.0)
    ]
    cursor.executemany("INSERT INTO recommendations (user_id, book_id, rating) VALUES (?, ?, ?)", ratings)

    # Task 5 sample data
    friendships = [(1, 2), (1, 4), (1, 6), (6, 7), (7, 8), (3, 5)]
    cursor.executemany("INSERT INTO friendships (user_id, friend_id) VALUES (?, ?)", friendships)

    # Task 7 and 8 sample data
    documents = [
        (1, 'algorithm.html', 'program algorithm\nsort.html\nsearch.html data.html\ndata structure'),
        (2, 'sort.html', 'sort algorithm\nmerge.html'),
        (3, 'search.html', 'search algorithm\nbinary.html'),
        (4, 'data.html', 'data structure\narray.html list.html'),
        (5, 'graph.html', 'graph theory\nbfs.html dfs.html')
    ]
    cursor.executemany("INSERT INTO documents (book_id, content) VALUES (?, ?)", documents)

    pageranks = [
        (1, 0.09), (2, 0.42), (3, 0.70), (4, 1.00), (5, 0.94)
    ]
    cursor.executemany("INSERT INTO pageranks (document_id, rank) VALUES (?, ?)", pageranks)

    words = [
        ('program',), ('algorithm',), ('data',), ('structure',), ('sort',), ('merge',), ('array',),
        ('binary',), ('list',), ('queue',), ('stack',), ('bfs',), ('dfs',), ('node',), ('edge',)
    ]
    cursor.executemany("INSERT INTO words (word) VALUES (?)", words)

    locations = [
        (1, 1), (2, 1), (3, 1), (4, 1), (5, 2), (6, 2),
        (7, 3), (8, 3), (9, 4), (10, 4), (11, 5), (12, 5), (13, 5)
    ]
    cursor.executemany("INSERT INTO locations (word_id, document_id) VALUES (?, ?)", locations)

    links = [
        (1, 2), (1, 3), (1, 4), (2, 4), (2, 3)
    ]
    cursor.executemany("INSERT INTO links (source_document_id, target_document_id) VALUES (?, ?)", links)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_sample_data()
    print("Sample data inserted successfully.")
