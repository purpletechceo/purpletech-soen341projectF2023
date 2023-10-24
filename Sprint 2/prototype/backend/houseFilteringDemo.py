import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Load data from data.csv file
df = pd.read_csv('data.csv')

# Create a copy of the DataFrame without the 'email' column
df_filtered = df[['house address', 'house type', 'number of rooms', 'number of bathrooms', 'image']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('image', hide=True)
gridoptions = gd.build()

# Initialize the visit request DataFrame
visit_request_df = pd.DataFrame(columns=["b_email", "property", "fname", "lname", "pnumber", "email", "date_time"])

selected_tab = st.sidebar.radio("Select a tab:", ["View Data", "CRUD Operations"])

if selected_tab == "View Data":
    # Dropdown filter for house type
    selected_house = st.selectbox('Select Property Type', ['All'] + list(df_filtered['house type'].unique()))

    # Display the ag-Grid with house information
    st.write("## List of Properties")

    if selected_house != 'All':
        filtered_df = df_filtered[df_filtered['house type'] == selected_house]
    else:
        filtered_df = df_filtered

    grid_table = AgGrid(filtered_df, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

    if grid_table['selected_rows']:
        selected_row = grid_table['selected_rows'][0]
        image_column, description_column = st.columns(2)

        with image_column:
            st.image(selected_row['image'], caption='Selected Image', use_column_width=True)

        with description_column:
            st.write(f"House Address: {selected_row['house address']}\n"
                     f"\nHouse Type: {selected_row['house type']}\n"
                     f"\nNumber of Rooms: {selected_row['number of rooms']}\n"
                     f"\nNumber of Bathrooms: {selected_row['number of bathrooms']}")

        if st.button("Request Visit"):

            # Use st.form to wrap all the inputs
            with st.form(key='visit_request_form'):
                fname = st.text_input("First Name")
                lname = st.text_input("Last Name")
                pnumber = st.text_input("Phone Number")
                email = st.text_input("Email")
                date = st.date_input("Visit Date", value="today", key='visit_date')
                time = st.time_input("Visit Time", value="now", key='visit_time')
                submitted = st.form_submit_button("Submit Request")

            if submitted:
                # Process the form submission
                broker_email = selected_row['broker_email']
                new_request = pd.DataFrame({
                    "b_email": [broker_email],
                    "property": [selected_row['house address']],
                    "fname": [fname],
                    "lname": [lname],
                    "pnumber": [pnumber],
                    "email": [email],
                    "date": [date],
                    "time": [time]
                })

                # Append the new request to the visit request DataFrame
                visit_request_df = visit_request_df.append(new_request, ignore_index=True)

                st.write("Request submitted successfully!")

    # Display the table with visit requests
    st.write("## Visit Requests")
    if not visit_request_df.empty:
        st.dataframe(visit_request_df, height=250)
    else:
        st.info("No visit requests yet.")

elif selected_tab == "CRUD Operations":
    # CRUD operations code goes here

    st.write("### CRUD Operations")

    # CREATE
    st.write("#### Create")
    new_house_address = st.text_input("House Address")
    new_house_type = st.text_input("House Type")
    new_num_rooms = st.text_input("Number of Rooms")
    new_num_bathrooms = st.text_input("Number of Bathrooms")
    new_image = st.text_input("Image URL")
    if st.button("Add New Row"):
        new_row = pd.DataFrame([{
            'house address': new_house_address,
            'house type': new_house_type,
            'number of rooms': new_num_rooms,
            'number of bathrooms': new_num_bathrooms,
            'image': new_image,
            'status': 'Pending'
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv('data.csv', index=False)

    # UPDATE
    st.write("#### Update")
    row_to_update = st.number_input("Row Index to Update", min_value=0, max_value=len(df) - 1, step=1, value=0)
    update_house_address = st.text_input("House Address", value=df.at[row_to_update, 'house address'])
    update_house_type = st.text_input("House Type", value=df.at[row_to_update, 'house type'])
    update_num_rooms = st.text_input("Number of Rooms", value=df.at[row_to_update, 'number of rooms'])
    update_num_bathrooms = st.text_input("Number of Bathrooms", value=df.at[row_to_update, 'number of bathrooms'])
    update_image = st.text_input("Image URL", value=df.at[row_to_update, 'image'])
    if st.button("Update Row"):
        df.at[row_to_update, 'house address'] = update_house_address
        df.at[row_to_update, 'house type'] = update_house_type
        df.at[row_to_update, 'number of rooms'] = update_num_rooms
        df.at[row_to_update, 'number of bathrooms'] = update_num_bathrooms
        df.at[row_to_update, 'image'] = update_image
        df.to_csv('data.csv', index=False)

    # DELETE
    st.write("#### Delete")
    row_to_delete = st.number_input("Row Index to Delete", min_value=0, max_value=len(df) - 1, step=1, value=0)
    if st.button("Delete Row"):
        df.drop(index=row_to_delete, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv('data.csv', index=False)

# Boiler plate code:
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
