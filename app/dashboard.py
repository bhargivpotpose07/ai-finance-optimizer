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
# -------------------------
# 💬 AI CHATBOT (FINAL FIX)
# -------------------------
st.subheader("💬 AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

# DISPLAY OLD MESSAGES
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# INPUT BOX
user_input = st.chat_input("Ask: Can I buy iPhone for 80000?")

# CHAT LOGIC
def smart_chat(q):
    q = q.lower()
    nums = re.findall(r'\d+', q)
    amt = int(nums[0]) if nums else None

    if "milk" in q or "food" in q:
        return f"🛒 Essential expense. With ₹{int(monthly_savings):,} savings, safe to buy."

    if "buy" in q:
        if monthly_savings <= 0:
            return "❌ You have no savings currently."

        if amt:
            if amt > monthly_savings * 3:
                return f"⚠️ ₹{amt:,} is too expensive vs savings ₹{int(monthly_savings):,}."
            elif amt < monthly_savings:
                return f"✅ ₹{amt:,} is affordable."
            else:
                return "⚠️ This will impact your savings significantly."

        return f"📊 Your savings ₹{int(monthly_savings):,}. Evaluate purchase."

    if "house" in q:
        return f"🏡 Income ₹{int(monthly_income):,}, savings ₹{int(monthly_savings):,}. Plan EMI carefully."

    if "tax" in q:
        return f"🏛️ Estimated tax ₹{tax_amount:,}"

    if "invest" in q:
        return "📈 Invest: Equity + Debt + Emergency fund"

    return "🤖 Ask about buying, tax, saving, investing."

# EXECUTION
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    reply = smart_chat(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)
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

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        title = ParagraphStyle(name="Title", fontSize=28, alignment=1, spaceAfter=30)
        heading = ParagraphStyle(name="Heading", fontSize=18, spaceAfter=12)
        body = ParagraphStyle(name="Body", fontSize=11, spaceAfter=10)

        content = []

        # COVER
        content.append(Spacer(1, 200))
        content.append(Paragraph("AI FINANCE REPORT", title))
        content.append(Paragraph(datetime.now().strftime("%d %B %Y"), body))
        content.append(PageBreak())

        # SUMMARY
        content.append(Paragraph("Executive Summary", heading))
        content.append(Paragraph(
            f"Income ₹{int(monthly_income):,}, Expenses ₹{int(monthly_expense):,}, Savings ₹{int(monthly_savings):,}.",
            body
        ))

        # TABLE
        table_data = [
            ["Metric", "Value"],
            ["Income", f"₹{int(monthly_income):,}"],
            ["Expenses", f"₹{int(monthly_expense):,}"],
            ["Savings", f"₹{int(monthly_savings):,}"],
            ["Tax", f"₹{tax_amount:,}"]
        ]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.black),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
        ]))

        content.append(table)

        # CHART
        fig, ax = plt.subplots()
        ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
        chart_path = "chart.png"
        plt.savefig(chart_path)
        plt.close()

        content.append(Spacer(1, 20))
        content.append(Paragraph("Expense Distribution", heading))
        content.append(Image(chart_path, width=400, height=300))

        # RECOMMENDATION
        content.append(Spacer(1, 20))
        content.append(Paragraph("Recommendations", heading))

        if savings_rate < 20:
            content.append(Paragraph("Increase savings and reduce expenses.", body))
        else:
            content.append(Paragraph("Maintain discipline and invest.", body))

        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")

        st.subheader("📄 Generate Report")

if st.button("📄 Generate Big4 Report"):
    generate_pdf("report.pdf")

    if os.path.exists("report.pdf"):
        with open("report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, "AI_Finance_Report.pdf")
# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("🚀 AI Finance Optimizer Pro")