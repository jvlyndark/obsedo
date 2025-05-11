import pytest
from app import create_app, db
from app.models import Task


@pytest.fixture
def client():
    test_config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"}
    app = create_app(test_config)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_get_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_task(client):
    data = {"title": "Test Task", "category": "dev", "priority": "high"}
    response = client.post("/tasks", json=data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["title"] == "Test Task"
    assert json_data["category"] == "dev"


def test_get_tasks_after_create(client):
    with client.application.app_context():
        task = Task(title="Foo", category="admin")
        db.session.add(task)
        db.session.commit()

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.get_json()) == 1
