def tax_new_regime(income):
    if income <= 1200000:
        return 0
    elif income <= 1500000:
        return int(income * 0.1)
    else:
        return int(income * 0.2)


def tax_old_regime(income):
    if income <= 250000:
        return 0
    elif income <= 500000:
        return int(income * 0.05)
    elif income <= 1000000:
        return int(income * 0.2)
    else:
        return int(income * 0.3)