
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

#save to csv:

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
            if selected_row['status'] == 'Approved' or 'Pending':
                st.write(f"House Address: {selected_row['house address']}\n"
                         f"\nHouse Type: {selected_row['house type']}\n"
                         f"\nNumber of Rooms: {selected_row['number of rooms']}\n"
                         f"\nNumber of Bathrooms: {selected_row['number of bathrooms']}")
            else:
                st.write(f"House Address: {selected_row['house address']}\n"
                         f"\nHouse Type: {selected_row['house type']}\n"
                         f"\nNumber of Rooms: {selected_row['number of rooms']}\n"
                         f"\nNumber of Bathrooms: {selected_row['number of bathrooms']}\n"
                         f"\nThis property has been {selected_row['status']}")


else:
    st.info("You have not created any listings")

# Offer Management (Sprint 4)

dfp = pd.read_csv('purchaseinfomain.csv')

# Create a copy of the DataFrame with the selected columns
p_df_filtered = dfp[
    ['Broker Name', 'License Number', 'Agency Name', 'Buyer Name', 'Buyer Current Address', 'Buyer Email',
     'Immovable Address', 'Price Offered', 'Deed of Sale Date', 'Occupancy Date', 'username', 'Offer Status']]

gd = GridOptionsBuilder.from_dataframe(p_df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gridoptions = gd.build()

p_df_filtered_display = p_df_filtered[p_df_filtered['Broker Name'] == logged_in_user]

vistRequests = st.checkbox("Show Requests on your Properties")
if vistRequests:
    grid_table = AgGrid(p_df_filtered_display, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                        height=250,
                        gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

    if grid_table['selected_rows']:
        p_selected_row = grid_table['selected_rows'][0]

        if p_selected_row['Offer Status'] == 'Pending':

            if st.button("Accept Offer"):
                row_num = df[df['house address'] == p_selected_row['Immovable Address']].index[0]
                df.at[row_num, 'status'] = f"Sold to {p_selected_row['Broker Name']}"
                p_row_num = dfp[dfp['Immovable Address'] == p_selected_row['Immovable Address']].index[0]
                dfp.at[p_row_num, 'Offer Status'] = "Accepted"
                df.to_csv('data.csv', index=False)
                dfp.to_csv('purchaseinfomain.csv', index=False)
                st.success("Property Sold!")

            if st.button("Reject Offer"):
                p_row_num = dfp[dfp['Immovable Address'] == p_selected_row['Immovable Address']].index[0]
                dfp.at[p_row_num, 'Offer Status'] = "Rejected"
                dfp.to_csv('purchaseinfomain.csv', index=False)
                st.success("Purchase Request Rejected")

# CRUD operations

st.write("### CRUD Operations")

# CREATE
st.write("#### Create")
new_house_address = st.text_input("House Address")
new_house_type = st.text_input("House Type")
new_num_rooms = st.text_input("Number of Rooms")
new_num_bathrooms = st.text_input("Number of Bathrooms")
new_image = st.text_input("Image URL")
new_location = st.text_input("Location")
new_sqf = st.text_input("Square Feet")
new_price = st.text_input("Price")
if st.button("Add New Row"):
    # Store the logged-in username in the 'username' column
    new_row = pd.DataFrame([{
        'house address': new_house_address,
        'house type': new_house_type,
        'number of rooms': new_num_rooms,
        'number of bathrooms': new_num_bathrooms,
        'image': new_image,
        'username': logged_in_user,
        'status': 'Pending',
        'location': new_location,
        'price': new_price,
        'location': new_location
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
    update_location = st.text_input("location", value=df.at[row_to_update, 'location'])
    update_price= st.text_input("price", value=df.at[row_to_update, 'price'])
    update_squareFeet = st.text_input("square feet", value=df.at[row_to_update, 'square feet'])
    if st.button("Update Row"):
        df.at[row_to_update, 'house address'] = update_house_address
        df.at[row_to_update, 'house type'] = update_house_type
        df.at[row_to_update, 'number of rooms'] = update_num_rooms
        df.at[row_to_update, 'number of bathrooms'] = update_num_bathrooms
        df.at[row_to_update, 'image'] = update_image
        df.at[row_to_update, 'status'] = 'Pending'
        df.at[row_to_update, 'location'] = update_location
        df.at[row_to_update, 'price'] = update_price
        df.at[row_to_update, 'square feet'] = update_squareFeet



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


