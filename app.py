from flask import Flask, jsonify, request, render_template
import sqlite3
from ai_agent import get_task_priority, get_daily_recommendation

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    ai_result = get_task_priority(
        title=data['title'],
        deadline=data.get('deadline', 'No deadline'),
        duration=data.get('duration', 60),
        category=data.get('category', 'General')
    )
    ai_score = ai_result.get('score', 5)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (title, deadline, priority, duration, category)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['title'], data.get('deadline'), ai_score, data.get('duration'), data.get('category')))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task created successfully!'}), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = get_db_connection()
    
    tasks = conn.execute("SELECT * FROM tasks WHERE status='pending' ORDER BY priority DESC").fetchall()
    conn.close()
    return jsonify({'tasks': [dict(row) for row in tasks]})


@app.route('/tasks/<int:task_id>/done', methods=['PUT'])
def mark_task_done(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status='completed' WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task marked as done!'})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully!'})


@app.route('/recommendation', methods=['GET'])
def get_recommendation():
    conn = get_db_connection()
    tasks = conn.execute("SELECT id, title, deadline, priority, duration, category FROM tasks WHERE status='pending' ORDER BY priority DESC").fetchall()
    conn.close()

    if not tasks:
        return jsonify({"message": "You have no pending tasks! Enjoy your day!"})

    task_list = [dict(row) for row in tasks]
    ai_recommendation = get_daily_recommendation(task_list)
    return jsonify(ai_recommendation)

if __name__ == '__main__':
    app.run(debug=True)