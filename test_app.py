

import pytest
import os
from app import app, students_collection

@pytest.fixture
def client():
    # Set environment variables for testing
    os.environ['MONGO_HOST'] = 'localhost'
    os.environ['MONGO_PORT'] = '27017'
    os.environ['MONGO_USERNAME'] = 'root'
    os.environ['MONGO_PASSWORD'] = 'pass'
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"Student Information" in rv.data

def test_add_student(client):
    new_student = {
        'name': 'Test Student',
        'roll_number': '12345',
        'grade': 'A'
    }
    rv = client.post('/add_student', data=new_student)
    assert rv.status_code == 302

    rv = client.get('/')
    assert b"Test Student" in rv.data
    assert b"12345" in rv.data
    assert b"A" in rv.data
