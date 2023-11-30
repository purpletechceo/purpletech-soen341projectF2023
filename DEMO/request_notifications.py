
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

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

st.write("## Info Requests:")

requests_df = pd.read_csv('broker_requests.csv')
ir_df = requests_df[requests_df['broker_username'] == logged_in_user]

if ir_df.shape[0] == 0:
    st.info('No Information Requests')
else:
    st.dataframe(ir_df.T[:7].T)

st.write("## Purchase Requests:")

purchaseinfo = pd.read_csv('purchaseinfomain.csv')
purchaseinfo_filtered = purchaseinfo[purchaseinfo['Broker Name'] == logged_in_user]

if purchaseinfo_filtered.shape[0] == 0:
    st.info('No Promises to Purchase Made')

else:

    st.dataframe(purchaseinfo_filtered)