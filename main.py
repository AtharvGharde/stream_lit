import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Initialize session state
if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False
if "budget_data" not in st.session_state:
    st.session_state.budget_data = {
        "income": 0,
        "expenses": {},
        "investment": {},
        "remaining_balance": 0,
        "data": []
    }

# Hardcoded login credentials
def login(username, password):
    if username == "developer" and password == "password123":
        st.session_state.user_logged_in = True
        return True
    return False

# Machine Learning Model
def train_model(data):
    df = pd.DataFrame(data)
    X = df[["income", "expenses", "investment"]]
    y = df["savings"]
    model = LinearRegression().fit(X, y)
    return model

def predict_savings(model, income, expenses, investment):
    return model.predict([[income, expenses, investment]])[0]

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

    st.session_state.budget_data['income'] = st.number_input("Enter your monthly income:", min_value=0)
    categories = ["Groceries", "Medicine", "Entertainment", "Rent", "Utilities", "Loans", "EMIs", "Investments", "Bills"]

    for category in categories:
        st.session_state.budget_data['expenses'][category] = st.number_input(f"{category}:", min_value=0)

    if st.button("Calculate Budget"):
        total_expenses = sum(st.session_state.budget_data['expenses'].values())
        st.session_state.budget_data['remaining_balance'] = st.session_state.budget_data['income'] - total_expenses
        st.success(f"Remaining Balance: {st.session_state.budget_data['remaining_balance']}")
        
        # Store data for ML model
        st.session_state.budget_data['data'].append({
            "income": st.session_state.budget_data['income'],
            "expenses": total_expenses,
            "investment": st.session_state.budget_data['remaining_balance'],
            "savings": st.session_state.budget_data['remaining_balance'] * 0.2  # Example savings
        })

# Investment Suggestions
elif choice == "Investment Suggestions" and st.session_state.user_logged_in:
    st.title("Investment Suggestions")

    if st.session_state.budget_data['remaining_balance'] > 0:
        model = train_model(st.session_state.budget_data['data'])
        prediction = predict_savings(model, st.session_state.budget_data['income'], 
                                     sum(st.session_state.budget_data['expenses'].values()), 
                                     st.session_state.budget_data['remaining_balance'])
        st.write(f"Suggested Investment: {prediction}")
    else:
        st.error("No remaining balance to invest.")

# Expense History
elif choice == "Expense History" and st.session_state.user_logged_in:
    st.title("Expense History")

    st.write("Your previous expenses:")
    st.write(st.session_state.budget_data['expenses'])

# Alerts
elif choice == "Alerts" and st.session_state.user_logged_in:
    st.title("Upcoming Bill Alerts")

    st.write("You have upcoming bills for the following categories:")
    for category, amount in st.session_state.budget_data['expenses'].items():
        if amount > 0:
            st.write(f"{category}: ${amount}")

# If not logged in, show login prompt on other pages
if not st.session_state.user_logged_in and choice != "Home":
    st.warning("Please log in to access this page.")
