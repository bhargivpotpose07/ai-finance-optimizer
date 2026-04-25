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
# HEADER
# -------------------------
st.title("💰 AI Financial Optimizer")
st.caption("Income = Annual | Expenses = Monthly")

# -------------------------
# SIDEBAR
# -------------------------
st.sidebar.header("⚙️ Inputs")

income = st.sidebar.number_input("Annual Income (₹)", value=1200000)
rent = st.sidebar.slider("Rent", 0, 50000, 20000)
food = st.sidebar.slider("Food", 0, 20000, 8000)
shopping = st.sidebar.slider("Shopping", 0, 20000, 5000)
entertainment = st.sidebar.slider("Entertainment", 0, 15000, 4000)

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
st.subheader("📊 Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Income", f"₹{int(monthly_income):,}")
c2.metric("Expenses", f"₹{int(monthly_expense):,}")
c3.metric("Savings", f"₹{int(monthly_savings):,}")
c4.metric("Savings %", f"{int(savings_rate)}%")

# -------------------------
# CHARTS
# -------------------------
st.subheader("📈 Expense Analysis")

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
st.subheader("🏛️ Policy Insights")

st.write(f"**Recommended Tax Regime:** {policy['better_regime']}")
st.write(f"**Risk Profile:** {policy['risk_profile']}")

for k, v in policy["allocation"].items():
    st.write(f"- {k}: {v}")

# -------------------------
# PDF (CORPORATE STYLE)
# -------------------------
def generate_pdf(file_path):
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import A4

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        title = ParagraphStyle(name="Title", fontSize=24)
        body = ParagraphStyle(name="Body", fontSize=12)

        content = []

        content.append(Spacer(1, 200))
        content.append(Paragraph("AI FINANCE REPORT", title))
        content.append(Spacer(1, 20))
        content.append(Paragraph(f"Income: ₹{int(monthly_income):,}", body))
        content.append(Paragraph(f"Savings: ₹{int(monthly_savings):,}", body))
        content.append(Paragraph(f"Savings Rate: {int(savings_rate)}%", body))

        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")

if st.button("📄 Generate Report"):
    generate_pdf("report.pdf")
    if os.path.exists("report.pdf"):
        with open("report.pdf", "rb") as f:
            st.download_button("Download PDF", f, "report.pdf")

# -------------------------
# CHATBOT (SMART)
# -------------------------
st.subheader("💬 AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask: Can I buy iPhone for 80000?")

def extract_amount(text):
    nums = re.findall(r'\d+', text)
    return int(nums[0]) if nums else None

def financial_chat(query):
    q = query.lower()
    savings = monthly_savings

    if "milk" in q:
        return f"🛒 Essential. Savings ₹{int(savings):,}, no issue."

    if "iphone" in q:
        return f"📱 You save ₹{int(savings):,}/month. Consider impact before buying."

    if "house" in q:
        return f"🏡 Income ₹{int(monthly_income):,}, savings ₹{int(savings):,}. Plan EMI carefully."

    if "invest" in q:
        return f"📈 Follow {policy['risk_profile']} strategy."

    return "🤖 Ask about buying, saving, investing."

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