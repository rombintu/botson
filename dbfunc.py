import sqlite3
import os

DATABASE = os.getcwd() + '/db.sqlite'

def add_target(content):
    db = sqlite3.connect(DATABASE)
    sql = db.cursor()
    script = f"INSERT INTO targets (title, cost) VALUES (?, ?)"
    sql.execute(script, (content))
    db.commit()
    db.close()

def select_target():
    db = sqlite3.connect(DATABASE)
    sql = db.cursor()
    script = f"SELECT * FROM targets"
    sql.execute(script)
    targets = sql.fetchall()
    db.close()
    return targets