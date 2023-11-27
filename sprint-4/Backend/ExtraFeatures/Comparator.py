import streamlit as st
import pandas as pd

# Sample property data (replace this with your own data)

image1 = 'https://www.forbes.com/advisor/wp-content/uploads/2022/10/what-is-a-townhouse.jpeg.jpg'
image2 = 'https://simpleshowing.ghost.io/content/images/2023/01/GetMedia-1.jpeg'
image3 = 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Forbes_House%2C_Halkin_Street.jpg/330px-Forbes_House%2C_Halkin_Street.jpg'

data = {
    'Property': ['House A', 'House B', 'House C'],
    'Price': [500000, 600000, 450000],
    'Bedrooms': [4, 3, 5],
    'Bathrooms': [3, 2, 4],
    'SquareFeet': [2500, 2000, 3000],
    'image': [image1, image2, image3],
}

# Create a DataFrame
df = pd.DataFrame(data)


# Function to compare properties
def compare_properties(selected_props):
    return df[df['Property'].isin(selected_props)]


st.title("Property Comparator")

# Select properties for comparison
selected_properties = st.multiselect("Select Properties for Comparison", df['Property'])

# Display details for selected properties
if selected_properties:
    compared_properties = compare_properties(selected_properties)

    # Create a new column with HTML image tags
    compared_properties['Image HTML'] = compared_properties['image'].apply(lambda x: f'<img src="{x}" style="max-width:100px;">' if x else '')

    # Drop 'Image' and 'Image HTML' columns before displaying the table
    compared_properties = compared_properties.drop(['image'], axis=1)

    # Plotting features
    st.subheader("Comparison Details")

    # Display transposed table with images
    st.write(compared_properties.set_index('Property').T.to_html(escape=False), unsafe_allow_html=True)
else:
    st.warning("Please select properties for comparison.")
