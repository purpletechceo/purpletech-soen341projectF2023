import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
import pandas as pd

# Dummy data for visit requests
data = {
    "b_email": ["broker1@example.com", "broker2@example.com", "broker1@example.com", "broker3@example.com", "broker4@example.com"],
    "property": ["House A", "House B", "House C", "House D", "House E"],
    "fname": ["John", "Alice", "Michael", "Ella", "Test"],
    "lname": ["Doe", "Smith", "Johnson", "Wilson", "Broker"],
    "pnumber": ["123-456-7890", "987-654-3210", "555-555-5555", "111-222-3333", "999-888-7777"],
    "email": ["john@example.com", "alice@example.com", "michael@example.com", "ella@example.com", "test@example.com"],
    "date_time": ["2023-10-25 10:00:00", "2023-10-26 14:30:00", "2023-10-27 11:15:00", "2023-10-28 15:45:00", "2023-10-29 09:30:00"],
}

df = pd.DataFrame(data)

# Create a copy of the DataFrame without the 'brokers_email' column
df_filtered = df[['property', 'fname', 'lname', 'pnumber', 'email', 'date_time']]

# Dropdown filter for broker email
selected_broker_email = st.selectbox('Filter by Broker Email', ['All'] + list(df['b_email'].unique()))

# Filter the DataFrame based on selected broker email
if selected_broker_email != 'All':
    filtered_df = df_filtered[df['b_email'] == selected_broker_email]
else:
    filtered_df = df_filtered

# Display the ag-Grid with visit requests
st.write("## Visit Requests")

gd = GridOptionsBuilder.from_dataframe(filtered_df)
gd.configure_selection(selection_mode='single', use_checkbox=True)

gridoptions = gd.build()

grid_table = AgGrid(filtered_df, height=250, gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)

if grid_table['selected_rows']:
    selected_row = grid_table['selected_rows'][0]
    st.write(f"Selected Property: {selected_row['property']}")
    st.write(f"Broker Email: {selected_row['b_email']}")

# Boiler plate code:
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
