import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Function to calculate the monthly mortgage payment
def calculate_mortgage(principal, annual_interest_rate, num_years):
    if principal <= 0:
        raise ValueError("Principal amount must be greater than zero")
    if num_years <= 0:
        raise ValueError("Loan term must be a positive number of years")
    if annual_interest_rate <= 0:
        raise ValueError("Annual interest rate must be greater than zero")

    if annual_interest_rate == 0:
        return principal / (num_years * 12)

    # Monthly interest rate
    monthly_interest_rate = annual_interest_rate / 12 / 100

    # Number of monthly payments
    num_payments = num_years * 12

    # Monthly payment calculation using the provided formula
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments) / (
                ((1 + monthly_interest_rate) ** num_payments) - 1)

    return monthly_payment

# Define loan options with corresponding interest rates
loan_options = {
    "User Selection": {"interest_rate": 0},
    "30-year Fixed": {"interest_rate": 7.83},
    "30-year Fixed VA": {"interest_rate": 7.09},
    "30-year Fixed FHA": {"interest_rate": 6.81},
    "20-year Fixed": {"interest_rate": 7.76},
    "15-year Fixed": {"interest_rate": 7.12},
    "10-year Fixed": {"interest_rate": 7.13},
    "5/1 ARM": {"interest_rate": 6.97},
}

st.title("Mortgage Calculator")
st.caption("Please ensure that all input fields are filled properly before calculating.")

# Input fields
home_price = st.number_input("Enter the home price: $", format="%.2f")

down_payment_option = st.selectbox("Select a down payment percentage:", ["20%", "25%", "30%", "35%", "40%", "I want to enter another amount"])
st.caption("Note: the down payment is based on given percentages of the total home price.")
custom_down_payment = 0

if down_payment_option == "I want to enter another amount":
    custom_down_payment = st.number_input("Enter down payment: $", format="%.2f")
else:
    down_payment_percentage = float(down_payment_option.strip('%')) / 100
    custom_down_payment = home_price * down_payment_percentage

loan_term_years = st.number_input("Enter the loan term in years:", min_value=1, step=1, value=30)

annual_interest_rate = st.number_input("Enter the annual interest rate (%):", min_value=0.01, format="%.2f", value=loan_options["30-year Fixed"]["interest_rate"], help="Please enter a non-zero interest rate")

# Update user selection with custom input
loan_options["User Selection"]["interest_rate"] = annual_interest_rate

