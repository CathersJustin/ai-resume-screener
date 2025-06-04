import sqlite3
import json

def init_db():
    conn = sqlite3.connect("resumes.db")
    conn.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            name TEXT,
            entities TEXT,
            score REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_candidate(name, entities, score):
    conn = sqlite3.connect("resumes.db")
    conn.execute("INSERT INTO candidates (name, entities, score) VALUES (?, ?, ?)",
                 (name, json.dumps(entities), score))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect("resumes.db")
    rows = conn.execute("SELECT name, entities, score FROM candidates").fetchall()
    conn.close()
    return [(name, json.loads(entities), score) for name, entities, score in rows]