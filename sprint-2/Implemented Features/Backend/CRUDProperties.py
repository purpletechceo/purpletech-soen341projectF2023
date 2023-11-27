import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Read data from CSV file
df = pd.read_csv('data.csv')

# Create a tabbed interface
st.set_page_config(page_title="Property Management", page_icon="🏠")

selected_tab = st.sidebar.radio("Select a tab:", ["View Properties", "Manage Properties"])

if selected_tab == "View Properties":
    # View Properties Page
    st.title("View Properties")
    st.subheader("Filter and view property details.")

    gd = GridOptionsBuilder.from_dataframe(df)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    gd.configure_column('image', hide=True)
    gridoptions = gd.build()

    # Dropdown filter for house type
    selected_house_type = st.selectbox('Select House Type', ['All'] + list(df['house type'].unique()))

    if selected_house_type != 'All':
        filtered_df = df[df['house type'] == selected_house_type]
    else:
        filtered_df = df

    grid_table = AgGrid(filtered_df, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

    st.header('Selected Property')

    if grid_table['selected_rows']:
        selected_property = grid_table['selected_rows'][0]
        selected_property_index = filtered_df[filtered_df['house address'] == selected_property['house address']].index[0] + 1  # Calculate the row number
        image_column, description_column = st.columns(2)

        with image_column:
            st.image(selected_property['image'], caption='Selected Property Image', use_column_width=True)

        with description_column:
            st.write(f"Row Number: {selected_property_index}\n")
            st.write(f"House Address: {selected_property['house address'].title()}\n")
            st.write(f"House Type: {selected_property['house type'].title()}\n")
            st.write(f"Number of Rooms: {int(selected_property['number of rooms'])}\n")
            st.write(f"Number of Bathrooms: {int(selected_property['number of bathrooms'])}")

    else:
        st.write('No property selected.')

elif selected_tab == "Manage Properties":
    # Manage Properties Page
    st.title("Manage Properties")
    st.subheader("Add, update, and delete property details.")

    # Create operation
    st.header("Add New Property")
    new_house_address = st.text_input("House Address")
    new_house_type = st.text_input("House Type")
    new_num_rooms = st.text_input("Number of Rooms")
    new_num_bathrooms = st.text_input("Number of Bathrooms")
    new_image = st.text_input("Image URL")
    if st.button("Add New Property"):
        new_row = pd.DataFrame([{
            'house address': new_house_address.title(),
            'house type': new_house_type.title(),
            'number of rooms': new_num_rooms,
            'number of bathrooms': new_num_bathrooms,
            'image': new_image,
            'status': 'Pending'
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data.csv', index=False)

    # Update operation
    st.header("Update Property")
    row_to_update = st.number_input("Row Index to Update", min_value=0, max_value=len(df) - 1, step=1, value=0)
    update_house_address = st.text_input("House Address", value=df.at[row_to_update, 'house address'].title())
    update_house_type = st.text_input("House Type", value=df.at[row_to_update, 'house type'].title())
    update_num_rooms = st.text_input("Number of Rooms", value=df.at[row_to_update, 'number of rooms'])
    update_num_bathrooms = st.text_input("Number of Bathrooms", value=df.at[row_to_update, 'number of bathrooms'])
    update_image = st.text_input("Image URL", value=df.at[row_to_update, 'image'])
    if st.button("Update Property"):
        df.at[row_to_update, 'house address'] = update_house_address.title()
        df.at[row_to_update, 'house type'] = update_house_type.title()
        df.at[row_to_update, 'number of rooms'] = update_num_rooms
        df.at[row_to_update, 'number of bathrooms'] = update_num_bathrooms
        df.at[row_to_update, 'image'] = update_image
        df.to_csv('data.csv', index=False)

    # Delete operation
    st.header("Delete Property")
    row_to_delete = st.number_input("Row Index to Delete", min_value=0, max_value=len(df) - 1, step=1, value=0)
    if st.button("Delete Property"):
        df.drop(index=row_to_delete, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv('data.csv', index=False)

# Boilerplate code to hide Streamlit's default menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
