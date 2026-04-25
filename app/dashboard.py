import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="AI Finance Optimizer", layout="wide")

# -------------------------
# UI STYLE
# -------------------------
st.markdown("""
<style>
.stMetric {
    background: #111827;
    padding: 15px;
    border-radius: 12px;
}
h1, h2, h3 {
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("💰 AI Finance Optimizer Pro")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("⚙️ Financial Inputs")

income = st.sidebar.number_input("Annual Income (₹)", value=1200000)

rent = st.sidebar.slider("🏠 Rent", 0, 50000, 20000)
food = st.sidebar.slider("🍔 Food", 0, 20000, 8000)
shopping = st.sidebar.slider("🛍️ Shopping", 0, 20000, 5000)
entertainment = st.sidebar.slider("🎬 Entertainment", 0, 15000, 4000)
utilities = st.sidebar.slider("💡 Utilities", 0, 10000, 3000)
transport = st.sidebar.slider("🚗 Transport", 0, 15000, 5000)
health = st.sidebar.slider("🏥 Health", 0, 10000, 2000)

# -------------------------
# CALCULATIONS
# -------------------------
monthly_income = income / 12
monthly_expense = rent + food + shopping + entertainment + utilities + transport + health
monthly_savings = monthly_income - monthly_expense
savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

def calculate_tax(income):
    if income > 1500000:
        return int(income * 0.30)
    elif income > 1200000:
        return int(income * 0.20)
    elif income > 700000:
        return int(income * 0.10)
    return 0

tax_amount = calculate_tax(income)

# -------------------------
# METRICS
# -------------------------
st.subheader("📊 Dashboard")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Income", f"₹{int(monthly_income):,}")
c2.metric("Expenses", f"₹{int(monthly_expense):,}")
c3.metric("Savings", f"₹{int(monthly_savings):,}")
c4.metric("Tax", f"₹{tax_amount:,}")

# -------------------------
# CHARTS
# -------------------------
st.subheader("📊 Expense Analysis")

chart_data = pd.DataFrame({
    "Category": ["Rent","Food","Shopping","Entertainment","Utilities","Transport","Health"],
    "Amount": [rent, food, shopping, entertainment, utilities, transport, health]
})

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(chart_data.set_index("Category"))

with col2:
    fig, ax = plt.subplots()
    ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
    st.pyplot(fig)

# -------------------------
# INVESTMENT SECTION
# -------------------------
st.subheader("📈 Investment")

sip = st.number_input("Monthly SIP (₹)", 1000, 100000, 5000)
years = st.slider("Years", 1, 30, 10)
rate = st.slider("Return (%)", 5, 20, 12)

months = years * 12
monthly_rate = rate / 12 / 100
future_value = sip * (((1 + monthly_rate)**months - 1) / monthly_rate) * (1 + monthly_rate)

st.metric("Projected Wealth", f"₹{int(future_value):,}")

# -------------------------
# POLICY
# -------------------------
st.subheader("🏛️ Policy")

st.write(f"Tax Estimate: ₹{tax_amount:,}")
st.write("GST: 5%–28% depending on category")

# -------------------------
# CHATBOT
# -------------------------
st.subheader("💬 AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

def smart_chat(q):
    q = q.lower()
    nums = re.findall(r'\d+', q)
    amt = int(nums[0]) if nums else None

    if "house" in q:
        return f"🏡 Income ₹{int(monthly_income):,}, savings ₹{int(monthly_savings):,}. Plan EMI carefully."

    if "buy" in q:
        if amt:
            return f"📊 Cost ₹{amt:,} vs savings ₹{int(monthly_savings):,}"
        return f"📊 Savings ₹{int(monthly_savings):,}"

    if "tax" in q:
        return f"🏛️ Tax ₹{tax_amount:,}"

    if "sip" in q:
        return f"📈 ₹{sip} SIP → ₹{int(future_value):,} in {years} years"

    return "Ask about buying, tax, or investment."

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    reply = smart_chat(user_input)

    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# -------------------------
# PDF
# -------------------------
def generate_pdf(file):
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import ParagraphStyle

    doc = SimpleDocTemplate(file)

    style = ParagraphStyle(name="Body", fontSize=12)

    content = []
    content.append(Paragraph("AI Finance Report", style))
    content.append(Paragraph(f"Income ₹{int(monthly_income):,}", style))
    content.append(Paragraph(f"Savings ₹{int(monthly_savings):,}", style))

    doc.build(content)

st.subheader("📄 Report")

if st.button("Generate PDF"):
    generate_pdf("report.pdf")
    with open("report.pdf", "rb") as f:
        st.download_button("Download", f, "report.pdf")

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🚀 AI Finance Optimizer Pro")