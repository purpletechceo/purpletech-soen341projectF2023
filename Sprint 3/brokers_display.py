import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

# Load data from 'info.csv' file
df = pd.read_csv('info.csv')

# Create a copy of the DataFrame with the selected columns
df_filtered = df[['FirstName', 'LastName', 'Phone', 'Email', 'License Number', 'Agency', 'ImageURL']]

gd = GridOptionsBuilder.from_dataframe(df_filtered)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('ImageURL', hide=True)
gridoptions = gd.build()

# Keyword search field
search_keyword = st.text_input('## Search for Brokers', '')

# Filter the DataFrame based on the search keyword
filtered_df = df_filtered[df_filtered.apply(lambda row: any(search_keyword.lower() in str(cell).lower() for cell in row), axis=1 )]

# Display the filtered data
st.write("## List of Brokers")

if len(filtered_df) > 0:
    grid_table = AgGrid(filtered_df, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, height=250,
                        gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED)
    if grid_table['selected_rows']:
        selected_row = grid_table['selected_rows'][0]
        first_name = selected_row['FirstName']
        last_name = selected_row['LastName']
        phone = selected_row['Phone']
        email = selected_row['Email']
        license_number = selected_row['License Number']
        agency = selected_row['Agency']
        image_url = selected_row['ImageURL']

        st.markdown("<br><br>", unsafe_allow_html=True)


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
            # Display the image
            st.image(image_url, caption='', use_column_width=True, width=200)

    else:
            st.write("No brokers match the search criteria.")

    # boiler plate code:

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

