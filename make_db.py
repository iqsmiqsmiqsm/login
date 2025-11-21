import sqlite3
import os
from werkzeug.security import generate_password_hash
from config import ADMIN_USER, ADMIN_PASS, DB_NAME

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
c.execute("DELETE FROM users")
c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (ADMIN_USER, generate_password_hash(ADMIN_PASS)))
conn.commit()
conn.close()
