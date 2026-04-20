# ---
# created: 14 Apr 2026
# author: kaedonkers
# modified: 14 Apr 2026
# ---
# Test API endpoints

from app import main, database

# TODO: Check content of todo items that are returned
# Tests
def test_server_is_live(test_client):
    response = test_client.get(url="/todos")
    assert response.status_code == 200

def test_create_single_todo(test_client):
    response = test_client.post(
        url="/todos", 
        json={
            "title": "test_create_single_todo",
            "description": "Create a new todo for testing create_single_todo().",
            },
        )
    assert response.status_code == 200

def test_read_all_todos(test_client):
    response = test_client.get(url="/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_single_todo(test_client):
    # First create a todo to ensure there is at least one
    create_response = test_client.post(
        url="/todos", 
        json={
            "title": "test_read_single_todo", 
            "description": "Create a new todo for testing read_single_todo().",
            },
        )
    assert create_response.status_code == 200
    created_todo = create_response.json()
    # Now read the created todo
    response = test_client.get(url=f"/todos/{created_todo['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created_todo["id"]

def test_update_single_todo(test_client):
    # First create a todo to ensure there is at least one
    create_response = test_client.post(
        url="/todos", 
        json={
            "title": "test_update_single_todo", 
            "description": "Create a new todo for testing update_single_todo().",
            },
        )
    assert create_response.status_code == 200
    created_todo = create_response.json()
    # Now update the created todo
    response = test_client.patch(
        url=f"/todos/{created_todo['id']}", 
        json={"completed": True},
        )
    assert response.status_code == 200
    assert response.json()["completed"] == True

def test_delete_single_todo(test_client):
    # First create a todo to ensure there is at least one
    create_response = test_client.post(
        url="/todos", 
        json={
            "title": "test_delete_single_todo", 
            "description": "Create a new todo for testing delete_single_todo().",
            },
        )
    assert create_response.status_code == 200
    created_todo = create_response.json()
    # Now delete the created todo
    response = test_client.delete(url=f"/todos/{created_todo['id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"

def test_delete_all_todos(test_client):
    # First create a todo to ensure there is at least one
    create_response = test_client.post(
        url="/todos", 
        json={
            "title": "test_delete_all_todos", 
            "description": "Create a new todo for testing delete_all_todos().",
            },
        )
    assert create_response.status_code == 200
    # Create another todo to ensure there are multiple
    create_response = test_client.post(
        url="/todos", 
        json={
            "title": "test_delete_all_todos_2", 
            "description": "Create another todo for testing delete_all_todos().",
            },
        )
    assert create_response.status_code == 200
    # Now delete all todos
    response = test_client.delete(url="/todos/")
    assert response.status_code == 200
    assert response.json()["message"] == "All todos deleted successfully"

def test_read_single_todo_not_found(test_client):
    # Attempt to read a non-existent todo
    # NB: Assumes ID 999999 does not exist in test database
    response = test_client.get(url="/todos/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"

