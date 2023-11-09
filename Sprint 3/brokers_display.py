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
search_keyword = st.text_input('Keyword Search', '')

# Filter the DataFrame based on the search keyword
filtered_df = df_filtered[df_filtered.apply(lambda row: any(search_keyword.lower() in str(cell).lower() for cell in row), axis=1 )]

