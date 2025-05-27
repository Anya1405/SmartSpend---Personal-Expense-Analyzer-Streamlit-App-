# SmartSpend - Streamlit Expense Analyzer App (Enhanced)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

st.set_page_config(page_title="SmartSpend Tracker", layout="wide")
st.title("💰 SmartSpend - Personal Expense Analyzer")

# --- Initialize session state ---
if 'expenses' not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

if 'budget' not in st.session_state:
    st.session_state.budget = 0.0

# --- Sidebar: Expense Input Form ---
st.sidebar.header("💸 Add New Expense")
date = st.sidebar.date_input("Date", datetime.now())
category = st.sidebar.selectbox("Category", ["Food", "Rent", "Utilities", "Transport", "Shopping", "Subscriptions", "Dining", "Miscellaneous"])
amount = st.sidebar.number_input("Amount ($)", min_value=0.0, format="%.2f")
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    new_expense = pd.DataFrame([[date, category, amount, description]], columns=['Date', 'Category', 'Amount', 'Description'])
    st.session_state.expenses = pd.concat([st.session_state.expenses, new_expense], ignore_index=True)
    st.sidebar.success("Expense added!")

# --- Sidebar: Monthly Budget ---
st.sidebar.header("📅 Monthly Budget")
st.session_state.budget = st.sidebar.number_input("Set Monthly Budget ($)", min_value=0.0, value=st.session_state.budget, format="%.2f")

# --- Main Section: Display & Analysis ---
st.subheader("📋 Expense Log")
st.dataframe(st.session_state.expenses)

if not st.session_state.expenses.empty:
    df = st.session_state.expenses.copy()
    df['Date'] = pd.to_datetime(df['Date'])

    total_spent = df['Amount'].sum()
    st.metric("Total Spent", f"${total_spent:.2f}", delta=f"Budget: ${st.session_state.budget:.2f}")

    # Budget Progress Bar
    if st.session_state.budget > 0:
        progress = min(1.0, total_spent / st.session_state.budget)
        st.progress(progress)

    st.subheader("📊 Spending by Category")
    cat_totals = df.groupby('Category')['Amount'].sum().reset_index().sort_values(by='Amount', ascending=False)
    fig1, ax1 = plt.subplots()
    sns.barplot(data=cat_totals, x='Amount', y='Category', ax=ax1, palette='viridis')
    ax1.set_xlabel("Total Spent ($)")
    st.pyplot(fig1)

    st.subheader("📈 Daily Spending Trend")
    daily = df.groupby('Date')['Amount'].sum().reset_index()
    fig2, ax2 = plt.subplots()
    ax2.plot(daily['Date'], daily['Amount'], marker='o', linestyle='-')
    ax2.set_ylabel("Amount Spent ($)")
    ax2.set_xlabel("Date")
    st.pyplot(fig2)

    st.subheader("💡 Recommendations")
    recs = []
    if df[df['Category'] == 'Dining']['Amount'].sum() > 200:
        recs.append("Consider reducing dining out and cooking at home more often.")
    if df[df['Category'] == 'Subscriptions']['Amount'].sum() > 100:
        recs.append("Review and cancel unused subscriptions.")
    if df['Category'].value_counts().get('Miscellaneous', 0) > 5:
        recs.append("Too many 'Miscellaneous' expenses — consider categorizing better.")

    if recs:
        for rec in recs:
            st.markdown(f"- ✅ {rec}")
    else:
        st.info("Your spending looks balanced. Great job!")

    # Export to CSV
    st.subheader("📤 Export Expenses")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='expenses.csv',
        mime='text/csv'
    )
else:
    st.info("Add some expenses to see analytics and recommendations.")


