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
# -------------------------
# 💬 AI CHATBOT (FINAL WORKING)
# -------------------------
# -------------------------
# 💬 AI CHATBOT (FINAL FIX)
# -------------------------
# -------------------------
# 💬 AI FINANCIAL CHATBOT (SMART)
# -------------------------
st.subheader("💬 AI Financial Advisor")

# INIT SESSION
if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# INPUT BOX
user_input = st.chat_input("Ask: Can I buy iPhone for 80000?")

# -------------------------
# 🧠 SMART CHAT FUNCTION
# -------------------------
def smart_chat(q):
    q = q.lower()

    nums = re.findall(r'\d+', q.replace(',', ''))
    amt = int(nums[0]) if nums else None

    savings = monthly_savings
    income_val = monthly_income
    expense = monthly_expense

    # 🏡 HOUSE
    if "house" in q or "home" in q:
        emi_limit = income_val * 0.35
        return (
            f"🏡 Buying a house requires careful planning.\n\n"
            f"📊 Your Financial Snapshot:\n"
            f"• Monthly Income: ₹{int(income_val):,}\n"
            f"• Monthly Expenses: ₹{int(expense):,}\n"
            f"• Monthly Savings: ₹{int(savings):,}\n\n"
            f"💡 Analysis:\n"
            f"• Safe EMI range: ₹{int(emi_limit):,}/month\n"
            f"• You should have at least 6 months emergency fund\n\n"
            f"👉 Recommendation:\n"
            f"Proceed only if EMI fits within limit and savings remain stable."
        )

    # 📱 BUY DECISION
    if "buy" in q:
        if savings <= 0:
            return (
                "❌ You currently have no savings.\n\n"
                "👉 Improve savings before making purchases."
            )

        if amt:
            ratio = amt / savings

            impact = (
                "High impact ❌" if ratio > 3 else
                "Moderate impact ⚠️" if ratio > 1 else
                "Low impact ✅"
            )

            decision = (
                "Avoid or delay purchase" if ratio > 3 else
                "Plan before buying" if ratio > 1 else
                "Safe to buy"
            )

            return (
                f"📊 Financial Evaluation:\n"
                f"• Item Cost: ₹{amt:,}\n"
                f"• Monthly Savings: ₹{int(savings):,}\n"
                f"• Cost-to-savings ratio: {round(ratio,2)}x\n\n"
                f"💡 Impact: {impact}\n\n"
                f"👉 Recommendation: {decision}"
            )

        return (
            f"📊 Your monthly savings: ₹{int(savings):,}\n"
            f"👉 Please provide item price for better advice."
        )

    # 📈 INVESTMENT
    if "invest" in q:
        return (
            f"📈 Investment Strategy:\n\n"
            f"• Monthly Savings: ₹{int(savings):,}\n\n"
            f"💡 Suggested Allocation:\n"
            f"• 50% Equity (growth)\n"
            f"• 30% Debt (stability)\n"
            f"• 20% Emergency fund\n\n"
            f"👉 Start SIP for long-term growth."
        )

    # 💰 SAVINGS
    if "save" in q or "savings" in q:
        return (
            f"💰 Savings Analysis:\n\n"
            f"• Monthly Savings: ₹{int(savings):,}\n"
            f"• Savings Rate: {int(savings_rate)}%\n\n"
            f"💡 Ideal: 20–30%\n\n"
            f"👉 {'Increase savings urgently' if savings_rate < 20 else 'You are doing well'}"
        )

    # 🏛️ TAX
    if "tax" in q:
        return (
            f"🏛️ Tax Analysis:\n\n"
            f"• Annual Income: ₹{income:,}\n"
            f"• Estimated Tax: ₹{tax_amount:,}\n\n"
            f"💡 Tips:\n"
            f"• Use 80C deductions\n"
            f"• Consider ELSS / PPF\n"
            f"• Health insurance (80D)"
        )

    # DEFAULT
    return (
        "🤖 I can help you with:\n"
        "• Buying decisions\n"
        "• Investment planning\n"
        "• Savings analysis\n"
        "• Tax advice\n\n"
        "👉 Try: 'Can I buy iPhone for 80000?'"
    )

# -------------------------
# EXECUTION
# -------------------------
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = smart_chat(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
# -------------------------
# PDF
# -------------------------
def generate_pdf(file_path):
    try:
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
        )
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import A4
        import matplotlib.pyplot as plt
        import os

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        # -------------------------
        # STYLES (PROFESSIONAL)
        # -------------------------
        title = ParagraphStyle(name="Title", fontSize=28, alignment=1, spaceAfter=30)
        subtitle = ParagraphStyle(name="Subtitle", fontSize=14, alignment=1, spaceAfter=20)
        heading = ParagraphStyle(name="Heading", fontSize=18, spaceAfter=12)
        body = ParagraphStyle(name="Body", fontSize=11, spaceAfter=10)

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

        health = (
            "Strong" if savings_rate > 20 else
            "Moderate" if savings_rate > 10 else
            "Weak"
        )

        content.append(Paragraph(
            f"This report evaluates your financial position based on income, expenses, and savings.\n\n"
            f"• Monthly Income: ₹{int(monthly_income):,}\n"
            f"• Monthly Expenses: ₹{int(monthly_expense):,}\n"
            f"• Monthly Savings: ₹{int(monthly_savings):,}\n\n"
            f"Your savings rate is <b>{int(savings_rate)}%</b>, indicating <b>{health}</b> financial health.",
            body
        ))

        # -------------------------
        # FINANCIAL SNAPSHOT TABLE
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Financial Snapshot", heading))

        table_data = [
            ["Metric", "Value"],
            ["Monthly Income", f"₹{int(monthly_income):,}"],
            ["Monthly Expenses", f"₹{int(monthly_expense):,}"],
            ["Monthly Savings", f"₹{int(monthly_savings):,}"],
            ["Savings Rate", f"{int(savings_rate)}%"],
            ["Annual Tax", f"₹{tax_amount:,}"]
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
        # EXPENSE CHART
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Expense Distribution", heading))

        fig, ax = plt.subplots()
        ax.pie(
            chart_data["Amount"],
            labels=chart_data["Category"],
            autopct='%1.1f%%'
        )

        chart_path = "expense_chart.png"
        plt.savefig(chart_path, bbox_inches='tight')
        plt.close()

        content.append(Image(chart_path, width=400, height=300))

        # -------------------------
        # TAX ANALYSIS
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Tax Analysis", heading))

        content.append(Paragraph(
            f"Based on your annual income, your estimated tax liability is "
            f"<b>₹{tax_amount:,}</b>. Consider using tax-saving instruments "
            f"such as ELSS, PPF, and insurance deductions.",
            body
        ))

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Strategic Recommendations", heading))

        if savings_rate < 20:
            content.append(Paragraph(
                "• Reduce discretionary expenses\n"
                "• Increase savings to at least 20%\n"
                "• Build emergency fund (6 months)\n"
                "• Start SIP investments",
                body
            ))
        else:
            content.append(Paragraph(
                "• Maintain strong savings discipline\n"
                "• Increase investment allocation\n"
                "• Diversify portfolio\n"
                "• Optimize tax planning",
                body
            ))

        # -------------------------
        # BUILD PDF
        # -------------------------
        doc.build(content)

        # Clean up chart file
        if os.path.exists(chart_path):
            os.remove(chart_path)

    except Exception as e:
        st.error(f"PDF error: {e}")
# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🚀 AI Finance Optimizer Pro")