import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Try to import scikit-learn and handle potential import errors
try:
    from sklearn.linear_model import LinearRegression
except ModuleNotFoundError:
    st.error("Error: scikit-learn is not installed. Please install it using `pip install scikit-learn`.")
    st.stop()

# Initialize session state
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = {
        'income': 0,
        'expenses': {},
        'investment': 0,
        'remaining_balance': 0,
        'data': []
    }

# Hardcoded login credentials
def login(username, password):
    if username == "developer" and password == "password123":
        st.session_state.user_logged_in = True
        return True
    return False

# Machine Learning Model
def train_model(data):
    if len(data) > 0:
        df = pd.DataFrame(data)
        X = df[['income', 'expenses', 'investment']]
        y = df['savings']
        model = LinearRegression().fit(X, y)
        return model
    return None

def predict_savings(model, income, expenses, investment):
    if model:
        return model.predict([[income, expenses, investment]])[0]
    return 0

# Sidebar for Navigation
st.sidebar.title("Navigation")
pages = ["Home", "Budget Calculator", "Investment Suggestions", "Expense History", "Alerts"]
choice = st.sidebar.radio("Go to", pages)

# Home Page
if choice == "Home":
    st.title("Welcome to AI Budget App")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log in"):
        if login(username, password):
            st.success("You are now logged in!")
        else:
            st.error("Incorrect username or password.")

# Budget Calculator
elif choice == "Budget Calculator" and st.session_state.user_logged_in:
    st.title("Budget Calculator")

    income = st.number_input("Enter your monthly income:", min_value=0)
    categories = ["Groceries", "Medicine", "Entertainment", "Rent", "Utilities", "Loans", "EMIs", "Investments", "Bills"]

    expenses = {}
    for category in categories:
        expenses[category] = st.number_input(f"{category}:", min_value=0)

    if st.button("Calculate Budget"):
        total_expenses = sum(expenses.values())
        remaining_balance = income - total_expenses
        st.session_state.budget_data = {
            'income': income,
            'expenses': expenses,
            'investment': remaining_balance,
            'remaining_balance': remaining_balance,
            'data': st.session_state.budget_data['data']
        }

        st.success(f"Remaining Balance: {remaining_balance}")
        
        # Store data for ML model
        st.session_state.budget_data['data'].append({
            'income': income,
            'expenses': total_expenses,
            'investment': remaining_balance,
            'savings': remaining_balance * 0.2  # Example savings
        })

        # Show charts
        st.write("### Expenses Breakdown")
        fig, ax = plt.subplots()
        ax.pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%')
        st.pyplot(fig)

        st.write("### Income vs Expenses")
        fig, ax = plt.subplots()
        ax.bar(["Income", "Total Expenses"], [income, total_expenses])
        st.pyplot(fig)

# Investment Suggestions
elif choice == "Investment Suggestions" and st.session_state.user_logged_in:
    st.title("Investment Suggestions")

    if st.session_state.budget_data['remaining_balance'] > 0:
        model = train_model(st.session_state.budget_data['data'])
        if model:
            prediction = predict_savings(model, st.session_state.budget_data['income'], 
                                         sum(st.session_state.budget_data['expenses'].values()), 
                                         st.session_state.budget_data['remaining_balance'])
            st.write(f"Suggested Investment: ${prediction:.2f}")
        else:
            st.warning("Not enough data to provide suggestions.")
    else:
        st.error("No remaining balance to invest.")

# Expense History
elif choice == "Expense History" and st.session_state.user_logged_in:
    st.title("Expense History")

    if st.session_state.budget_data['expenses']:
        st.write("Your previous expenses:")
        st.write(st.session_state.budget_data['expenses'])
    else:
        st.write("No expense history available.")

# Alerts
elif choice == "Alerts" and st.session_state.user_logged_in:
    st.title("Upcoming Bill Alerts")

    upcoming_bills = [category for category, amount in st.session_state.budget_data['expenses'].items() if amount > 0]

    if upcoming_bills:
        st.write("You have upcoming bills for the following categories:")
        for category in upcoming_bills:
            st.write(f"{category}: ${st.session_state.budget_data['expenses'][category]:.2f}")
    else:
        st.write("No upcoming bills.")

# If not logged in, show login prompt on other pages
if not st.session_state.user_logged_in and choice != "Home":
    st.warning("Please log in to access this page.")
