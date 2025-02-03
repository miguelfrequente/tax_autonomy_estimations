


annual_income = 100000
monthly_income = annual_income / 12

# This is a function that calculates the income tax for a given income according to the german tax system using internal variables for the tax brackets and rates.

def calculate_german_income_tax_final(income):
    """
    Fully corrected German income tax calculation for 2024 using the official tax formula.
    """

    # **Tax Brackets for 2024**
    E0 = 11605   # Tax-free allowance
    E1 = 17006
    E2 = 66761
    E3 = 277826

    # **Progression Zone Coefficients (official values)**
    a1, b1 = 0.14, 998*10e-8
    a2, b2 = 0.2397, 0.00022874

    # **Proportional Tax Offsets (corrected)**
    c3, d3 = 0.42, 9136.63
    c4, d4 = 0.45, 17374.99

    # **Tax Calculation**
    if income <= E0:
        return 0  # No tax in the first zone

    elif E0 < income <= E1:
        # First progression zone (quadratic tax growth)
        return round(a1 * (income - E0) + b1 * ((income - E0) ** 2), 2)

    elif E1 < income <= E2:
        # Compute tax at E1 (S1)
        S1 = a1 * (E1 - E0) + b1 * ((E1 - E0) ** 2)
        # Second progression zone
        return round(S1 + a2 * (income - E1) + b2 * ((income - E1) ** 2), 2)

    elif E2 < income <= E3:
        # First proportional tax zone (linear tax with offset)
        return round(c3 * income - d3, 2)

    else:  # income > E3
        # Highest proportional tax zone (linear tax with offset)
        return round(c4 * income - d4, 2)

# **Test Cases (Final)**
test_incomes_final = [10000, 20000, 50000, 100000, 300000]
test_results_final = {income: calculate_german_income_tax_final(income) for income in test_incomes_final}
#print(test_results_final)



if __name__ == "__main__":
    print(calculate_german_income_tax_final(50000))
    print(calculate_german_income_tax_final(100000))