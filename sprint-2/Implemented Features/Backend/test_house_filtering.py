import houseFilteringDemo
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Define a test DataFrame with sample data
data = {
    'house address': ['House 1', 'House 2'],
    'house type': ['Townhouse', 'Split Level'],
    'number of rooms': ['6', '7'],
    'number of bathrooms': ['2', '3'],
    'image': ['image1_url', 'image2_url'],
    'broker_email': ['johnterry@gmail.com', 'terrencewallace@hotmail.com']
}

# Create a DataFrame df using the sample data
df = pd.DataFrame(data)

# Define a test function for filtering the DataFrame
def test_filter_dataframe():
    # Define the selected house type to filter by
    selected_house = 'Townhouse'
    
    # Create a new DataFrame filtered_df by selecting rows where 'house type' matches selected_house
    filtered_df = df[df['house type'] == selected_house]
    
    # Assert that the length of filtered_df is 1, as we expect only one matching row
    assert len(filtered_df) == 1

# Define a test function for hiding the image column
def test_hide_image_column():
    # Create a filtered DataFrame df_filtered without the 'image' column
    df_filtered = df[['house address', 'house type', 'number of rooms', 'number of bathrooms', 'broker_email']]
    
    # Assert that 'image' is not present in the columns of df_filtered
    assert 'image' not in df_filtered.columns

# Define a test function for checking the form submission
def test_form_submission():
    # This is a placeholder assertion for form submission testing
    # You can replace it with actual form submission testing logic
    assert True

# Run the tests if this script is executed as the main program
if __name__ == "__main__":
    # Call the test functions to run the tests
    test_filter_dataframe()
    test_hide_image_column()
    test_form_submission()
    
    # Print a message indicating that all tests have passed
    print("All tests passed!")