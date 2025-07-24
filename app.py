from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=1)
admin_password_hash = os.environ.get('ADMIN_PASSWORD_HASH')

def get_db():
    conn = sqlite3.connect('lessons.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS lessons(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                parent_id INTEGER,
                FOREIGN KEY (parent_id) REFERENCES lessons(id) ON DELETE CASCADE)''')
    

    
    root_exists = cur.execute('SELECT id FROM lessons WHERE id = 1').fetchone()
    if not root_exists:
        cur.execute("INSERT INTO lessons (id, title, content, parent_id) VALUES (?, ?, ?, ?)", (1, 'ROOT', '', None))

    
    conn.commit()#redundant dar bine sa nu uit
    conn.close()

@app.route('/')
def pagina_principala():
    conn = get_db()
    cur = conn.cursor()
    all_content = conn.execute("SELECT * FROM lessons").fetchall()
    conn.close()
    return render_template('index.html', lessons=all_content)

@app.route('/login', methods=['POST', 'GET'])
def pagina_login():
    if request.method == 'POST':
        input_parola = request.form.get("password")#ceva aici
        if admin_password_hash and check_password_hash(admin_password_hash, input_parola):
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('pagina_admin'))
        else:
            return redirect(url_for('pagina_login'))
        
    return render_template('login.html')#GET

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('pagina_principala'))


@app.route('/admin', methods=['POST', 'GET'])
def pagina_admin():
    if not session.get('logged_in'):
        return redirect(url_for('pagina_login'))

    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')
        if action == "delete":
            id = request.form.get("delete_id")
            flag = cur.execute('SELECT * FROM lessons WHERE id = ?', (id,)).fetchone()

            if flag:
                cur.execute('DELETE FROM lessons WHERE id = ?', (id,))
        else:
            title = request.form.get("title")
            content = request.form.get("content")
            parent_id = request.form.get("parent_id")

            cur.execute(
                'INSERT INTO lessons (title, content, parent_id) VALUES (?, ?, ?)',
                (title, content, parent_id)
            )

        conn.commit()
        conn.close()
        return redirect(url_for('pagina_admin'))


    all_lessons = cur.execute('SELECT * FROM lessons').fetchall()
    conn.close()
    return render_template('admin.html', lessons=all_lessons)

    
@app.route('/lessons/<int:lesson_id>')
def view_lesson(lesson_id):
    conn = get_db()

    cur = conn.cursor()

    lesson = cur.execute(
    'SELECT * FROM lessons WHERE id = ?',
    (lesson_id,)).fetchone()
    all_lessons = cur.execute('SELECT * FROM lessons').fetchall()
    conn.close()
    return render_template('index.html', featured=lesson, lessons=all_lessons)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

