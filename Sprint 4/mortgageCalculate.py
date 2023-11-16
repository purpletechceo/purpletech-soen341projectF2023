import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the monthly mortgage payment
def calculate_mortgage(principal, annual_interest_rate, num_years):
    # Monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12 / 100
    
    # Number of monthly payments
    num_payments = num_years * 12
    
    # Monthly payment calculation using the provided formula
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / (((1 + monthly_interest_rate) ** num_payments) - 1)
    
    return monthly_payment

# Define loan options with corresponding interest rates and loan terms
loan_options = {
    "30-year Fixed": {"interest_rate": 7.83, "loan_term": 30},
    "30-year Fixed VA": {"interest_rate": 7.09, "loan_term": 30},
    "30-year Fixed FHA": {"interest_rate": 6.81, "loan_term": 30},
    "30-year Fixed Jumbo": {"interest_rate": 7.83, "loan_term": 30},
    "20-year Fixed": {"interest_rate": 7.76, "loan_term": 20},
    "15-year Fixed": {"interest_rate": 7.12, "loan_term": 15},
    "10-year Fixed": {"interest_rate": 7.13, "loan_term": 10},
    "5/1 ARM": {"interest_rate": 6.97, "loan_term": 5}
}

st.title("Mortgage Calculator")
st.caption("Please ensure that all input fields are filled properly before calculating.")

# Input fields
home_price = st.number_input("Enter the home price: $", format="%.2f")
down_payment = st.number_input("Enter the down payment: $", format="%.2f")
selected_option = st.selectbox("Select a loan type:", list(loan_options.keys()))
loan_data = loan_options[selected_option]
annual_interest_rate = st.number_input("Enter the annual interest rate (%):", min_value=0.01, format="%.2f", value=loan_data["interest_rate"], help="Please enter a non-zero interest rate")

# Always show the Calculate button
if st.button("Calculate"):
    invalid_fields = []
    
    # Check if all required input fields are filled properly
    if home_price <= 0.0:
        invalid_fields.append("Home Price")
    if down_payment <= 0.0:
        invalid_fields.append("Down Payment")
    if annual_interest_rate <= 0.0:
        invalid_fields.append("Annual Interest Rate")
    
    if len(invalid_fields) > 0:
        st.warning(f"You need to fill out the following field(s) with values greater than 0 before proceeding: {', '.join(invalid_fields)}")
    else:
        # Calculate the principal loan amount
        principal = home_price - down_payment
        
        # Calculate the monthly mortgage payment
        num_years = loan_data["loan_term"]
        monthly_payment = calculate_mortgage(principal, annual_interest_rate, num_years)
        st.success(f"Your total monthly mortgage payment over {num_years} years will be: ${monthly_payment:.2f}")     
        
        # Create a plot chart to compare loan options
        st.header("Scenario Analyzer: Loan Type Comparisons")
        st.caption("The following chart displays how much you would pay monthly, according to the different loan type (years) and their respective annual interest rates.")
        
        loan_terms = list(loan_options.keys())
        monthly_payments = [calculate_mortgage(principal, loan_options[term]["interest_rate"], loan_options[term]["loan_term"]) for term in loan_terms]

        plt.figure(figsize=(10, 6))
        bars = plt.bar(loan_terms, monthly_payments, color='purple')
        plt.xlabel('Loan Type')
        plt.ylabel('Monthly Payment ($)')
        plt.title('Loan Options Comparison')
        plt.xticks(rotation=45)

        # Display actual monthly payment values centered on top of each bar
        for bar, payment in zip(bars, monthly_payments):
            plt.text(bar.get_x() + bar.get_width() / 2 - 0.05, payment + 20, f"${payment:.2f}", ha='center', color='black', fontsize=9)

        st.pyplot(plt)
        
        # Provide guidance on selecting the best option    
        best_option = min(loan_options, key=lambda x: calculate_mortgage(principal, loan_options[x]["interest_rate"], loan_options[x]["loan_term"]))
        st.success(f"To minimize your monthly payment, you may consider the '{best_option}' option, which would result in a lower monthly payment compared to other options.")