import unittest
from streamlit_mock import StreamlitTestClient  # You can use a Streamlit test client library like 'streamlit_mock'
from PurchasePromisePatched import *  

class TestMyStreamlitApp(unittest.TestCase):

    def setUp(self):
        # Create a Streamlit test client
        self.test_client = StreamlitTestClient()

    def test_login_with_valid_credentials(self):
        # Test logging in with valid credentials
        self.test_client.write("Username: user1")
        self.test_client.write("Password: pass1")
        self.test_client.press("Login")
        response = self.test_client.read()
        self.assertIn("Welcome, your_valid_username!", response)

    def test_login_with_invalid_credentials(self):
        # Test logging in with invalid credentials
        self.test_client.write("Username: user10")
        self.test_client.write("Password: user10")
        self.test_client.press("Login")
        response = self.test_client.read()
        self.assertIn("Invalid credentials. Please try again.", response)

        # Simulate creating a new listing
        self.test_client.press("CRUD Operations")
        self.test_client.write("House Address: New House")
        self.test_client.write("House Type: Apartment")
        self.test_client.write("Number of Rooms: 3")
        self.test_client.write("Number of Bathrooms: 2")
        self.test_client.write("Image URL: http://example.com/image.jpg")
        self.test_client.write("Location: New Location")
        self.test_client.press("Add New Row")
        
        response = self.test_client.read()
        self.assertIn("New House", response)  # Check if the new listing is displayed

    def test_update_existing_listing(self):
        # Test updating an existing listing
        self.test_client.write("Username: your_valid_username")
        self.test_client.write("Password: your_valid_password")
        self.test_client.press("Login")

        # Simulate updating an existing listing
        self.test_client.press("CRUD Operations")
        self.test_client.write("Row Index to Update: 0")
        self.test_client.write("House Address: Updated House")
        self.test_client.press("Update Row")

        # Verify if the listing is updated
        self.test_client.press("View Data")
        response = self.test_client.read()
        self.assertIn("Updated House", response)  # Check if the updated listing is displayed

    def test_delete_listing(self):
        # Test deleting a listing
        self.test_client.write("Username: your_valid_username")
        self.test_client.write("Password: your_valid_password")
        self.test_client.press("Login")

        # Simulate deleting an existing listing
        self.test_client.press("CRUD Operations")
        self.test_client.write("Row Index to Delete: 0")
        self.test_client.press("Delete Row")

        # Verify if the listing is deleted
        self.test_client.press("View Data")
        response = self.test_client.read()
        self.assertNotIn("Deleted House", response)  # Check if the deleted listing is not displayed

if __name__ == '__main__':
    unittest.main()
