import pandas as pd
import numpy as np
import streamlit as st

# Sample data
image1 = 'https://www.forbes.com/advisor/wp-content/uploads/2022/10/what-is-a-townhouse.jpeg.jpg'
image2 = 'https://simpleshowing.ghost.io/content/images/2023/01/GetMedia-1.jpeg'

data = {
    'House': ['House 1', 'House 2'],
    'House Type': ['Townhouse', 'Split Level'],
    'Number of Rooms': ['6', '7'],
    'Number of Bathrooms': ['2', '3'],
    'Image': [image1, image2]
}

df = pd.DataFrame(data)

st.title("Properties CRUDs")

# Function to create a new property
def create_property(df):
    
    st.subheader("Create Property")
    new_address = st.text_input("Enter the new House :")
    new_house_type = st.text_input("Enter the House type:")
    new_num_rooms = st.number_input("Enter the number of rooms:")
    new_num_bathrooms = st.number_input("Enter the number of bathrooms:")

    if st.button("Create Property"):
        new_property = {
            'House': new_address,
            'House Type': new_house_type,
            'Number of Rooms': new_num_rooms,
            'Number of Bathrooms': new_num_bathrooms,
            'Image': image1  
        }
        new_row = pd.DataFrame(new_property, index=[0])
        st.success("Property created successfully!")

# Function to update a property
def update_property(df):
    st.subheader("Update Property")
    property_to_update = st.selectbox("Select a property to update", df['House'])
    new_address = st.text_input("Enter the updated house address:", df.loc[df['House'] == property_to_update, 'House'].values[0])
    new_house_type = st.text_input("Enter the updated house type:", df.loc[df['House'] == property_to_update, 'House Type'].values[0])
    new_num_rooms = st.number_input("Enter the updated number of rooms:", float(df.loc[df['House'] == property_to_update, 'Number of Rooms'].values[0]))
    new_num_bathrooms = st.number_input("Enter the updated number of bathrooms:", float(df.loc[df['House'] == property_to_update, 'Number of Bathrooms'].values[0]))

    if st.button("Update Property"):
        index = df.index[df['house'] == property_to_update][0]
        df.at[index, 'House'] = new_address
        df.at[index, 'House Type'] = new_house_type
        df.at[index, 'Number of Rooms'] = new_num_rooms
        df.at[index, 'Number of Bathrooms'] = new_num_bathrooms
        st.success("Property updated successfully!")

# Function to delete a property
def delete_property(df):
    st.subheader("Delete Property")
    property_to_delete = st.selectbox("Select a property to delete", df['House'])
    if st.button("Delete Property"):
        df = df[df['House'] != property_to_delete]
        st.success("Property deleted successfully!")

create_property(df)  # Call the create property function
update_property(df)  # Call the update property function
delete_property(df)  # Call the delete property function

# Display the property data in a table using st.table
st.subheader("Property Data")
st.table(df)

st.title("Administrator CRUDs")
st.text("This is the administrator dashboard. Following is a table that provides control "
        "over brokers.")

