import pandas as pd
import os
import pytest
from tests.refactorLogin import login_function 

@pytest.fixture
def setup_teardown():
    # Setup: Create an initial user data CSV file for testing
    initial_user_data = pd.DataFrame({
        'username': ['user1', 'user2'],
        'password': ['pass1', 'pass2']
    })
    initial_user_data.to_csv("userdata.csv", index=False)

    yield

    # Teardown: Remove the user data CSV file created for testing
    os.remove("userdata.csv")

def test_successful_login(setup_teardown):
    # Replace these values with valid login credentials
    username = "user1"
    password = "pass1"
    
    result = login_function(username, password)
    
    # Check if the result indicates a successful login
    assert result == f"Welcome, {username}!"

def test_failed_login(setup_teardown):
    # Replace these values with invalid login credentials
    username = "invalid_user"
    password = "invalid_pass"
    
    result = login_function(username, password)
    
    # Check if the result indicates a failed login
    assert result == "Invalid username or password. Please try again."
