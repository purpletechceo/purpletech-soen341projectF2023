import streamlit as st
import pandas as pd
import os

# Load user data from CSV
user_data = pd.read_csv("userdata.csv")

# CSV file to store the current logged-in user
current_user_file = "current_user.csv"

# Main application
st.title("Simple Login Application")

# Username and password input fields
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button



if st.button("Login"):
    user = user_data[(user_data['username'] == username) & (user_data['password'] == password)]
    if not user.empty:
        st.success(f"Welcome, {username}!")

        # Save current logged-in user to CSV
        current_user_df = pd.DataFrame({"current logged in user": [username], 'pass': [password]})
        current_user_df.to_csv(current_user_file, index=False)

        # Display sign-out button
        sign_out_button = st.button("Sign Out")
        if sign_out_button:
            current_user_df = pd.DataFrame({"current logged in user": [""]})
            current_user_df.to_csv(current_user_file, index=False)
            st.text("User signed out.")
    else:
        st.error("Invalid username or password. Please try again.")
