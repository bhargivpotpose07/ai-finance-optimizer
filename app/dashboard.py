import sys, os
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
h1, h2, h3 { color: #e2e8f0; }
.stMetric { background-color: #1e293b; padding: 15px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("💰 AI Financial Optimizer")
st.caption("AI + Government Policy Based Financial System")
st.markdown("""
### 💡 What this app does
- Analyze your income & expenses  
- Apply government tax logic  
- Suggest investment strategy  
- Generate professional report  
""")
# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("⚙️ Financial Inputs")

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
if monthly_savings < 0:
    st.error("You are overspending. Reduce expenses.")


# -------------------------
# POLICY ENGINE
# -------------------------
policy = apply_policies(income, monthly_savings)

# -------------------------
# METRICS
# -------------------------
st.subheader("📊 Financial Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Expense", f"₹{int(monthly_expense):,}")
col2.metric("Savings", f"₹{int(monthly_savings):,}")
col3.metric("Savings %", f"{int(savings_rate)}%")
col4.metric("Risk", policy["risk_profile"])

# -------------------------
# CHARTS
# -------------------------
st.subheader("📈 Expense Breakdown")

chart_data = pd.DataFrame({
    "Category": ["Rent", "Food", "Shopping", "Entertainment"],
    "Amount": [rent, food, shopping, entertainment]
})

st.bar_chart(chart_data.set_index("Category"))

fig, ax = plt.subplots()
ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
st.pyplot(fig)

# -------------------------
# AI INSIGHTS
# -------------------------
st.subheader("🧠 Insights")

if savings_rate < 10:
    st.error("Low savings → high financial risk")
elif savings_rate < 20:
    st.warning("Moderate savings → improve discipline")
else:
    st.success("Strong financial health")

# -------------------------
# POLICY DISPLAY
# -------------------------
st.subheader("🏛️ Policy Intelligence")

col1, col2 = st.columns(2)

col1.metric("Recommended Regime", policy["better_regime"])
col2.metric("Risk Profile", policy["risk_profile"])

st.write(f"New Tax: ₹{policy['new_tax']}")
st.write(f"Old Tax: ₹{policy['old_tax']}")

st.write("### Investment Allocation")
for k, v in policy["allocation"].items():
    st.write(f"{k}: {v}")

# -------------------------
# WEALTH PROJECTION
# -------------------------
st.subheader("📈 Wealth Projection")

years = st.slider("Years", 1, 15, 5)
future_value = max(monthly_savings, 0) * 12 * years * 1.12

st.metric("Projected Wealth", f"₹{int(future_value)}")

# -------------------------
# CSV DOWNLOAD
# -------------------------
st.subheader("📥 Download CSV")

csv = chart_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="financial_report.csv",
    mime="text/csv"
)

# -------------------------
# PDF REPORT FUNCTION
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

        # Styles
        title = ParagraphStyle(name="Title", fontSize=24, alignment=1, spaceAfter=20)
        heading = ParagraphStyle(name="Heading", fontSize=16, spaceAfter=10)
        body = ParagraphStyle(name="Body", fontSize=11, spaceAfter=8)

        content = []

        # Cover Page
        content.append(Spacer(1, 250))
        content.append(Paragraph("AI FINANCE SYSTEM", title))
        content.append(Paragraph("Financial Optimization Report", heading))
        content.append(Paragraph(datetime.now().strftime("%d %B %Y"), body))
        content.append(PageBreak())

        # Summary
        content.append(Paragraph("Executive Summary", heading))
        content.append(Paragraph(f"Savings Rate: {int(savings_rate)}%", body))

        # Table
        table_data = [
            ["Metric", "Value"],
            ["Income", f"₹{int(monthly_income)}"],
            ["Expense", f"₹{int(monthly_expense)}"],
            ["Savings", f"₹{int(monthly_savings)}"]
        ]

        table = Table(table_data)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.black),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey)
        ]))

        content.append(table)

        # Chart
        fig, ax = plt.subplots()
        ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
        chart_path = "chart.png"
        plt.savefig(chart_path)
        plt.close()

        content.append(Paragraph("Expense Distribution", heading))
        content.append(Image(chart_path, width=400, height=300))

        # Policy Section
        content.append(Paragraph("Policy Insights", heading))
        content.append(Paragraph(f"Recommended Regime: {policy['better_regime']}", body))
        content.append(Paragraph(f"Risk Profile: {policy['risk_profile']}", body))

        for k, v in policy["allocation"].items():
            content.append(Paragraph(f"{k}: {v}", body))

        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")

# -------------------------
# PDF BUTTON
# -------------------------
st.subheader("📄 Professional Report")

if st.button("Generate PDF Report"):
    generate_pdf("report.pdf")

    if os.path.exists("report.pdf"):
        with open("report.pdf", "rb") as f:
            st.download_button(
                "📥 Download PDF",
                f,
                "AI_Finance_Report.pdf",
                "application/pdf"
            )