import streamlit as st

# Function to calculate the monthly mortgage payment
def calculate_mortgage(principal, interest_rate, num_payments):
    # Monthly interest rate
    monthly_interest_rate = interest_rate / 12 / 100
    
    # Monthly payment calculation
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / ((1 + monthly_interest_rate) ** num_payments - 1)
    
    return monthly_payment

st.title("Mortgage Calculator")

principal = st.number_input("Enter the loan amount (principal): $", min_value=0.00, format="%.2f")
interest_rate = st.number_input("Enter the annual interest rate (%): ", min_value=0.00, format="%.2f")
num_years = st.number_input("Enter the number of years for the loan: ", min_value=1, step=1, format="%.2d")

# Calculate the number of monthly payments
num_payments = num_years * 12

if st.button("Calculate"):
    # Calculate the monthly mortgage payment
    monthly_payment = calculate_mortgage(principal, interest_rate, num_payments)
    st.success(f"Your monthly mortgage payment will be: ${monthly_payment:.2f}")

st.text("")