from flask import Flask, jsonify, request, render_template, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from ai_agent import get_task_priority, get_daily_recommendation

app = Flask(__name__)
app.secret_key = 'smart_task_secret_key' 

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
   
    conn.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
   
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        deadline TEXT,
        priority INTEGER,
        duration INTEGER,
        category TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')
    conn.commit()
    conn.close()

init_db()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password) 

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Username already exists!")
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid username or password!")

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('login'))



@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login')) 
    return render_template('index.html', username=session['username'])

@app.route('/tasks', methods=['POST'])
def create_task():
    if 'user_id' not in session: return jsonify({'error': 'Unauthorized'}), 401
    data = request.get_json()

    ai_result = get_task_priority(
        title=data['title'],
        deadline=data.get('deadline', 'No deadline'),
        duration=data.get('duration', 60),
        category=data.get('category', 'General')
    )
    ai_score = ai_result.get('score', 5)

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tasks (user_id, title, deadline, priority, duration, category)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session['user_id'], data['title'], data.get('deadline'), ai_score, data.get('duration'), data.get('category')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task created successfully!'}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    if 'user_id' not in session: return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks WHERE status='pending' AND user_id=? ORDER BY priority DESC", (session['user_id'],)).fetchall()
    conn.close()
    return jsonify({'tasks': [dict(row) for row in tasks]})

@app.route('/tasks/<int:task_id>/done', methods=['PUT'])
def mark_task_done(task_id):
    if 'user_id' not in session: return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status='completed' WHERE id=? AND user_id=?", (task_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task marked as done!'})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user_id' not in session: return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id=? AND user_id=?", (task_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully!'})

@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    if 'user_id' not in session: return jsonify({'error': 'Unauthorized'}), 401
    conn = get_db_connection()
    tasks = conn.execute("SELECT id, title, deadline, priority, duration, category FROM tasks WHERE status='pending' AND user_id=? ORDER BY priority DESC", (session['user_id'],)).fetchall()
    conn.close()

    if not tasks:
        return jsonify({"message": "You have no pending tasks! Enjoy your day!"})

    task_list = [dict(row) for row in tasks]
    ai_recommendation = get_daily_recommendation(task_list)
    return jsonify(ai_recommendation)

if __name__ == '__main__':
    app.run(debug=True)