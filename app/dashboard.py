import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.policy_engine import apply_policies

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Finance Optimizer", layout="wide")

# -------------------------
# HEADER
# -------------------------
st.title("💰 AI Financial Optimizer")
st.markdown("### 📊 Smart, Interactive Financial Dashboard")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("⚙️ Customize Your Finances")

income = st.sidebar.number_input("Annual Income (₹)", value=1200000)

rent = st.sidebar.slider("🏠 Rent", 0, 50000, 20000)
food = st.sidebar.slider("🍔 Food", 0, 20000, 8000)
shopping = st.sidebar.slider("🛍️ Shopping", 0, 20000, 5000)
entertainment = st.sidebar.slider("🎬 Entertainment", 0, 15000, 4000)

# -------------------------
# CALCULATIONS
# -------------------------
monthly_income = income / 12
monthly_expense = rent + food + shopping + entertainment
monthly_savings = monthly_income - monthly_expense
savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

policy = apply_policies(income, monthly_savings)

# -------------------------
# METRICS
# -------------------------
st.subheader("📈 Financial Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("💰 Income", f"₹{int(monthly_income):,}")
c2.metric("💸 Expenses", f"₹{int(monthly_expense):,}")
c3.metric("💾 Savings", f"₹{int(monthly_savings):,}")
c4.metric("📊 Savings %", f"{int(savings_rate)}%")

# -------------------------
# INSIGHTS (LIVE FEEDBACK)
# -------------------------
st.subheader("🧠 Insights")

if savings_rate < 10:
    st.error("⚠️ Very low savings. Reduce expenses immediately.")
elif savings_rate < 20:
    st.warning("⚠️ Moderate savings. Try improving.")
else:
    st.success("✅ Excellent financial health!")

# -------------------------
# CHARTS
# -------------------------
st.subheader("📊 Expense Visualization")

chart_data = pd.DataFrame({
    "Category": ["Rent", "Food", "Shopping", "Entertainment"],
    "Amount": [rent, food, shopping, entertainment]
})

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(chart_data.set_index("Category"))

with col2:
    fig, ax = plt.subplots()
    ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
    st.pyplot(fig)

# -------------------------
# POLICY SECTION
# -------------------------
st.subheader("🏛️ Smart Recommendations")

st.write(f"**Tax Regime:** {policy['better_regime']}")
st.write(f"**Risk Profile:** {policy['risk_profile']}")

for k, v in policy["allocation"].items():
    st.write(f"• {k}: {v}")

# -------------------------
# CHATBOT (INTERACTIVE)
# -------------------------
st.subheader("💬 AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything...")

def financial_chat(q):
    q = q.lower()
    savings = monthly_savings

    if "iphone" in q:
        return f"📱 You save ₹{int(savings):,}/month. Consider if this affects your savings."
    if "house" in q:
        return f"🏡 With ₹{int(savings):,}/month savings, plan EMI carefully."
    if "milk" in q:
        return "🛒 Basic need. No issue buying it."
    if "invest" in q:
        return f"📈 Follow {policy['risk_profile']} strategy."

    return "🤖 Try asking about buying, saving, or investing."

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = financial_chat(user_input)

    st.session_state.messages.append({"role":"assistant","content":reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🚀 Built by Bhargiv")