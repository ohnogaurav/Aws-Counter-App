from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this in production

DB_NAME = "counter.db"

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    counter INTEGER DEFAULT 0
                )''')
    conn.commit()
    conn.close()

init_db()

# ---------------- Routes ----------------
@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT counter FROM users WHERE username=?", (username,))
    counter = c.fetchone()[0]
    conn.close()

    return render_template("index.html", username=username, counter=counter)

@app.route('/increment')
def increment():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET counter = counter + 1 WHERE username=?", (session['username'],))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/reset')
def reset():
    if 'username' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE users SET counter = 0 WHERE username=?", (session['username'],))
    conn.commit()
    conn.close()

    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username already exists")

    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# ---------------- Run ----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
