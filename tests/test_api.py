# ---
# created: 14 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Test API endpoints

from fastapi.testclient import TestClient

from app import main, database

# NB: Could setup in-memory database and override get_db for more isolated testing, 
# e.g. SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# but for simplicity I'll just test against the actual database 

# Tests
def test_server_is_up():
    client = TestClient(main.app)
    response = client.get(url="/todos")
    assert response.status_code == 200

def test_create_single_todo():
    client = TestClient(main.app)
    response = client.post(
        url="/todos", 
        json={
            "title": "test_create_single_todo",
            "description": "Create a new todo for testing create_single_todo().",
            },
        )
    assert response.status_code == 200

def test_read_all_todos():
    client = TestClient(main.app)
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_single_todo():
    client = TestClient(main.app)
    # First create a todo to ensure there is at least one
    create_response = client.post(
        url="/todos", 
        json={
            "title": "test_read_single_todo", 
            "description": "Create a new todo for testing read_single_todo().",
            },
        )
    assert create_response.status_code == 200
    created_todo = create_response.json()
    # Now read the created todo
    response = client.get(url=f"/todos/{created_todo['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_todo["id"]

def test_update_single_todo():
    client = TestClient(main.app)
    # First create a todo to ensure there is at least one
    create_response = client.post(
        url="/todos", 
        json={
            "title": "test_update_single_todo", 
            "description": "Create a new todo for testing update_single_todo().",
            },
        )
    assert create_response.status_code == 200
    created_todo = create_response.json()
    # Now update the created todo
    response = client.patch(
        url=f"/todos/{created_todo['id']}", 
        json={"completed": True},
        )
    assert response.status_code == 200
    assert response.json()["completed"] == True

def test_delete_single_todo():
    client = TestClient(main.app)
    # First create a todo to ensure there is at least one
    create_response = client.post(
        url="/todos", 
        json={
            "title": "test_delete_single_todo", 
            "description": "Create a new todo for testing delete_single_todo().",
            },
        )
    assert create_response.status_code == 200
    created_todo = create_response.json()
    # Now delete the created todo
    response = client.delete(url=f"/todos/{created_todo['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"

def test_delete_all_todos():
    client = TestClient(main.app)
    # First create a todo to ensure there is at least one
    create_response = client.post(
        url="/todos", 
        json={
            "title": "test_delete_all_todos", 
            "description": "Create a new todo for testing delete_all_todos().",
            },
        )
    assert create_response.status_code == 200
    # Create another todo to ensure there are multiple
    create_response = client.post(
        url="/todos", 
        json={
            "title": "test_delete_all_todos_2", 
            "description": "Create another todo for testing delete_all_todos().",
            },
        )
    assert create_response.status_code == 200
    # Now delete all todos
    response = client.delete(url="/todos/")
    assert response.status_code == 200
    assert response.json()["message"] == "All todos deleted successfully"

def test_read_single_todo_not_found():
    client = TestClient(main.app)
    response = client.get(url="/todos/999999")  # Assuming this ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"