# Always show the Calculate button
if st.button("Calculate"):
    if home_price > 0:
        # Calculate the principal loan amount
        principal = home_price - custom_down_payment

        # Calculate the monthly mortgage payment
        num_years = loan_term_years
        monthly_payment = calculate_mortgage(principal, annual_interest_rate, num_years)
        st.success(f"Your total monthly mortgage payment over {num_years} years will be: ${monthly_payment:.2f}")

        # Calculate payment scenarios
        months = num_years * 12
        weekly_payment = monthly_payment * 12 / 52
        accelerated_weekly_payment = monthly_payment / 4
        bi_weekly_payment = monthly_payment / 2
        monthly_payment = monthly_payment
        quarterly_payment = monthly_payment * 3
        annual_payment = monthly_payment * 12

        # Payment scenarios DataFrame
        payment_scenarios = pd.DataFrame({
            "Payment Type": ["Weekly", "Accelerated Weekly", "Bi-weekly", "Monthly", "Quarterly", "Annually"],
            "Amount": [weekly_payment, accelerated_weekly_payment, bi_weekly_payment, monthly_payment, quarterly_payment, annual_payment],
        })

        # Create a dashboard layout
        st.header("Payment Schedule")
        st.table(payment_scenarios.set_index('Payment Type').style.format({'Amount': '${:.2f}'}))

        # Amortization Schedule
        st.header("Amortization Schedule")
        st.text("Amortization built based on a monthly payment basis.")
        
        # Initialize amortization_data as an empty list
        amortization_data = []
        
        # Initialize interest_paid_list and principal_paid_list
        interest_paid_list = []
        principal_paid_list = []

        # Initialize current_year here
        current_year = 1  
        
        # Initialize balance_list with the initial principal
        balance_list = [principal]
        
        # Calculate monthly_interest_rate before entering the loop
        monthly_interest_rate = annual_interest_rate / 12 / 100  

        for month in range(1, months + 1):
            interest_paid = balance_list[-1] * monthly_interest_rate
            principal_paid = monthly_payment - interest_paid
            new_balance = balance_list[-1] - principal_paid

            interest_paid_list.append(interest_paid)
            principal_paid_list.append(principal_paid)
            balance_list.append(new_balance)

            # Add data to the amortization_data list
            amortization_data.append({
                "Year": current_year,
                "Month": month,
                "Payment": monthly_payment,
                "Principal Paid": principal_paid,
                "Interest Paid": interest_paid,
                "Remaining Balance": new_balance
            })

            if month % 12 == 0:
                current_year += 1  # Update current_year for the next year

        # Create a dictionary to store amortization data for each year
        amortization_years = {}

        # Separate the data for each year
        for year in range(1, num_years + 1):
            year_data = [data for data in amortization_data if data["Year"] == year]
            amortization_years[year] = pd.DataFrame(year_data)

        # Create an expander for each year
        for year in range(1, num_years + 1):
            with st.expander(f"Year {year}"):
                year_data = amortization_years[year]
                st.table(year_data[['Month', 'Payment', 'Principal Paid', 'Interest Paid', 'Remaining Balance']].set_index('Month').style.format({
                    "Payment": "${:.2f}",
                    "Principal Paid": "${:.2f}",
                    "Interest Paid": "${:.2f}",
                    "Remaining Balance": "${:.2f}"
                }))
        
        st.subheader("Summary")
        # Visualize the amortization data with green-themed graphs
        # Scatter plot for Principal Paid vs. Month
        principal_paid = [data['Principal Paid'] for data in amortization_data]
        month = [data['Month'] for data in amortization_data]

        # Histogram for Interest Paid
        interest_paid = [data['Interest Paid'] for data in amortization_data]

        # Horizontal bar chart for Remaining Balance by Year
        remaining_balance = [data['Remaining Balance'] for data in amortization_data]
        year = [data['Year'] for data in amortization_data]

        # Create a plot chart to compare loan options
        loan_terms = list(loan_options.keys())
        monthly_payments = [calculate_mortgage(principal, loan_options[term]["interest_rate"], loan_term_years) for term in loan_terms]

        # Create columns for layout
        col1, col2 = st.columns(2)

        # Column 1: 
        with col1:
            st.subheader("Principal Paid vs. Month")
            plt.figure(figsize=(8, 4))
            plt.scatter(month, principal_paid, color='green', marker='o', linewidths=0.20)
            plt.xlabel('Month')
            plt.ylabel('Principal Paid ($)')
            plt.title('Principal Paid vs. Month')
            st.pyplot(plt)
            
            st.subheader("Principal Paid vs. Year")
            principal_paid_by_year = [sum(principal_paid[i:i+12]) for i in range(0, len(principal_paid), 12)]
            years = list(range(1, num_years + 1))
            plt.figure(figsize=(8, 4))
            plt.bar(years, principal_paid_by_year, color='green')
            plt.xlabel('Year')
            plt.ylabel('Principal Paid ($)')
            plt.title('Principal Paid vs. Year')
            st.pyplot(plt)

        # Column 2: 
        with col2:
            st.subheader("Histogram of Interest Paid")
            plt.figure(figsize=(8, 4))
            plt.hist(interest_paid, bins=10, color='green', alpha=0.7)
            plt.xlabel('Interest Paid ($)')
            plt.ylabel('Frequency')
            plt.title('Histogram of Interest Paid')
            st.pyplot(plt)
            
            st.subheader("Remaining Balance by Year")
            plt.figure(figsize=(8, 4))
            plt.barh(year, remaining_balance, color='green')
            plt.xlabel('Remaining Balance ($)')
            plt.ylabel('Year')
            plt.title('Horizontal Bar Chart of Remaining Balance by Year')
            st.pyplot(plt)
        
        st.subheader("Loan Term Options Comparison")
        st.caption(f"In addition to your selection, Purple Tech offers various plans.") 
        st.caption("The following chart displays how much you would pay monthly accordingly.")
        st.caption(f"Remember that for User Selection, you chose {loan_term_years} years.")
        
        plt.figure(figsize=(8, 4))
        bars = plt.bar(loan_terms, monthly_payments, color=['#EE82EE' if loan_term == 'User Selection' else '#800080' for loan_term in loan_terms])
        plt.xlabel('Loan Type')
        plt.ylabel('Monthly Payment ($)')
        plt.title(f'Loan Term Options Comparison')
        plt.xticks(rotation=45)
            
        for bar, payment in zip(bars, monthly_payments):
            plt.text(bar.get_x() + bar.get_width() / 2 - 0.05, payment + 20, f"${payment:.2f}", ha='center', color='black', fontsize=9)
            
        st.pyplot(plt)

        # Provide guidance on selecting the best option
        best_option = min(loan_options, key=lambda x: calculate_mortgage(principal, loan_options[x]["interest_rate"], loan_term_years))
        st.success(f"To minimize your monthly payment, you may consider the '{best_option}' option, which would result in a lower monthly payment compared to other options.")
            
            