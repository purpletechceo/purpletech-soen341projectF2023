import datetime

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder




# Read user data from 'userdata.csv' file
user_data = pd.read_csv('userdata.csv')

valid_usernames = set(user_data['username'])
user_passwords = dict(zip(user_data['username'], user_data['password']))

# Load data from data.csv file
df = pd.read_csv('data.csv')
# Load visits data from 'visits.csv' file



# Create a copy of the DataFrame without the 'email' column
df_filtered = df[['house address', 'house type', 'number of rooms', 'number of bathrooms', 'image','username', 'status']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('image', hide=True)
gridoptions = gd.build()

# Initialize the visit request DataFrame
visit_request_df = pd.DataFrame(columns=["b_email", "property", "fname", "lname", "pnumber", "email", "date_time"])


selected_tab = st.sidebar.radio("Select a tab:", ["View Data", "CRUD Operations", "Your Listings", "Administrator"], key="tab_selection")

# User login interface
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type='password')



# Authentication logic
if st.sidebar.button("Login"):
    if username in valid_usernames and password == user_passwords[username]:
        st.sidebar.success(f"Welcome, {username}!")
        st.session_state.logged_in = True
    else:
        st.sidebar.error("Invalid credentials. Please try again.")
        st.session_state.logged_in = False

# Add a signout button in the sidebar
if getattr(st.session_state, 'logged_in', False):
    logged_in_user = username
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.sidebar.success("You have been successfully signed out.")

    if selected_tab == "View Data":
        # Dropdown filter for house type
        selected_house = st.selectbox('Select Property Type', ['All'] + list(df_filtered['house type'].unique()))

        # Display the ag-Grid with house information
        st.write("## List of Properties")

        if selected_house != 'All':
            filtered_df = df_filtered[df_filtered['house type'] == selected_house]

        else:
            filtered_df = df_filtered


        df_filtered_display =filtered_df[filtered_df['status'] == 'Approved']


        grid_table = AgGrid(df_filtered_display,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, height=250, gridOptions=gridoptions,
                            update_mode=GridUpdateMode.SELECTION_CHANGED)

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

        if grid_table['selected_rows']:
            selected_row = grid_table['selected_rows'][0]



            # Data entry fields for visit request
            st.write("## Request Visit")
            last_name = st.text_input("Last Name", key="last_name")
            first_name = st.text_input("First Name", key="first_name")
            current_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            selected_date = st.date_input("Visit Date", min_value=pd.Timestamp.now().date(), key="visit_date")
            visit_address = st.text_input("Visit Address", key="visit_address")


            # Request Visits button
            if st.button("Request Visits"):
                if last_name and first_name and visit_address:
                    # Create a new DataFrame for visit request with the correct column order
                    visit_request_data = pd.DataFrame({
                        "b_email": [username],
                        "property": [selected_row['house address']],
                        "fname": [first_name],
                        "lname": [last_name],
                        "date_time": [f"{selected_date} {current_time}"],
                        "visit_address": [visit_address]
                    })

                    # Concatenate the visit request data with the existing visits DataFrame
                    visits= pd.read_csv('visits.csv')
                    visit_request_df = pd.concat([visits, visit_request_data], ignore_index=True)
                    visit_request_df.to_csv('visits.csv', index=False)

                    # Display success message
                    st.success("Visit request submitted successfully!")
                else:
                    # Display error message if required fields are not filled
                    st.error("Please fill out all the required fields.")

            # Display user's own visit requests
        st.write("## Your Visit Requests")
        visits_data = pd.read_csv('visits.csv')
        user_visits = visits_data[visits_data['b_email'] == username]


        st.dataframe(user_visits)



    elif selected_tab == "CRUD Operations":

        # Dropdown filter for house type
        selected_house = st.selectbox('Select Property Type', ['All'] + list(df_filtered['house type'].unique()))

        # Display the ag-Grid with house information
        st.write("## Your Listings:")

        listings_df = pd.read_csv('data.csv')


        listings_df_display = listings_df[listings_df['username']== logged_in_user]

        if not listings_df_display.empty:
            grid_table = AgGrid(listings_df_display, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                                height=250, gridOptions=gridoptions,
                                update_mode=GridUpdateMode.SELECTION_CHANGED)

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
        else:
            st.info("You have not created any listings")




        # CRUD operations

        st.write("### CRUD Operations")

        # CREATE
        st.write("#### Create")
        new_house_address = st.text_input("House Address")
        new_house_type = st.text_input("House Type")
        new_num_rooms = st.text_input("Number of Rooms")
        new_num_bathrooms = st.text_input("Number of Bathrooms")
        new_image = st.text_input("Image URL")
        if st.button("Add New Row"):
            # Store the logged-in username in the 'username' column
            new_row = pd.DataFrame([{
                'house address': new_house_address,
                'house type': new_house_type,
                'number of rooms': new_num_rooms,
                'number of bathrooms': new_num_bathrooms,
                'image': new_image,
                'username': logged_in_user,  # Store the logged-in username
                'status': 'Pending'
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv('data.csv', index=False)

        # UPDATE
        st.write("#### Update")
        row_to_update = st.number_input("Row Index to Update", min_value=0, max_value=len(df) - 1, step=1, value=0)
        if df.at[row_to_update, 'username'] == logged_in_user:  # Check if the user created this listing
            update_house_address = st.text_input("House Address", value=df.at[row_to_update, 'house address'])
            update_house_type = st.text_input("House Type", value=df.at[row_to_update, 'house type'])
            update_num_rooms = st.text_input("Number of Rooms", value=df.at[row_to_update, 'number of rooms'])
            update_num_bathrooms = st.text_input("Number of Bathrooms",
                                                 value=df.at[row_to_update, 'number of bathrooms'])
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
        if df.at[row_to_delete, 'username'] == logged_in_user:  # Check if the user created this listing
            if st.button("Delete Row"):
                # Delete only if the user created this listing
                df.drop(index=row_to_delete, inplace=True)
                df.reset_index(drop=True, inplace=True)
                df.to_csv('data.csv', index=False)


    # Add a new tab named "Your Requests"
    elif selected_tab == "Your Listings":
        st.write("## Listing Requests:")

        # Read data from 'data.csv' file
        user_data = pd.read_csv('data.csv')

        # Filter data for the listings made by the logged-in user
        user_listings = user_data[user_data['username'] == logged_in_user]

        if not user_listings.empty:
            # Get the list of properties made by the logged-in user
            user_properties = user_listings['house address'].tolist()

            # Read visit data from 'visits.csv' file
            visits_data = pd.read_csv('visits.csv')

            # Filter visit requests for the properties made by the logged-in user
            user_visits = visits_data[visits_data['property'].isin(user_properties)]

            # Display visit requests for the user's properties
            if not user_visits.empty:
                st.dataframe(user_visits)
            else:
                st.info("No visit requests for your properties.")
        else:
            st.info("No Request For Your Listings")

    elif selected_tab == "Administrator":

        if username == 'admin' and password =='admin':

            st.write("## Admin Operations")

            # Grid Table Display for Admin with Status Visible
            gd = GridOptionsBuilder.from_dataframe(df_filtered)
            gd.configure_selection(selection_mode='single', use_checkbox=True)
            gd.configure_column('image', hide=True)
            gridoptions = gd.build()

            # Display the ag-Grid with house information
            st.write("#### List of Properties to Approve")

            filtered_df = df_filtered

            grid_table = AgGrid(filtered_df,columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, height=250, gridOptions=gridoptions,
                                update_mode=GridUpdateMode.SELECTION_CHANGED)

            if grid_table['selected_rows']:
                selected_row = grid_table['selected_rows'][0]
                image_column, description_column = st.columns(2)

                with image_column:
                    st.image(selected_row['image'], caption='Selected Image', use_column_width=True)

                with description_column:
                    st.write(f"House Address: {selected_row['house address']}\n"
                             f"\nHouse Type: {selected_row['house type']}\n"
                             f"\nNumber of Rooms: {selected_row['number of rooms']}\n"
                             f"\nNumber of Bathrooms: {selected_row['number of bathrooms']}\n")

                # Approve button for houses pending approval
                if selected_row['status'] == 'Pending':

                    if st.button("Approve"):
                        row_num = df[df['house address'] == selected_row['house address']].index[0]
                        df.at[row_num, 'status'] = "Approved"
                        df.to_csv('data.csv', index=False)

                # Delete button for deleting any house
                if st.button("Delete"):
                    row_num = df[df['house address'] == selected_row['house address']].index[0]
                    df.drop(index=row_num, inplace=True)
                    df.reset_index(drop=True, inplace=True)
                    df.to_csv('data.csv', index=False)

            # Admin controls
            st.write("#### Administrator Operations")
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

        else:
            st.warning('Permission Denied')


else:
    # If not logged in, do not display other tabs
    st.warning("Please log in to access the application.")


    # Boilerplate code for hiding Streamlit style
    hide_streamlit_style = """
         <style>
         #MainMenu {visibility: hidden;}
         footer {visibility: hidden;}
         </style>
     """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
