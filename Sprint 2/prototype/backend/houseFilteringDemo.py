import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

image1 = 'https://www.forbes.com/advisor/wp-content/uploads/2022/10/what-is-a-townhouse.jpeg.jpg'
image2 = 'https://simpleshowing.ghost.io/content/images/2023/01/GetMedia-1.jpeg'

data = {
    'house address': ['House 1', 'House 2'],
    'house type': ['Townhouse', 'Split Level'],
    'number of rooms': ['6', '7'],
    'number of bathrooms': ['2', '3'],
    'image': [image1, image2],
    'broker_email': ['johnterry@gmail.com', 'terrencewallace@hotmail.com']
}

df = pd.DataFrame(data)

# Create a copy of the DataFrame without the 'email' column
df_filtered = df[['house address', 'house type', 'number of rooms', 'number of bathrooms', 'image', 'broker_email']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('image', hide=True)
gridoptions = gd.build()

# Initialize the visit request DataFrame
visit_request_df = pd.DataFrame(columns=["b_email", "property", "fname", "lname", "pnumber", "email", "date_time"])

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

# Boiler plate code:
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
