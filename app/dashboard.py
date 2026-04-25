import sys, os, re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="AI Finance Optimizer", layout="wide")

# -------------------------
# PREMIUM UI STYLE
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
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("💰 AI Finance Optimizer Pro")
st.caption("Smart Financial Planning System")

# -------------------------
# SIDEBAR (MORE EXPENSES)
# -------------------------
st.sidebar.header("⚙️ Financial Inputs")

income = st.sidebar.number_input("Annual Income (₹)", value=1200000)

rent = st.sidebar.slider("🏠 Rent", 0, 50000, 20000)
food = st.sidebar.slider("🍔 Food", 0, 20000, 8000)
shopping = st.sidebar.slider("🛍️ Shopping", 0, 20000, 5000)
entertainment = st.sidebar.slider("🎬 Entertainment", 0, 15000, 4000)
utilities = st.sidebar.slider("💡 Utilities (Electricity, Internet)", 0, 10000, 3000)
transport = st.sidebar.slider("🚗 Transport", 0, 15000, 5000)
health = st.sidebar.slider("🏥 Health", 0, 10000, 2000)

# -------------------------
# CALCULATIONS
# -------------------------
monthly_income = income / 12

monthly_expense = (
    rent + food + shopping + entertainment +
    utilities + transport + health
)

monthly_savings = monthly_income - monthly_expense
savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

# -------------------------
# TAX LOGIC (UPDATED INDIA STYLE SIMPLIFIED)
# -------------------------
def calculate_tax(income):
    # simplified new regime logic
    tax = 0
    if income > 1500000:
        tax = income * 0.30
    elif income > 1200000:
        tax = income * 0.20
    elif income > 700000:
        tax = income * 0.10
    else:
        tax = 0
    return int(tax)

tax_amount = calculate_tax(income)

# -------------------------
# METRICS
# -------------------------
st.subheader("📊 Financial Dashboard")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Income", f"₹{int(monthly_income):,}")
c2.metric("Expenses", f"₹{int(monthly_expense):,}")
c3.metric("Savings", f"₹{int(monthly_savings):,}")
c4.metric("Tax (Annual)", f"₹{tax_amount:,}")

# -------------------------
# INSIGHTS
# -------------------------
st.subheader("🧠 AI Insights")

if savings_rate < 10:
    st.error("⚠️ Low savings — high financial risk")
elif savings_rate < 20:
    st.warning("⚠️ Moderate savings — can improve")
else:
    st.success("✅ Strong financial health")

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
# POLICY SECTION
# -------------------------
st.subheader("🏛️ Government Policy Insights")

st.write("**Income Tax (India - New Regime Approximation)**")
st.write(f"Estimated Annual Tax: ₹{tax_amount:,}")

st.write("**GST Impact (Approx)**")
st.write("• Essentials: 5%")
st.write("• Electronics: 18%")
st.write("• Luxury: 28%")

# -------------------------
# 💬 SMART CHATBOT (UPGRADED)
# -------------------------
st.subheader("💬 AI Financial Advisor Pro")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask anything about your finances...")

def smart_chat(q):
    q = q.lower()

    if "buy" in q:
        return (
            f"Based on your monthly savings of ₹{int(monthly_savings):,}, "
            f"this purchase should be evaluated carefully.\n\n"
            f"If it exceeds 2–3x your savings, it may impact your financial stability."
        )

    if "invest" in q:
        return (
            "Diversify investments:\n"
            "• Equity for growth\n"
            "• Debt for stability\n"
            "• Emergency fund first"
        )

    if "tax" in q:
        return f"Your estimated tax is ₹{tax_amount:,} under current structure."

    return "Ask about buying, saving, investing, or tax."

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = smart_chat(user_input)

    st.session_state.messages.append({"role":"assistant","content":reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

# -------------------------
def generate_pdf(file_path):
    try:
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        )
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import A4

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        # -------------------------
        # STYLES
        # -------------------------
        title = ParagraphStyle(name="Title", fontSize=28, alignment=1, spaceAfter=30)
        subtitle = ParagraphStyle(name="Subtitle", fontSize=14, alignment=1, spaceAfter=20)
        heading = ParagraphStyle(name="Heading", fontSize=18, spaceAfter=12)
        body = ParagraphStyle(name="Body", fontSize=12, spaceAfter=10)

        content = []

        # -------------------------
        # COVER PAGE
        # -------------------------
        content.append(Spacer(1, 200))
        content.append(Paragraph("AI FINANCE REPORT", title))
        content.append(Paragraph("Financial Analysis & Advisory", subtitle))
        content.append(Paragraph(datetime.now().strftime("%d %B %Y"), body))
        content.append(PageBreak())

        # -------------------------
        # EXECUTIVE SUMMARY
        # -------------------------
        content.append(Paragraph("Executive Summary", heading))

        content.append(Paragraph(
            f"This report analyzes your financial position based on income, expenses, and savings behavior.",
            body
        ))

        content.append(Paragraph(
            f"Your monthly income is <b>₹{int(monthly_income):,}</b> and expenses are "
            f"<b>₹{int(monthly_expense):,}</b>, resulting in savings of "
            f"<b>₹{int(monthly_savings):,}</b>.",
            body
        ))

        content.append(Paragraph(
            f"Your savings rate is <b>{int(savings_rate)}%</b>, indicating "
            f"{'strong' if savings_rate > 20 else 'moderate' if savings_rate > 10 else 'low'} financial health.",
            body
        ))

        # -------------------------
        # FINANCIAL BREAKDOWN TABLE
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Financial Breakdown", heading))

        table_data = [
            ["Metric", "Amount (₹)"],
            ["Monthly Income", f"{int(monthly_income):,}"],
            ["Monthly Expenses", f"{int(monthly_expense):,}"],
            ["Monthly Savings", f"{int(monthly_savings):,}"],
            ["Annual Tax", f"{tax_amount:,}"]
        ]

        table = Table(table_data, colWidths=[250, 150])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")
        ]))

        content.append(table)

        # -------------------------
        # EXPENSE ANALYSIS
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Expense Analysis", heading))

        content.append(Paragraph(
            f"Your total monthly expenses are ₹{int(monthly_expense):,}. "
            f"Major spending categories include rent, food, and discretionary expenses.",
            body
        ))

        # -------------------------
        # TAX ANALYSIS
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Tax Analysis", heading))

        content.append(Paragraph(
            f"Based on your annual income, your estimated tax liability is "
            f"<b>₹{tax_amount:,}</b> under the current tax structure.",
            body
        ))

        content.append(Paragraph(
            "Consider tax-saving investments and deductions to reduce liability.",
            body
        ))

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Recommendations", heading))

        if savings_rate < 20:
            content.append(Paragraph(
                "• Increase savings by reducing discretionary expenses.\n"
                "• Track monthly spending more closely.\n"
                "• Build an emergency fund of at least 6 months.",
                body
            ))
        else:
            content.append(Paragraph(
                "• Maintain current savings discipline.\n"
                "• Increase investment allocation.\n"
                "• Diversify portfolio for long-term growth.",
                body
            ))

        # -------------------------
        # BUILD PDF
        # -------------------------
        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")
# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🚀 AI Finance Optimizer Pro")