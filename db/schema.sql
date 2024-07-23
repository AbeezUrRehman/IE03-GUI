CREATE TABLE IF NOT EXISTS url (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS word (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS link (
    source INTEGER,
    target INTEGER,
    FOREIGN KEY (source) REFERENCES url(id),
    FOREIGN KEY (target) REFERENCES url(id)
);

CREATE TABLE IF NOT EXISTS location (
    wordid INTEGER,
    urlid INTEGER,
    FOREIGN KEY (wordid) REFERENCES word(id),
    FOREIGN KEY (urlid) REFERENCES url(id)
);

CREATE TABLE IF NOT EXISTS pagerank (
    urlid INTEGER,
    rank REAL,
    FOREIGN KEY (urlid) REFERENCES url(id)
);

CREATE TABLE IF NOT EXISTS friends (
    user1 INT,
    user2 INT
);

CREATE TABLE IF NOT EXISTS groups (
    group_id INT PRIMARY KEY,
    group_name VARCHAR(100)
);
