import pytest
import json
from app import app, db, User
from flask import jsonify
from unittest.mock import patch


@pytest.fixture
def client():
    # Setting up a test client for Flask
    with app.app_context():  # Ensuring the app context is available
        with app.test_client() as client:
            db.create_all()  # Creates the database schema inside the app context
            yield client
            # After each test, drop the database
            db.drop_all()


def test_home(client):
    """Test the home route"""
    response = client.get('/')
    assert response.data == b'Okta Authentication with Flask Backend'
    assert response.status_code == 200


@patch('requests.post')
def test_verify_user_new_user(mock_post, client):
    """Test the /verify route for a valid new user"""
    # Mocking the Okta introspect response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "active": True,
        "sub": "user123",
        "username": "user123",
        "exp": 1700000000
    }

    headers = {
        'Authorization': 'Bearer valid-okta-token'
    }

    # Sending a POST request to the /verify route
    response = client.post('/verify', headers=headers)
    
    # Assert that the response is a success (status code 200)
    assert response.status_code == 200
    
    # Assert that the user was verified and stored
    user = User.query.filter_by(okta_id="user123").first()
    assert user is not None
    assert user.email == "user123"
    
    response_json = json.loads(response.data)
    assert response_json["message"] == "User verified and stored successfully"
    assert response_json["user"]["sub"] == "user123"


@patch('requests.post')
def test_verify_user_existing_user(mock_post, client):
    """Test the /verify route for an existing user"""
    # Add a user to the database
    existing_user = User(okta_id="existing_user", email="existing_user@example.com")
    db.session.add(existing_user)
    db.session.commit()

    # Mocking the Okta introspect response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "active": True,
        "sub": "existing_user",
        "username": "existing_user",
        "exp": 1700000000
    }

    headers = {
        'Authorization': 'Bearer valid-okta-token'
    }

    # Sending a POST request to the /verify route
    response = client.post('/verify', headers=headers)
    
    # Assert that the response is a success (status code 200)
    assert response.status_code == 200

    # Assert that the existing user is not duplicated
    user = User.query.filter_by(okta_id="existing_user").first()
    assert user is not None
    assert user.email == "existing_user@example.com"
    
    response_json = json.loads(response.data)
    assert response_json["message"] == "User verified and stored successfully"
    assert response_json["user"]["sub"] == "existing_user"


@patch('requests.post')
def test_verify_invalid_token(mock_post, client):
    """Test the /verify route for an invalid token"""
    # Mocking the Okta introspect response with an invalid token
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "active": False
    }

    headers = {
        'Authorization': 'Bearer invalid-okta-token'
    }

    # Sending a POST request to the /verify route
    response = client.post('/verify', headers=headers)
    
    # Assert that the response is a failure (status code 401)
    assert response.status_code == 401
    response_json = json.loads(response.data)
    assert response_json["error"] == "Invalid token"


def test_missing_token(client):
    """Test the /verify route when token is missing"""
    response = client.post('/verify')
    
    # Assert that the status code is 400 because the token is missing
    assert response.status_code == 400
    
    # Assert that the response contains the expected error message
    response_json = json.loads(response.data)
    assert response_json["error"] == "Token is missing"
