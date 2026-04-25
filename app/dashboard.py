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
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("⚙️ Inputs")

income = st.sidebar.number_input("Annual Income (₹)", value=600000)
rent = st.sidebar.slider("Rent (Monthly)", 0, 50000, 15000)
food = st.sidebar.slider("Food (Monthly)", 0, 20000, 6000)
shopping = st.sidebar.slider("Shopping (Monthly)", 0, 20000, 5000)
entertainment = st.sidebar.slider("Entertainment (Monthly)", 0, 15000, 4000)

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
c1, c2, c3, c4 = st.columns(4)
c1.metric("Income", f"₹{int(monthly_income):,}")
c2.metric("Expenses", f"₹{int(monthly_expense):,}")
c3.metric("Savings", f"₹{int(monthly_savings):,}")
c4.metric("Savings %", f"{int(savings_rate)}%")

# -------------------------
# CHART
# -------------------------
st.subheader("📊 Expense Breakdown")

chart_data = pd.DataFrame({
    "Category": ["Rent", "Food", "Shopping", "Entertainment"],
    "Amount": [rent, food, shopping, entertainment]
})

st.bar_chart(chart_data.set_index("Category"))

# -------------------------
# PDF GENERATION (CORPORATE)
# -------------------------
def generate_pdf(file_path):
    try:
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
        )
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import A4

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        title = ParagraphStyle(name="Title", fontSize=26, alignment=1, spaceAfter=30)
        subtitle = ParagraphStyle(name="Subtitle", fontSize=14, alignment=1, spaceAfter=20)
        heading = ParagraphStyle(name="Heading", fontSize=16, spaceAfter=12)
        body = ParagraphStyle(name="Body", fontSize=11, spaceAfter=10)

        content = []

        # COVER PAGE
        content.append(Spacer(1, 200))
        content.append(Paragraph("AI FINANCE REPORT", title))
        content.append(Paragraph("Financial Advisory Report", subtitle))
        content.append(Paragraph(datetime.now().strftime("%d %B %Y"), body))
        content.append(PageBreak())

        # SUMMARY
        content.append(Paragraph("Executive Summary", heading))
        content.append(Paragraph(
            f"Your monthly income is ₹{int(monthly_income):,} and savings are ₹{int(monthly_savings):,}.",
            body
        ))
        content.append(Paragraph(
            f"Savings rate: <b>{int(savings_rate)}%</b> indicating "
            f"{'strong' if savings_rate > 20 else 'moderate' if savings_rate > 10 else 'low'} financial health.",
            body
        ))

        # TABLE
        table_data = [
            ["Metric", "Value"],
            ["Income", f"₹{int(monthly_income):,}"],
            ["Expenses", f"₹{int(monthly_expense):,}"],
            ["Savings", f"₹{int(monthly_savings):,}"]
        ]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.black),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
        ]))

        content.append(table)
        content.append(Spacer(1, 20))

        # CHART
        fig, ax = plt.subplots()
        ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
        chart_path = "chart.png"
        plt.savefig(chart_path)
        plt.close()

        content.append(Paragraph("Expense Distribution", heading))
        content.append(Image(chart_path, width=400, height=300))

        # POLICY
        content.append(Spacer(1, 20))
        content.append(Paragraph("Policy Insights", heading))
        content.append(Paragraph(f"Recommended Regime: {policy['better_regime']}", body))
        content.append(Paragraph(f"Risk Profile: {policy['risk_profile']}", body))

        for k, v in policy["allocation"].items():
            content.append(Paragraph(f"{k}: {v}", body))

        # RECOMMENDATION
        content.append(Spacer(1, 20))
        content.append(Paragraph("Recommendations", heading))

        if savings_rate < 20:
            content.append(Paragraph("Increase savings and reduce unnecessary expenses.", body))
        else:
            content.append(Paragraph("Maintain strong financial discipline and invest wisely.", body))

        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")

# PDF BUTTON
if st.button("📄 Generate Professional Report"):
    generate_pdf("report.pdf")

    if os.path.exists("report.pdf"):
        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, "AI_Finance_Report.pdf")

# -------------------------
# 💬 SMART CHATBOT
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
    amt = extract_amount(q)

    savings = monthly_savings

    if "milk" in q:
        return f"🛒 Essential expense. Your savings ₹{int(savings):,} — no issue."

    if "iphone" in q or "phone" in q:
        return f"📱 Your savings ₹{int(savings):,}. Consider if it impacts savings."

    if "house" in q:
        return f"🏡 Income ₹{int(monthly_income):,}/month, savings ₹{int(savings):,}. Plan EMI carefully."

    if "invest" in q:
        return f"📈 Follow {policy['risk_profile']} strategy."

    return "🤖 Ask about buying, investing, savings."

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
st.caption("🚀 Built by Bhargiv | AI Finance Optimizer")