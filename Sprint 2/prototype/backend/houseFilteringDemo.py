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
    'image': [image1, image2]
}

df = pd.DataFrame(data)
gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_selection(selection_mode='single', use_checkbox=True)
gd.configure_column('image', hide=True)
gridoptions = gd.build()

# Dropdown filter for house type
selected_house = st.selectbox('Select Housetype', ['All'] + list(df['house type'].unique()))

if selected_house != 'All':
    filtered_df = df[df['house type'] == selected_house]
else:
    filtered_df = df

grid_table = AgGrid(filtered_df, height=250, gridOptions=gridoptions,
                update_mode=GridUpdateMode.SELECTION_CHANGED)

st.write('## Selected')

if grid_table['selected_rows']:
    selected_row = grid_table['selected_rows'][0]
    image_column, description_column = st.columns(2)

    with image_column:
        st.image(selected_row['image'], caption='Selected Image', use_column_width=True)

    with description_column:
        st.write(f"Number of Rooms: {selected_row['number of rooms']}\n\r"
                 f"Number of Bathrooms: {selected_row['number of bathrooms']}")
else:
    st.write('No row selected.')


# boiler plate code:

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)