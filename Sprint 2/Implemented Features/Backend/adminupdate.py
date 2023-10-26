import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Read user data from 'userdata.csv' file
user_data = pd.read_csv('userdata.csv')

valid_usernames = set(user_data['username'])
user_passwords = dict(zip(user_data['username'], user_data['password']))

# Load data from data.csv file
df = pd.read_csv('data.csv')

# Create a copy of the DataFrame without the 'email' column
df_filtered = df[['house address', 'house type', 'number of rooms', 'number of bathrooms', 'image', 'status']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('image', hide=True)
gd.configure_column('status', hide=True)
gridoptions = gd.build()

# Initialize the visit request DataFrame
visit_request_df = pd.DataFrame(columns=["b_email", "property", "fname", "lname", "pnumber", "email", "date_time"])

selected_tab = st.sidebar.radio("Select a tab:", ["View Data", "CRUD Operations", "Administrator"], key="tab_selection")

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
    if st.sidebar.button("Sign Out"):
        st.session_state.logged_in = False
        st.sidebar.success("You have been successfully signed out.")

if selected_tab == "Administrator":

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
