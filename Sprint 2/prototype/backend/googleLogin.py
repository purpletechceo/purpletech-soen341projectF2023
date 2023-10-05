import streamlit as st
import requests
import webbrowser

# Google OAuth configuration
CLIENT_ID = "30633705814-mjshvsq8g040ep704qrs0hl3uaam7a6d.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501"

# Streamlit app
st.title("Google Login App")

# Check if the user is logged in
if 'access_token' not in st.session_state:
    st.session_state.access_token = None

# Redirect user to Google for authentication
google_auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=email profile"
google_button = st.button("Login with Google")
if google_button:
    webbrowser.open(google_auth_url)

# Sign-out button
sign_out_button = st.button("Sign Out")

# Handle sign-out
if sign_out_button:
    st.session_state.access_token = None
    st.write("You have been signed out.")

# Get the authorization code from the URL query parameters after the redirect
query_params = st.experimental_get_query_params()
auth_code = query_params.get("code")

if auth_code:
    # Exchange authorization code for access token and fetch user data
    token_url = "https://oauth2.googleapis.com/token"
    token_params = {
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=token_params)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        st.session_state.access_token = access_token  # Store access token in session state
        # Fetch user data from Google API
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code == 200:
            user_data = user_info_response.json()
            user_email = user_data.get("email")
            st.write(f"Hello {user_email}")
        else:
            st.write("Error: Unable to fetch user data from Google.")
    else:
        st.write("Click the link above to log in with Google.")
elif st.session_state.access_token:
    # If the user is already logged in, display their email
    st.write(f"Hello {st.session_state.access_token}")
else:
    st.write("Please sign in.")