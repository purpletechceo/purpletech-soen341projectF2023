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

tab1, tab2, tab3= st.tabs(['Property Search', 'Morgage Calculator', 'Compare Your Listing'])

with tab1:


    # Create a copy of the DataFrame without the 'email' column
    df_filtered = df[['house address', 'house type', 'location', 'number of rooms','square feet','price', 'number of bathrooms', 'image','username', 'status']]

    gd = GridOptionsBuilder.from_dataframe(df_filtered)
    gd.configure_selection(selection_mode='single', use_checkbox=True)
    gd.configure_column('image', hide=True)
    gd.configure_column('number of bathrooms', hide=True)
    gd.configure_column('status', hide=True)
    gd.configure_column('username', hide=True)
    gd.configure_column('square feet', hide=True)

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
    selected_house = st.sidebar.selectbox('Select Property Type', ['All'] + list(df_filtered['house type'].unique()))
    selected_location = st.sidebar.selectbox('Select House Location', ['All'] + list(df_filtered['location'].unique()))

    selected_rooms = st.sidebar.slider('Select Number of Rooms', min_value=min(df_filtered['number of rooms']),
                                       max_value=max(df_filtered['number of rooms']),
                                       value=(min(df_filtered['number of rooms']), max(df_filtered['number of rooms'])))

    selected_square_feet = st.sidebar.slider('Select Square Feet Range', min_value=min(df_filtered['square feet']),
                                             max_value=max(df_filtered['square feet']),
                                             value=(min(df_filtered['square feet']), max(df_filtered['square feet'])))

    # Add a price range slider
    selected_price_range = st.sidebar.slider('Select Price Range', min_value=min(df_filtered['price']),
                                             max_value=max(df_filtered['price']),
                                             value=(min(df_filtered['price']), max(df_filtered['price'])))

    # Dropdown filter for number of bathrooms
    selected_bathrooms = st.sidebar.slider('Select Number of Bathrooms',
                                           min_value=min(df_filtered['number of bathrooms']),
                                           max_value=max(df_filtered['number of bathrooms']),
                                           value=(min(df_filtered['number of bathrooms']),
                                                  max(df_filtered['number of bathrooms'])))

    # Filter the DataFrame based on user selections
    if selected_house != 'All' and selected_location != 'All':
        filtered_df = df_filtered[
            (df_filtered['house type'] == selected_house) & (df_filtered['location'] == selected_location) & (
                df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1])) &
            (df_filtered['square feet'].between(selected_square_feet[0], selected_square_feet[1])) &
            (df_filtered['price'].between(selected_price_range[0], selected_price_range[1]))
            ]
    elif selected_house != 'All':
        filtered_df = df_filtered[(df_filtered['house type'] == selected_house) & (
            df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1])) &
                                  (df_filtered['square feet'].between(selected_square_feet[0],
                                                                      selected_square_feet[1])) &
                                  (df_filtered['price'].between(selected_price_range[0], selected_price_range[1]))
                                  ]
    elif selected_location != 'All':
        filtered_df = df_filtered[(df_filtered['location'] == selected_location) & (
            df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1])) &
                                  (df_filtered['square feet'].between(selected_square_feet[0],
                                                                      selected_square_feet[1])) &
                                  (df_filtered['price'].between(selected_price_range[0], selected_price_range[1]))
                                  ]
    else:
        filtered_df = df_filtered[df_filtered['number of rooms'].between(selected_rooms[0], selected_rooms[1]) &
                                  (df_filtered['square feet'].between(selected_square_feet[0],
                                                                      selected_square_feet[1])) &
                                  (df_filtered['price'].between(selected_price_range[0], selected_price_range[1]))]

    df_filtered_display = filtered_df[filtered_df['status'] == 'Approved']
    df_filtered_display = df_filtered_display[df_filtered_display['username'] != logged_in_user]

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
                     f"\nNumber of Bathrooms: {selected_row['number of bathrooms']}\n"
                     f"\nSquare Feet: {selected_row['square feet']}\n"
                     f"\nBroker Name: {selected_row['username']}"
                     )

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

with tab2:
    import streamlit as st


    # Function to calculate the monthly mortgage payment
    def calculate_mortgage(principal, interest_rate, num_payments):
        # Monthly interest rate
        monthly_interest_rate = interest_rate / 12 / 100

        # Monthly payment calculation
        monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / (
                    (1 + monthly_interest_rate) ** num_payments - 1)

        return monthly_payment


    st.title("Mortgage Calculator")

    try:
        principal = st.number_input("Enter the loan amount (principal): $", min_value=float(selected_row['price']), format="%.2f")
    except:
        principal = st.number_input("Enter the loan amount (principal): $", min_value=0.00,
                                    format="%.2f")
    interest_rate = st.number_input("Enter the annual interest rate (%): ", min_value=0.01, format="%.2f")
    num_years = st.number_input("Enter the number of years for the loan: ", min_value=1, step=1, format="%.2d")

    # Calculate the number of monthly payments
    num_payments = num_years * 12

    if st.button("Calculate"):
        # Calculate the monthly mortgage payment
        monthly_payment = calculate_mortgage(principal, interest_rate, num_payments)
        st.success(f"Your monthly mortgage payment will be: ${monthly_payment:.2f}")


with tab3:
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
    df = pd.read_csv('data.csv')


    # Function to compare properties
    def compare_properties(selected_props):
        return df[df['house address'].isin(selected_props)]


    st.title("Property Comparator")

    # Select properties for comparison
    try:
        selected_properties = st.multiselect("Select Properties for Comparison", df['house address'], default=selected_row['house address'])
    except:
        selected_properties = st.multiselect("Select Properties for Comparison", df['house address'])
    # Display details for selected properties
    if selected_properties:
        compared_properties = compare_properties(selected_properties)

        # Create a new column with HTML image tags
        compared_properties['Image'] = compared_properties['image'].apply(
            lambda x: f'<img src="{x}" style="max-width:100px;">' if x else '')

        # Drop 'Image' and 'Image HTML' columns before displaying the table
        compared_properties = compared_properties.drop(['image'], axis=1)

        # Plotting features
        st.subheader("Comparison Details")

        # Display transposed table with images
        st.write(compared_properties.set_index('house address').T.to_html(escape=False), unsafe_allow_html=True)
    else:
        st.warning("Please select properties for comparison.")
