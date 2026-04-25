# utils/policy_engine.py

def apply_policies(income, monthly_savings):
    """
    Simplified Indian policy engine (2026–27 style).
    Returns tax comparison, best regime, risk profile, and allocation.
    """

    # ---------- TAX (SIMPLIFIED) ----------
    def new_tax(income):
        if income <= 1200000:
            return 0
        elif income <= 1500000:
            return (income - 1200000) * 0.10
        else:
            return (300000 * 0.10) + (income - 1500000) * 0.20

    def old_tax(income):
        tax = 0
        if income > 250000:
            tax += min(income - 250000, 250000) * 0.05
        if income > 500000:
            tax += min(income - 500000, 500000) * 0.20
        if income > 1000000:
            tax += (income - 1000000) * 0.30
        return tax

    new_regime_tax = new_tax(income)
    old_regime_tax = old_tax(income)

    # ---------- SAVINGS RATE ----------
    monthly_income = income / 12 if income else 0
    savings_rate = (monthly_savings / monthly_income) * 100 if monthly_income else 0

    # ---------- RISK PROFILE ----------
    if savings_rate > 25:
        risk = "High Growth"
        allocation = {"Equity": "60%", "Debt": "25%", "Emergency": "15%"}
    elif savings_rate > 10:
        risk = "Balanced"
        allocation = {"Equity": "40%", "Debt": "40%", "Emergency": "20%"}
    else:
        risk = "Conservative"
        allocation = {"Equity": "20%", "Debt": "50%", "Emergency": "30%"}

    return {
        "new_tax": int(new_regime_tax),
        "old_tax": int(old_regime_tax),
        "better_regime": "New" if new_regime_tax < old_regime_tax else "Old",
        "risk_profile": risk,
        "allocation": allocation,
        "savings_rate": int(savings_rate)
    }