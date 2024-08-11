import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

# Initialize session state
if 'user_logged_in' not in st.session_state:
    st.session_state.user_logged_in = False
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = []

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

# Sidebar for Navigation
st.sidebar.title("Navigation")
pages = ["Home", "Budget Calculator"]
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
    expenses = st.number_input("Enter your monthly expenses:", min_value=0)
    investment = income - expenses
    st.session_state.budget_data.append({
        'income': income,
        'expenses': expenses,
        'investment': investment,
        'savings': investment * 0.2
    })
    st.write("Income:", income)
    st.write("Expenses:", expenses)
    st.write("Investment:", investment)

# If not logged in, show login prompt on other pages
if not st.session_state.user_logged_in and choice != "Home":
    st.warning("Please log in to access this page.")
