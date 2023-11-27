import streamlit as st
import pandas as pd

def login_function(username, password):
    user_data = pd.read_csv("userdata.csv")
    current_user_file = "current_user.csv"

    user = user_data[(user_data['username'] == username) & (user_data['password'] == password)]
    
    if not user.empty:
        # Save current logged-in user to CSV
        current_user_df = pd.DataFrame({"current logged in user": [username], 'pass': [password]})
        current_user_df.to_csv(current_user_file, index=False)
        
        return f"Welcome, {username}!"
    else:
        return "Invalid username or password. Please try again."

if __name__ == "__main__":
    # Main application
    st.title("Login")

    # Username and password input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        result = login_function(username, password)
        if result.startswith("Welcome"):
            st.success(result)
        else:
            st.error(result)