
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



# Dropdown filter for house type
selected_house = st.selectbox('Select Property Type', ['All'] + list(df_filtered['house type'].unique()))
selected_location = st.selectbox('Select House Location', ['All'] + list(df_filtered['location'].unique()))
selected_rooms = st.slider('Select Number of Rooms', min_value=min(df_filtered['number of rooms']),
                           max_value=max(df_filtered['number of rooms']),
                           value=(min(df_filtered['number of rooms']), max(df_filtered['number of rooms'])))

# Filter the DataFrame based on user selections
if selected_house != 'All' and selected_location != 'All':
    filtered_df = df_filtered[
        (df_filtered['house type'] == selected_house) & (df_filtered['location'] == selected_location) & (
            df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1]))]
elif selected_house != 'All':
    filtered_df = df_filtered[(df_filtered['house type'] == selected_house) & (
        df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1]))]
elif selected_location != 'All':
    filtered_df = df_filtered[(df_filtered['location'] == selected_location) & (
        df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1]))]
else:
    filtered_df = df_filtered[df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1])]

df_filtered_display = filtered_df[filtered_df['status'] == 'Approved']
df_filtered_display = df_filtered_display [df_filtered_display ['username'] != logged_in_user]

# Display the filtered data
st.write("## List of Properties")

grid_table = AgGrid(df_filtered_display, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, height=250,
                    gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

if not grid_table['selected_rows']:
    st.info('Select a property to view more info and make requests')


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

    requestVisit = st.checkbox("Open Request Visit Form")
    if ('broker' in logged_in_user):
        promiseToPurchase = st.checkbox("Open Promise Purchase form")
    else:
        promiseToPurchase = False

    if requestVisit:
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



    if (promiseToPurchase):

        broker_name = st.text_input("Full Name", key="broker_name")
        license_no = st.text_input("License Number", key="license_no")
        agency_name = st.text_input("Agency Name", key="agency_name")
        buyer_name = st.text_input("Buyer's Name", key="buyer_name")
        buyer_address = st.text_input("Buyer's Current Address", key="buyer_address")
        buyer_email = st.text_input("Buyer's Email", key="buyer_email")
        # Autofilling house address
        immovable_address = st.text_input("Address of the Property to Buy", key="immovable_address",
                                          value=selected_row['house address'])
        offer_price = st.text_input("Price to Offer", key="offer_price", value="$")
        deed_date = st.date_input("Deed of Sale Date", key="deed_date")
        occupancy_date = st.date_input("Occupancy of Premises Date", key="occupancy_date")

        # Create a submit button to save and concatenate data
        if st.button("Submit"):
            if broker_name and license_no and agency_name and buyer_name and buyer_address and buyer_address and immovable_address and offer_price and deed_date and occupancy_date:
                purchase_data = pd.DataFrame({
                    'Broker Name': [broker_name],
                    'License Number': [license_no],
                    'Agency Name': [agency_name],
                    'Buyer Name': [buyer_name],
                    'Buyer Current Address': [buyer_address],
                    'Buyer Email': [buyer_email],
                    'Immovable Address': [immovable_address],
                    'Price Offered': [offer_price],
                    'Deed of Sale Date': [deed_date],
                    'Occupancy Date': [occupancy_date],
                    'username':[logged_in_user]
                })

            save_to_csv(purchase_data, "purchaseinfomain.csv")
            st.success("Data saved and concatenated to purchaseinfomain.csv")



    # Display user's own visit requests
vistRequests = st.checkbox("Show Your Requests")

if vistRequests:
    st.write("## Your Requests")
    visits_data = pd.read_csv('visits.csv')
    user_visits = visits_data[visits_data['b_email'] == username]
    purchase_requests= pd.read_csv('purchaseinfomain.csv')
    purchase_requests = purchase_requests[purchase_requests['username'] == logged_in_user]

    st.write("#### Visit Requests:")
    if user_visits.shape[0] == 0:
        st.info('You have made no requests to visit a property, select a property and fill in the form')

    else:
        st.dataframe(user_visits)

    if('broker' in logged_in_user):
        st.write("#### Purchase Requests:")
    if purchase_requests.shape[0] == 0:
        if ('broker' in logged_in_user):
            st.info('You have made no promises to purchase, select a property and fill in the form')
        else:
            pass

    else:
        st.dataframe(purchase_requests)