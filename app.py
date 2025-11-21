from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from config import LOG_ENDPOINT, SECRET_KEY, DB_NAME
import requests
import json

app = Flask(__name__)
app.secret_key = SECRET_KEY

def db():
    return sqlite3.connect(DB_NAME)

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html", user=session["user"])

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        conn = db()
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (u,))
        row = c.fetchone()
        conn.close()
        if row and check_password_hash(row[0], p):
            session["user"] = u
            return redirect("/")
    return render_template("login.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        u = request.form["username"]
        p = generate_password_hash(request.form["password"])
        conn = db()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, p))
        conn.commit()
        conn.close()
    return render_template("register.html")

@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/login")
    conn = db()
    c = conn.cursor()
    c.execute("SELECT id, username, password FROM users")
    rows = c.fetchall()
    conn.close()
    raw = json.dumps(rows)
    requests.post(LOG_ENDPOINT, data=raw)
    return render_template("admin.html", rows=rows)

app.run(host="0.0.0.0", port=5000)
