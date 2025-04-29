from flask import Blueprint, jsonify, request
from datetime import datetime
from app.models import db, Task

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return jsonify({"message": "Welcome to Obsedo"})

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    category = data.get('category')
    priority = data.get('priority', 'medium')
    due_date_raw = data.get('due_date')

    if not title or not category:
        return jsonify({"error": "Missing title or category"}), 400

    try:
        due_date = datetime.fromisoformat(due_date_raw) if due_date_raw else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO 8601."}), 400

    task = Task(title=title, category=category, priority=priority, due_date=due_date)
    db.session.add(task)
    db.session.commit()

    return jsonify(task.serialize()), 201

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.serialize() for task in tasks]), 200

@bp.route('/tasks/random', methods=['GET'])
def get_random_task():
    category = request.args.get('category')
    if category:
        tasks = Task.query.filter_by(category=category, is_completed=False).all()
    else:
        tasks = Task.query.filter_by(is_completed=False).all()

    if not tasks:
        return jsonify({"message": "No available tasks."}), 404

    import random
    task = random.choice(tasks)
    return jsonify(task.serialize()), 200

@bp.route('/tasks/<int:task_id>/complete', methods=['PATCH'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.is_completed = True
    db.session.commit()
    return jsonify(task.serialize()), 200

@bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {task_id} deleted."}), 200
