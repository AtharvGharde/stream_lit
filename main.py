import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for storing data
if 'data' not in st.session_state:
    st.session_state['data'] = []

# Input fields for budget categories
st.title("Budget Management App")

st.header("Income")
wages = st.number_input("Wages", min_value=0, value=0)
monthly_wages = st.number_input("Monthly Wages", min_value=0, value=0)

st.header("Expenses")
groceries = st.number_input("Groceries", min_value=0, value=0)
medicine = st.number_input("Medicine", min_value=0, value=0)
entertainment = st.number_input("Entertainment", min_value=0, value=0)
rent = st.number_input("Rent", min_value=0, value=0)
utilities = st.number_input("Utilities", min_value=0, value=0)
loans = st.number_input("Loans", min_value=0, value=0)
emis = st.number_input("EMIs", min_value=0, value=0)
investments = st.number_input("Investments", min_value=0, value=0)
bills = st.number_input("Bills", min_value=0, value=0)

# Calculate totals
total_income = wages + monthly_wages
total_expenses = groceries + medicine + entertainment + rent + utilities + loans + emis + bills
remaining_balance = total_income - total_expenses

# Simple interest calculation for loan
interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=5.0)
interest_lost = loans * (interest_rate / 100)

# Returns on investment (simple estimation)
investment_return_rate = st.number_input("Investment Return Rate (%)", min_value=0.0, value=7.0)
investment_return = investments * (investment_return_rate / 100)

# Store data in session state
st.session_state['data'].append({
    "Wages": wages,
    "Monthly Wages": monthly_wages,
    "Total Income": total_income,
    "Groceries": groceries,
    "Medicine": medicine,
    "Entertainment": entertainment,
    "Rent": rent,
    "Utilities": utilities,
    "Loans": loans,
    "EMIs": emis,
    "Bills": bills,
    "Total Expenses": total_expenses,
    "Remaining Balance": remaining_balance,
    "Interest Lost": interest_lost,
    "Investment Return": investment_return
})

# Display results
st.subheader("Summary")
st.write(f"**Total Income:** ${total_income}")
st.write(f"**Total Expenses:** ${total_expenses}")
st.write(f"**Remaining Balance:** ${remaining_balance}")
st.write(f"**Interest Lost on Loans:** ${interest_lost}")
st.write(f"**Returns on Investment:** ${investment_return}")

# Visualization
st.subheader("Visualization")
if st.button("Generate Charts"):
    df = pd.DataFrame(st.session_state['data'])

    # Pie chart for expenses
    st.write("**Expenses Distribution**")
    fig1, ax1 = plt.subplots()
    ax1.pie([groceries, medicine, entertainment, rent, utilities, loans, emis, bills], 
            labels=["Groceries", "Medicine", "Entertainment", "Rent", "Utilities", "Loans", "EMIs", "Bills"],
            autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)

    # Bar chart for income vs expenses
    st.write("**Income vs Expenses**")
    fig2, ax2 = plt.subplots()
    ax2.bar(["Total Income", "Total Expenses", "Remaining Balance"], 
            [total_income, total_expenses, remaining_balance], color=['green', 'red', 'blue'])
    st.pyplot(fig2)

# Machine Learning - Placeholder for future implementation
st.subheader("Future Enhancement: Machine Learning")
st.write("Machine learning algorithms will be implemented to provide personalized investment and budgeting advice based on your data.")
