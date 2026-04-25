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
h1 { color: #f8fafc; font-weight: 700; }
h2, h3 { color: #cbd5f5; }

[data-testid="stMetric"] {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.stButton>button {
    background-color: #3b82f6;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
}

p, span { color: #e2e8f0; }
hr { border: 1px solid #334155; }
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.title("💰 AI Financial Optimizer")
st.markdown("### 💡 Smart Financial Advisor — Make smarter decisions instantly")

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
    st.error("⚠️ You are overspending. Reduce expenses.")

# -------------------------
# POLICY ENGINE
# -------------------------
policy = apply_policies(income, monthly_savings)

# -------------------------
# METRICS
# -------------------------
st.subheader("📊 Financial Overview")

c1, c2, c3, c4 = st.columns(4)
c1.metric("💸 Expenses", f"₹{int(monthly_expense):,}")
c2.metric("💰 Savings", f"₹{int(monthly_savings):,}")
c3.metric("📈 Savings %", f"{int(savings_rate)}%")
c4.metric("🧠 Risk", policy["risk_profile"])

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
ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%', textprops={'color': "white"})
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#0f172a')
st.pyplot(fig)

# -------------------------
# INSIGHTS
# -------------------------
st.subheader("🧠 Insights")

if savings_rate < 10:
    st.error("⚠️ Critical: Very low savings.")
elif savings_rate < 20:
    st.warning("⚠️ Moderate: Improve savings.")
else:
    st.success("✅ Strong financial health.")

# -------------------------
# POLICY
# -------------------------
st.subheader("🏛️ Policy Recommendations")

st.info(f"Recommended Tax Regime: {policy['better_regime']}")

c1, c2 = st.columns(2)
c1.metric("New Tax", f"₹{policy['new_tax']:,}")
c2.metric("Old Tax", f"₹{policy['old_tax']:,}")

st.markdown("### 📊 Investment Strategy")
for k, v in policy["allocation"].items():
    st.write(f"**{k}:** {v}")

# -------------------------
# WEALTH PROJECTION
# -------------------------
st.subheader("📈 Wealth Projection")

years = st.slider("Years", 1, 15, 5)
future_value = max(monthly_savings, 0) * 12 * years * 1.12
st.metric("Projected Wealth", f"₹{int(future_value):,}")

# -------------------------
# CSV DOWNLOAD
# -------------------------
st.subheader("📥 Download Data")
csv = chart_data.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV Report", csv, "financial_report.csv")

# -------------------------
#def generate_pdf(file_path):
    try:
        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
        )
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.pagesizes import A4

        doc = SimpleDocTemplate(file_path, pagesize=A4)

        # -------------------------
        # STYLES
        # -------------------------
        title = ParagraphStyle(name="Title", fontSize=28, alignment=1, spaceAfter=30)
        subtitle = ParagraphStyle(name="Subtitle", fontSize=16, alignment=1, spaceAfter=20)
        heading = ParagraphStyle(name="Heading", fontSize=18, spaceAfter=12)
        body = ParagraphStyle(name="Body", fontSize=11, spaceAfter=10)

        content = []

        # -------------------------
        # COVER PAGE
        # -------------------------
        content.append(Spacer(1, 200))
        content.append(Paragraph("AI FINANCE REPORT", title))
        content.append(Paragraph("Financial Optimization System", subtitle))
        content.append(Paragraph(datetime.now().strftime("%d %B %Y"), body))
        content.append(PageBreak())

        # -------------------------
        # EXECUTIVE SUMMARY
        # -------------------------
        content.append(Paragraph("Executive Summary", heading))

        content.append(Paragraph(
            f"This report analyzes your financial health based on income, expenses, and savings behavior.",
            body
        ))

        content.append(Paragraph(
            f"Your current savings rate is <b>{int(savings_rate)}%</b>, "
            f"indicating {'strong' if savings_rate > 20 else 'moderate' if savings_rate > 10 else 'low'} financial health.",
            body
        ))

        # -------------------------
        # TABLE
        # -------------------------
        table_data = [
            ["Metric", "Value"],
            ["Monthly Income", f"₹{int(monthly_income):,}"],
            ["Monthly Expense", f"₹{int(monthly_expense):,}"],
            ["Monthly Savings", f"₹{int(monthly_savings):,}"]
        ]

        table = Table(table_data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#1e293b")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke)
        ]))

        content.append(table)
        content.append(Spacer(1, 20))

        # -------------------------
        # CHART
        # -------------------------
        fig, ax = plt.subplots()
        ax.pie(chart_data["Amount"], labels=chart_data["Category"], autopct='%1.1f%%')
        chart_path = "chart.png"
        plt.savefig(chart_path)
        plt.close()

        content.append(Paragraph("Expense Distribution", heading))
        content.append(Image(chart_path, width=400, height=300))

        # -------------------------
        # POLICY SECTION
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Policy Insights", heading))

        content.append(Paragraph(
            f"Recommended Tax Regime: <b>{policy['better_regime']}</b>", body
        ))

        content.append(Paragraph(
            f"Risk Profile: <b>{policy['risk_profile']}</b>", body
        ))

        content.append(Spacer(1, 10))

        for k, v in policy["allocation"].items():
            content.append(Paragraph(f"{k}: {v}", body))

        # -------------------------
        # RECOMMENDATIONS
        # -------------------------
        content.append(Spacer(1, 20))
        content.append(Paragraph("Recommendations", heading))

        if savings_rate < 20:
            content.append(Paragraph(
                "Increase savings by reducing discretionary expenses and improving budgeting.",
                body
            ))
        else:
            content.append(Paragraph(
                "Maintain your current financial discipline and consider long-term investments.",
                body
            ))

        content.append(Paragraph(
            "Ensure you maintain an emergency fund of at least 6 months of expenses.",
            body
        ))

        doc.build(content)

    except Exception as e:
        st.error(f"PDF error: {e}")
# -------------------------
# 💬 SMART CHATBOT (FINAL)
# -------------------------
st.subheader("💬 AI Financial Advisor")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask: Can I buy iPhone for 80000?")

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
        return f"🛒 This is essential. Your savings: ₹{int(savings):,}. This will not impact your finances."

    # MEDIUM PURCHASE
    if any(x in q for x in ["phone","iphone","laptop","bike"]):
        if savings <= 0:
            return f"❌ You have ₹{int(savings):,} savings. Avoid this purchase."

        if amt:
            if amt > savings * 3:
                return f"⚠️ Cost ₹{amt:,} is too high vs savings ₹{int(savings):,}."
            elif amt < savings:
                return f"✅ Affordable. Cost ₹{amt:,}, savings ₹{int(savings):,}."
            else:
                return f"⚠️ It will impact savings significantly."

        return f"📱 Your savings ₹{int(savings):,}. Evaluate before buying."

    # BIG PURCHASE
    if any(x in q for x in ["house","home","car"]):
        return (
            f"🏡 Big decision.\n\n"
            f"Income: ₹{int(income_val):,}/month\n"
            f"Savings: ₹{int(savings):,}/month\n\n"
            f"Ensure EMI < 30–40% income and emergency fund."
        )

    # INVEST
    if "invest" in q:
        return f"📈 Risk profile: {policy['risk_profile']}. Invest accordingly."

    # SAVE
    if "save" in q:
        return f"💰 Savings rate: {int(savings_rate)}%. Aim for 20–30%."

    # TAX
    if "tax" in q:
        return f"🏛️ {policy['better_regime']} regime saves more tax."

    return "🤖 Ask about buying, investing, savings, or tax."

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