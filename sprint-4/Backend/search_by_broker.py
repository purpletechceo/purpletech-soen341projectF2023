
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

#save to csv:

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    if not pd.io.common.file_exists(filename):
        df.to_csv(filename, index=False)
    else:
        existing_data = pd.read_csv(filename)
        updated_data = pd.concat([existing_data, df], ignore_index=True)
        updated_data.to_csv(filename, index=False)


# Read user data from 'userdata.csv' file
user_data = pd.read_csv('userdata.csv')

valid_usernames = set(user_data['username'])
user_passwords = dict(zip(user_data['username'], user_data['password']))

# Load data from data.csv file
df = pd.read_csv('data.csv')
# Load visits data from 'visits.csv' file



# Create a copy of the DataFrame without the 'email' column
df_filtered = df[['house address', 'house type', 'number of rooms', 'number of bathrooms', 'image','username', 'status', 'location']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('image', hide=True)
gridoptions = gd.build()

# Initialize the visit request DataFrame
visit_request_df = pd.DataFrame(columns=["b_email", "property", "fname", "lname", "pnumber", "email", "date_time"])


# User login interface

userCreds= pd.read_csv('current_user.csv')

username = userCreds['current logged in user'][0]
password = userCreds['pass'][0]



# Authentication logic

if username in valid_usernames and password == user_passwords[username]:
        st.success(f"Welcome, {username}!")
        st.session_state.logged_in = True
else:
    st.sidebar.error("Invalid credentials. Please try again.")
    st.session_state.logged_in = False

logged_in_user = username



# ADD MINH'S MODIFICATIONS LATER

# Load data from 'brokerinfo.csv' file
df = pd.read_csv('info.csv')

# Create a copy of the DataFrame with the selected columns
df_filtered = df[
    ['username', 'FirstName', 'LastName', 'Phone', 'Email', 'License Number', 'Agency', 'ImageURL']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('ImageURL', hide=True)
gridoptions = gd.build()

# Keyword search field
search_keyword = st.text_input('Keyword Search', '')

# Filter the DataFrame based on the search keyword


b_df_filtered = df_filtered[df_filtered['username'] != logged_in_user]

b_filtered_df = b_df_filtered[
    df_filtered.apply(lambda row: any(search_keyword.lower() in str(cell).lower() for cell in row), axis=1)]

# Display the filtered data
st.write("## List of Brokers")

if len(b_filtered_df) > 0:
    grid_table = AgGrid(b_filtered_df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, height=250,
                        gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)
    if grid_table['selected_rows']:
        selected_row = grid_table['selected_rows'][0]
        first_name = selected_row['FirstName']
        last_name = selected_row['LastName']
        phone = selected_row['Phone']
        email = selected_row['Email']
        license_number = selected_row['License Number']
        agency = selected_row['Agency']
        # Display broker information
        # Display broker information
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Selected Broker's Profile")
            st.write(f"**Name:** {first_name} {last_name}")
            st.write(f"**Phone:** {phone}")
            st.write(f"**Email:** {email}")
            st.write(f"**License Number:** {license_number}")
            st.write(f"**Agency:** {agency}")
        with col2:
            st.image(selected_row['ImageURL'], caption='', use_column_width=True, width=200)

        # Display the image URL, but hide it in the form




else:
    st.write("No brokers match the search criteria.")

df = pd.read_csv('data.csv')

brokerBool = True

try:
    currentBroker = (selected_row['username'])

except:
    st.warning('Please select a broker to see listings and request info form')
    brokerBool = False

if brokerBool:

    show_listings = st.checkbox("Show Broker Listings:")

    df_filtered = df[
        ['house address', 'house type', 'number of rooms', 'number of bathrooms', 'image', 'username', 'status',
         'location']]
    gd = GridOptionsBuilder.from_dataframe(df_filtered)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    gd.configure_column('image', hide=True)
    gridoptions = gd.build()

    if show_listings:

        st.write("### List of Properties")

        if df_filtered[df_filtered['username'] == currentBroker].shape[0] == 0:
            st.info('This broker does not have any listings, stay tuned!')

        try:
            grid_table = AgGrid(df_filtered[df_filtered['username'] == currentBroker],
                                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, height=250,
                                gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

        except:
            pass

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

    # Checkbox to toggle form visibility
    show_form = st.checkbox("Show Request Broker Info Form:")

    # Display form when checkbox is checked
    if show_form:
        st.write("### Request Broker Info: ")
        # Create input fields for the form
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        pnumber = st.text_input("Phone Number")
        email = st.text_input("Email")
        message = st.text_input(label="", value="",
                                placeholder="Enter additional comments for the broker (Optional)")

        # Create a submit button to save and concatenate data
        if st.button("Submit"):
            data = {
                "broker_username": [currentBroker],
                "buyer_username": [logged_in_user],
                "First Name": [fname],
                "Last Name": [lname],
                "Phone Number": [pnumber],
                "Email": [email],
                "Message": [message],
            }
            save_to_csv(data, "broker_requests.csv")
            st.success("You Request Has Filed")