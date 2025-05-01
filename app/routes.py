import os
import json
import random
from datetime import datetime

from flask import Blueprint, jsonify, request
from openai import OpenAI

from app.models import db, Task

bp = Blueprint("routes", __name__)


@bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    category = data.get("category")
    priority = data.get("priority", "medium")
    due_date_raw = data.get("due_date")

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


@bp.route("/tasks", methods=["GET"])
def get_tasks():
    query = Task.query

    priority = request.args.get("priority")
    category = request.args.get("category")
    is_completed = request.args.get("is_completed")
    sort = request.args.get("sort")

    if priority:
        query = query.filter_by(priority=priority)
    if category:
        query = query.filter_by(category=category)
    if is_completed is not None:
        is_completed_bool = is_completed.lower() == "true"
        query = query.filter_by(is_completed=is_completed_bool)
    if sort == "due_date":
        query = query.order_by(Task.due_date.asc())

    tasks = query.all()
    return jsonify([task.serialize() for task in tasks]), 200


@bp.route("/tasks/random", methods=["GET"])
def get_random_task():
    category = request.args.get("category")
    if category:
        tasks = Task.query.filter_by(category=category, is_completed=False).all()
    else:
        tasks = Task.query.filter_by(is_completed=False).all()

    if not tasks:
        return jsonify({"message": "No available tasks."}), 404

    import random

    task = random.choice(tasks)
    return jsonify(task.serialize()), 200


@bp.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.is_completed = True
    db.session.commit()
    return jsonify(task.serialize()), 200


@bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": f"Task {task_id} deleted."}), 200


@bp.route("/generate-tasks", methods=["POST"])
def generate_tasks_from_goal():
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    data = request.get_json()
    goal = data.get("goal")
    model = data.get("model", "gpt-3.5-turbo-0125")
    temperature = data.get("temperature", 0.7)
    max_tasks = data.get("max_tasks", 5)

    if not goal:
        return jsonify({"error": "Missing 'goal' in request body"}), 400

    prompt = f"""
        You're an intelligent task manager. The user wants to achieve the following goal:

        "{goal}"

        Break it down into {max_tasks} concrete tasks. For each task, return:
        - title
        - category (e.g. focus, admin, travel, social)
        - priority (low, medium, high)
        - optional due date (in ISO 8601 format, or null if none)

        Return as JSON in the following format:

        [
        {{
            "title": "...",
            "category": "...",
            "priority": "...",
            "due_date": "..." or null
        }},
        ...
        ]
        """

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful task planner."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )

        content = response.choices[0].message.content

        try:
            tasks = json.loads(content)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse response from OpenAI"}), 502

        created = []
        for item in tasks:
            due = item.get("due_date")
            due_date = datetime.fromisoformat(due) if due else None
            task = Task(
                title=item["title"],
                category=item["category"],
                priority=item.get("priority", "medium"),
                due_date=due_date,
            )
            db.session.add(task)
            created.append(task)

        db.session.commit()
        return jsonify([t.serialize() for t in created]), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
