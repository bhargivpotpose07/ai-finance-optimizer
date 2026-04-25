import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from utils.policy_engine import apply_policies

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Finance Optimizer", layout="wide")

# -------------------------
# UI STYLE
# -------------------------
st.markdown("""
<style>
body { background-color: #0f172a; }
h1 { color: #f8fafc; }
[data-testid="stMetric"] {
    background-color: #1e293b;
    border-radius: 10px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("💰 AI Financial Optimizer")

# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.caption("💡 Income is annual, expenses are monthly")
income = st.sidebar.number_input("Annual Income (₹)", value=600000)
rent = st.sidebar.slider("Rent", 0, 50000, 15000)
food = st.sidebar.slider("Food", 0, 20000, 6000)
shopping = st.sidebar.slider("Shopping", 0, 20000, 5000)
entertainment = st.sidebar.slider("Entertainment", 0, 15000, 4000)

# -------------------------
# CALCULATIONS
# -------------------------
monthly_income = income / 12
monthly_expense = rent + food + shopping + entertainment
monthly_savings = monthly_income - monthly_expense
savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

# -------------------------
# POLICY ENGINE
# -------------------------
policy = apply_policies(income, monthly_savings)

# -------------------------
# METRICS
# -------------------------
c1, c2, c3, c4 = st.columns(4)
c1.metric("Expenses", f"₹{int(monthly_expense):,}")
c2.metric("Savings", f"₹{int(monthly_savings):,}")
c3.metric("Savings %", f"{int(savings_rate)}%")
c4.metric("Risk", policy["risk_profile"])

# -------------------------
# CHART
# -------------------------
chart_data = pd.DataFrame({
    "Category": ["Rent", "Food", "Shopping", "Entertainment"],
    "Amount": [rent, food, shopping, entertainment]
})

st.bar_chart(chart_data.set_index("Category"))

# -------------------------
# PDF FUNCTION (FIXED)
# -------------------------
def generate_pdf(file_path):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import A4

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        title = ParagraphStyle(name="Title", fontSize=20)
        body = ParagraphStyle(name="Body", fontSize=12)

        content = []

        content.append(Spacer(1, 200))
        content.append(Paragraph("AI FINANCE REPORT", title))
        content.append(Spacer(1, 20))
        content.append(Paragraph(f"Savings Rate: {int(savings_rate)}%", body))

        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")

# -------------------------
# PDF BUTTON
# -------------------------
if st.button("Generate PDF"):
    generate_pdf("report.pdf")
    if os.path.exists("report.pdf"):
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, "report.pdf")

# -------------------------
# 💬 SMART CHATBOT (FINAL)
# -------------------------
st.subheader("💬 AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something like: Can I buy iPhone for 80000?")

def extract_amount(text):
    nums = re.findall(r'\d+', text.replace(',', ''))
    return int(nums[0]) if nums else None

def financial_chat(query):
    q = query.lower()
    amt = extract_amount(q)

    savings = monthly_savings
    income_val = monthly_income

    # NECESSITIES
    if any(x in q for x in ["milk","food","groceries","vegetables","medicine"]):
        return f"🛒 Essential expense. Your savings ₹{int(savings):,} — no issue buying this."

    # MEDIUM
    if any(x in q for x in ["phone","iphone","laptop","bike"]):
        if savings <= 0:
            return f"❌ You have ₹{int(savings):,} savings. Avoid this purchase."

        if amt:
            if amt > savings * 3:
                return f"⚠️ ₹{amt} is too high vs your savings ₹{int(savings):,}."
            elif amt < savings:
                return f"✅ Affordable. Cost ₹{amt}, savings ₹{int(savings):,}."
            else:
                return "⚠️ It will reduce your savings significantly."

        return f"📱 Your savings ₹{int(savings):,}. Evaluate carefully."

    # BIG
    if any(x in q for x in ["house","home","car"]):
        return (
            f"🏡 Big decision.\n\n"
            f"Income: ₹{int(income_val):,}/month\n"
            f"Savings: ₹{int(savings):,}/month\n\n"
            f"Ensure EMI < 40% income + emergency fund."
        )

    # OTHER
    if "invest" in q:
        return f"📈 Follow {policy['risk_profile']} investment strategy."

    if "save" in q:
        return f"💰 Your savings rate is {int(savings_rate)}%. Aim for 20–30%."

    if "tax" in q:
        return f"🏛️ {policy['better_regime']} regime is better."

    return "🤖 Ask about buying, investing, savings, or tax."

# CHAT EXECUTION
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