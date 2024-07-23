import sqlite3

def create_schema(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS url (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS word (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS link (
            source INTEGER,
            target INTEGER,
            FOREIGN KEY (source) REFERENCES url(id),
            FOREIGN KEY (target) REFERENCES url(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS location (
            wordid INTEGER,
            urlid INTEGER,
            FOREIGN KEY (wordid) REFERENCES word(id),
            FOREIGN KEY (urlid) REFERENCES url(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pagerank (
            urlid INTEGER,
            rank REAL,
            FOREIGN KEY (urlid) REFERENCES url(id)
        )
    ''')

def insert_data(cursor, urls, words, links, locations, pageranks):
    for url in urls:
        cursor.execute("INSERT OR IGNORE INTO url (url) VALUES (?)", (url,))
    for word in words:
        cursor.execute("INSERT OR IGNORE INTO word (word) VALUES (?)", (word,))
    for source, target in links:
        cursor.execute("INSERT INTO link (source, target) VALUES ((SELECT id FROM url WHERE url = ?), (SELECT id FROM url WHERE url = ?))", (source, target))
    for word, url in locations:
        cursor.execute("INSERT INTO location (wordid, urlid) VALUES ((SELECT id FROM word WHERE word = ?), (SELECT id FROM url WHERE url = ?))", (word, url))
    for url, rank in pageranks.items():
        cursor.execute("INSERT INTO pagerank (urlid, rank) VALUES ((SELECT id FROM url WHERE url = ?), ?)", (url, rank))

def main():
    conn = sqlite3.connect('book_recommendations.db')
    cursor = conn.cursor()
    create_schema(cursor)
    
    urls = ['algorithm.html', 'sort.html', 'search.html', 'data.html', 'graph.html']
    words = ['program', 'algorithm', 'data', 'structure', 'sort', 'merge', 'array', 'binary', 'list', 'queue', 'stack', 'bfs', 'dfs', 'node', 'edge']
    links = [('algorithm.html', 'sort.html'), ('algorithm.html', 'search.html'), ('algorithm.html', 'data.html'), ('sort.html', 'data.html'), ('sort.html', 'search.html')]
    locations = [('program', 'algorithm.html'), ('algorithm', 'algorithm.html'), ('data', 'algorithm.html'), ('structure', 'algorithm.html'), ('sort', 'sort.html')]
    pageranks = {
        'algorithm.html': 0.15,
        'sort.html': 0.66,
        'search.html': 1.10,
        'data.html': 1.58,
        'graph.html': 1.49
    }
    
    insert_data(cursor, urls, words, links, locations, pageranks)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
