import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from utils.score import financial_score

# -------------------------
# 🎨 PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Finance Optimizer", layout="wide")

# -------------------------
# 🎨 CUSTOM UI
# -------------------------
st.markdown("""
<style>
body { background-color: #0f172a; }
h1, h2, h3 { color: #e2e8f0; }
.stMetric { background-color: #1e293b; padding: 15px; border-radius: 12px; }
.stButton>button { background-color: #22c55e; color: white; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# 🏆 HEADER
# -------------------------
st.title("💰 AI Financial Optimizer")
st.caption("Smart decisions. Better future.")

# -------------------------
# 📊 SIDEBAR INPUT
# -------------------------
st.sidebar.header("⚙️ Financial Inputs")

income = st.sidebar.number_input("Annual Income (₹)", value=600000)
rent = st.sidebar.slider("Rent", 0, 50000, 15000)
food = st.sidebar.slider("Food", 0, 20000, 6000)
shopping = st.sidebar.slider("Shopping", 0, 20000, 5000)
entertainment = st.sidebar.slider("Entertainment", 0, 15000, 4000)

# -------------------------
# 🧮 CALCULATIONS
# -------------------------
monthly_income = income / 12
monthly_expense = rent + food + shopping + entertainment
monthly_savings = monthly_income - monthly_expense
savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income > 0 else 0
expense_ratio = monthly_expense / monthly_income if monthly_income > 0 else 0

# dummy anomaly count (for now)
anomalies = 3

# -------------------------
# 🏆 FINANCIAL SCORE
# -------------------------
score = financial_score(savings_rate, anomalies, expense_ratio)

# -------------------------
# 📊 METRICS
# -------------------------
st.subheader("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💸 Expense", f"₹{monthly_expense}")
col2.metric("💰 Savings", f"₹{int(monthly_savings)}")
col3.metric("📈 Savings %", f"{int(savings_rate)}%")

if score > 80:
    col4.metric("Score", "Excellent 💎")
elif score > 50:
    col4.metric("Score", "Moderate ⚠️")
else:
    col4.metric("Score", "Poor ❌")

# -------------------------
# 📈 CHARTS
# -------------------------
st.subheader("📈 Expense Breakdown")

chart_data = pd.DataFrame({
    "Category": ["Rent", "Food", "Shopping", "Entertainment"],
    "Amount": [rent, food, shopping, entertainment]
})

st.bar_chart(chart_data.set_index("Category"))

# Pie chart
fig, ax = plt.subplots()
ax.pie(
    [rent, food, shopping, entertainment],
    labels=["Rent", "Food", "Shopping", "Entertainment"],
    autopct='%1.1f%%'
)
st.pyplot(fig)

# -------------------------
# 🧠 AI INSIGHTS
# -------------------------
st.subheader("🧠 AI Insights")

if savings_rate < 10:
    st.error("⚠️ Critical: You are saving too little.")
elif savings_rate < 20:
    st.warning("⚠️ Improve your savings.")
else:
    st.success("✅ Good financial health.")

# smart alerts
if rent > monthly_income * 0.4:
    st.warning("🏠 Rent is too high (>40% of income)")

if shopping > food:
    st.warning("🛍️ Shopping exceeds food → impulse spending")

# -------------------------
# 🧾 TAX SYSTEM
# -------------------------
st.subheader("🧾 Tax Optimization")

def tax_new(income):
    if income <= 1200000:
        return 0
    elif income <= 1500000:
        return int(income * 0.1)
    else:
        return int(income * 0.2)

def tax_old(income):
    if income <= 250000:
        return 0
    elif income <= 500000:
        return int(income * 0.05)
    elif income <= 1000000:
        return int(income * 0.2)
    else:
        return int(income * 0.3)

new_tax = tax_new(income)
old_tax = tax_old(income)

col1, col2 = st.columns(2)
col1.metric("New Regime", f"₹{new_tax}")
col2.metric("Old Regime", f"₹{old_tax}")

if new_tax < old_tax:
    st.success("Recommended: New Regime")
else:
    st.info("Recommended: Old Regime")

# -------------------------
# 💡 RECOMMENDATIONS
# -------------------------
st.subheader("💡 Recommendations")

if st.button("Generate Advice"):
    if monthly_savings < 0:
        st.write("👉 Reduce unnecessary expenses")
    if savings_rate < 20:
        st.write("👉 Increase savings to 20%")
    st.write("👉 Invest in mutual funds")
    st.write("👉 Build emergency fund")

# -------------------------
# 🛒 AFFORDABILITY CHECK
# -------------------------
st.subheader("🛒 Can You Afford This?")

item_price = st.number_input("Item Price (₹)", value=20000)

if st.button("Check Affordability"):
    if item_price < monthly_savings * 3:
        st.success("✅ You can afford this")
    elif item_price < monthly_savings * 6:
        st.warning("⚠️ Risky purchase")
    else:
        st.error("❌ Not recommended")

# -------------------------
# 🎯 SAVINGS GOAL
# -------------------------
st.subheader("🎯 Savings Goal")

goal = st.number_input("Goal Amount (₹)", value=500000)

months = goal / max(monthly_savings, 1)
st.info(f"Goal achievable in {int(months)} months")

# -------------------------
# 📊 WEALTH PROJECTION
# -------------------------
st.subheader("📊 Future Wealth")

years = st.slider("Years", 1, 15, 5)

future_value = max(monthly_savings, 0) * 12 * years * 1.12

st.metric("Projected Wealth", f"₹{int(future_value)}")
st.caption("Assuming 12% return")