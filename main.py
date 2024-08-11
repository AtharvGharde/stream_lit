import streamlit as st
import pandas as pd

# Title of the app
st.title('Simple Budget-Making Application')

# Input for wages
wages = st.number_input('Enter your monthly wages:', min_value=0, format='%d')

# Input for expense categories
st.header('Expenses')
categories = st.text_area('Enter your expense categories (comma-separated):', 'Rent, Groceries, Utilities, Entertainment')
categories_list = [cat.strip() for cat in categories.split(',')]

expenses = {}
for cat in categories_list:
    amount = st.number_input(f'Enter amount for {cat}:', min_value=0, format='%d', key=f'expense_{cat}')
    expenses[cat] = amount

# Input for investments
st.header('Investments')
investments = st.text_area('Enter your investments (comma-separated, e.g., Mutual Funds, Stocks, Insurance):', 'Mutual Funds, Stocks, Insurance')
investments_list = [inv.strip() for inv in investments.split(',')]

investment_amounts = {}
for inv in investments_list:
    amount = st.number_input(f'Enter amount for {inv}:', min_value=0, format='%d', key=f'investment_{inv}')
    investment_amounts[inv] = amount

# Calculate total expenses, investments, and remaining balance
total_expenses = sum(expenses.values())
total_investments = sum(investment_amounts.values())
remaining_balance = wages - total_expenses - total_investments

# Display results
st.write(f'Total Expenses: ${total_expenses}')
st.write(f'Total Investments: ${total_investments}')
st.write(f'Remaining Balance: ${remaining_balance}')

# Visualization
if total_expenses > 0:
    st.subheader('Expense Distribution')
    expense_df = pd.DataFrame(list(expenses.items()), columns=['Category', 'Amount'])
    st.bar_chart(expense_df.set_index('Category'))

if total_investments > 0:
    st.subheader('Investment Distribution')
    investment_df = pd.DataFrame(list(investment_amounts.items()), columns=['Investment', 'Amount'])
    st.bar_chart(investment_df.set_index('Investment'))
