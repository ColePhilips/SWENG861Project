# test_api.py

import pytest
from unittest.mock import patch, MagicMock
from api import app  # Import the app from your api.py

# Create a test client
@pytest.fixture
def client():
    app.config["MONGO_URI"] = "mongodb+srv://ColePhilips:MongoDBDragon22!@monsterhunterdb.3kgwi.mongodb.net/test_db?retryWrites=true&w=majority&appName=MonsterHunterDB"  # Use a test database
    with app.test_client() as client:
        yield client

# Mock MongoDB
@pytest.fixture
def mock_mongo():
    with patch('api.mongo') as mock:
        # Set up mock for Tasks collection
        mock.db.Tasks = MagicMock()
        mock.db.Tasks.find.return_value = []  # Default to empty list for find
        mock.db.Tasks.find_one.return_value = None  # Ensure no task exists by default
        mock.db.Tasks.count_documents.return_value = 0  # Ensure count is 0 by default

        # Set up mock for monsters collection
        mock.cx['mhw_db']['monsters'] = MagicMock()
        mock.cx['mhw_db']['monsters'].find.return_value = []  # Default to empty list for find
        mock.cx['mhw_db']['monsters'].find_one.return_value = None  # Ensure no monster exists by default
        mock.cx['mhw_db']['monsters'].count_documents.return_value = 0  # Ensure count is 0 by default

        yield mock

def test_create_task(client, mock_mongo):
    response = client.post('/Tasks', json={"Task": "Test Task", "id": 1})
    assert response.status_code == 200
    assert b'Test Task' in response.data
    mock_mongo.db.Tasks.insert_one.assert_called_once()

def test_create_task_without_description(client, mock_mongo):
    response = client.post('/Tasks', json={"id": 1})
    assert response.status_code == 400
    assert b'Task description is required!' in response.data

def test_get_all_tasks(client, mock_mongo):
    mock_mongo.db.Tasks.find.return_value = [{"id": 1, "Task": "Test Task 1"}, {"id": 2, "Task": "Test Task 2"}]
    response = client.get('/Tasks')
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_task_by_id(client, mock_mongo):
    mock_mongo.db.Tasks.find_one.return_value = {"id": 1, "Task": "Test Task"}
    response = client.get('/Tasks/1')
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_get_nonexistent_task(client, mock_mongo):
    response = client.get('/Tasks/999')
    assert response.status_code == 404
    assert b'Task not found' in response.data

def test_update_task(client, mock_mongo):
    mock_mongo.db.Tasks.find_one.return_value = {"id": 1, "Task": "Old Task"}
    response = client.put('/Tasks/1', json={"Task": "Updated Task"})
    assert response.status_code == 200
    assert b'Updated Task' in response.data
    mock_mongo.db.Tasks.update_one.assert_called_once()

def test_update_task_without_description(client, mock_mongo):
    mock_mongo.db.Tasks.find_one.return_value = {"id": 1, "Task": "Old Task"}
    response = client.put('/Tasks/1', json={})
    assert response.status_code == 400
    assert b'Task description is required!' in response.data

def test_update_nonexistent_task(client, mock_mongo):
    mock_mongo.db.Tasks.find_one.return_value = None
    mock_mongo.db.Tasks.update_one.return_value.matched_count = 0
    response = client.put('/Tasks/999', json={"Task": "Updated Task"})
    assert response.status_code == 404
    assert b'Task not found!' in response.data

def test_delete_task(client, mock_mongo):
    mock_mongo.db.Tasks.find_one.return_value = {"id": 1, "Task": "Test Task"}
    response = client.delete('/Tasks/1')
    assert response.status_code == 200
    assert b'Task deleted successfully!' in response.data
    mock_mongo.db.Tasks.delete_one.assert_called_once()

def test_delete_nonexistent_task(client, mock_mongo):
    mock_mongo.db.Tasks.delete_one.return_value.deleted_count = 0
    response = client.delete('/Tasks/999')
    assert response.status_code == 404
    assert b'Task not found!' in response.data

def test_get_all_monsters(client, mock_mongo):
    mock_mongo.cx['mhw_db']['monsters'].find.return_value = [
 {"id": 1, "name": "Monster1"},
        {"id": 2, "name": "Monster2"}
    ]
    response = client.get('/Monsters')
    assert response.status_code == 200
    assert len(response.get_json()) == 2
    assert response.get_json() == [
        {"id": 1, "name": "Monster1"},
        {"id": 2, "name": "Monster2"}
    ]

def test_get_no_monsters(client, mock_mongo):
    response = client.get('/Monsters')
    assert response.status_code == 200
    assert response.get_json() == []

if __name__ == '__main__':
    pytest.main()