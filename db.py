import sqlite3

def create_db():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY, title TEXT)")
    db.commit()
    db.close()

def insert_post(title):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("INSERT INTO posts (title) VALUES (?)", (title,))
    db.commit()
    db.close()

def get_posts():
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    db.close()
    return posts

def findTitle(title):
    db = sqlite3.connect('database.db')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM posts WHERE title = ?", (title,))
    post = cursor.fetchone()
    db.close()
    return post