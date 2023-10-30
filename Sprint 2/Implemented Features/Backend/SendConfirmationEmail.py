import streamlit as st
import smtplib
from email.mime.text import MIMEText

# Taking inputs
email_sender = "fill in with broker's email"  # we won't actually be able to do this, so we might use the ceo email
email_receiver = "user's email"  # we probably won't be able to do this too, but we can test with our own emails
subject = "subject to change lol"
body = "we don't body shame here kek"
password = "password of broker's email"

try:
    msg = MIMEText(body)
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = subject

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_sender, password)
    server.sendmail(email_sender, email_receiver, msg.as_string())
    server.quit()

    st.success('Email sent successfully! 🚀')
except Exception as e:
    st.error(f"Error trying to send the email: {e}")
