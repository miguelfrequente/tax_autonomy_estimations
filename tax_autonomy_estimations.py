
import numpy as np
import matplotlib.pyplot as plt

class TaxCalculator:
    @staticmethod
    def calculate_german_income_tax(income: float) -> float:
        """
        German income tax calculation for 2025 using the official tax formula according to

        https://de.wikipedia.org/wiki/Einkommensteuer_(Deutschland)#

        Validity checked according to the 2022 curve with the 2022 values for E0, E1, E2 and E3.

        params:
            income: float, annual income in EUR    
        """

        # **Tax Brackets for 2025**
        E0 = 12097 # 10348 for 2022
        E1 = 17444 # 14927 for 2022
        E2 = 68481 # 58497 for 2022
        E3 = 277286 # 277826 for 2022

        # **Progression Zone Coefficients (official values)**
        sg1, p1 = 0.14, 998*1e-8
        sg2, p2 = 0.2397, 181.19*1e-8

        # **Proportional Tax Offsets (corrected)**
        sg3, C3 = 0.42, -10911
        sg4, C4 = 0.45, -19256.67

        # **Tax Calculation**
        if income <= E0:
            return 0  # No tax in the first zone

        elif E0 < income <= E1:
            # First progression zone (quadratic tax growth)
            return round(sg1 * (income - E0) + np.pow(income - E0,2)*p1, 2)

        elif E1 < income <= E2:
            # Compute tax at E1 (S1)
            S1 = sg1 * (E1 - E0) + np.pow(E1 - E0,2)*p1
            # Second progression zone
            return round(sg2 * (income - E1) + np.pow(income - E1,2)*p2 + S1, 2)

        elif E2 < income <= E3:
            # First proportional tax zone (linear tax with offset)
            return round(sg3*income - np.abs(C3), 2)

        else:  # income > E3
            # Highest proportional tax zone (linear tax with offset)
            return round(sg4 * income - np.abs(C4), 2)

    def calculate_german_social_security_tax(income: float) -> float:
        """
        German social security tax calculation for 2025 using the official tax formula according to

        params:
            income: float, annual income in EUR    
        """

        lower_tax_limit = 12097
        upper_tax_limit = 68481

        medical_insurance_rate = (0.146+0.036) / 2 # Only the employee part
        pension_insurance_rate = 0.186 / 2 # Only the employee part
        unemployment_insurance_rate = 0.026 / 2 # Only the employee part

        if income <= 0:
            return 0
        
        elif 0 < income <= lower_tax_limit:
            return 0
        
        elif lower_tax_limit < income <= upper_tax_limit:
            return income * (medical_insurance_rate + pension_insurance_rate + unemployment_insurance_rate)
        
        elif income > upper_tax_limit:
            return upper_tax_limit * (medical_insurance_rate + pension_insurance_rate + unemployment_insurance_rate)
        
    @staticmethod
    def print_results_income_tax(income:float) -> None:
        tax = TaxCalculator.calculate_german_income_tax(income)
        average_tax = tax / income
        print(f"Monthly income: {income} €. Absolute Tax to pay: {tax} €. Average tax rate: {average_tax*100:.2f}%")

    @staticmethod
    def validate_output_income_tax() -> None:
        TaxCalculator.print_results_income_tax(10e3) # For 2022 expected average tax rate: 0 %
        TaxCalculator.print_results_income_tax(20e3) # For 2022 expected aexiverage tax rate: 11 %
        TaxCalculator.print_results_income_tax(50e3) # For 2022 expected average tax rate: 23 %
        TaxCalculator.print_results_income_tax(80e3) # For 2022 expected average tax rate: 28 %
        TaxCalculator.print_results_income_tax(100e3) # For 2022 expected average tax rate: 32 %
        TaxCalculator.print_results_income_tax(200e3) # For 2022 expected average tax rate: 37 %

    @staticmethod
    def print_results_social_security_tax(income:float) -> None:
        tax = TaxCalculator.calculate_german_social_security_tax(income)
        average_tax = tax / income
        print(f"Monthly income: {income} €. Absolute Tax to pay: {tax} €. Average tax rate: {average_tax*100:.2f}%")

    def validate_output_social_security_tax() -> None:
        TaxCalculator.print_results_social_security_tax(10e3) # For 2022 expected average tax rate: 0 %
        TaxCalculator.print_results_social_security_tax(20e3) # For 2022 expected average tax rate: 19.7 %
        TaxCalculator.print_results_social_security_tax(50e3) # For 2022 expected average tax rate: 19.7 %
        TaxCalculator.print_results_social_security_tax(80e3) # For 2022 expected average tax rate: < 19.7 %
        TaxCalculator.print_results_social_security_tax(100e3) # For 2022 expected average tax rate: < 19.7 %




def calculate_compound_capital_growth(annual_capital_increase_capital: float, interest_rate:float, years: int, monthly_investment: bool) -> float:
    """
    Calculate the compound growth of a capital over 10 years with a given interest rate.

    params:
        annual_capita_increase_capital: float, initial capital in EUR
        interest_rate: float, annual interest rate in percent
        years: float, number of years to calculate the compound
    """
    total_capital = 0
    monthly_income = annual_capital_increase_capital / 12

    for _ in range(years):
        if monthly_investment:
            for _ in range(12):
                total_capital = total_capital * (1 + interest_rate / 12) + monthly_income
        else:
            total_capital = total_capital * (1 + interest_rate) + annual_capital_increase_capital

    return total_capital


def calculate_number_of_years(interest_rate_annual: float, interest_rate_low_risk: float, annual_income: float, annual_income_cap: float) -> float: 
    """
    Calculate the number of years to reach a sufficient capital to maintain annual net income from capital income.

    params:
        interest_rate_annual: float, annual interest rate for the capital growth phase (e.g. 20% would be 0.2)
        interest_rate_low_risk: float, annual interest rate for the time when the capital serves as passive income
        annual_income: float, annual income in EUR
        annual_income_cap: float, annual income in EUR that would represent "the maximum income needed" even if the current annual income is higher.
    """

    years = 0
    total_capital = 0

    income_tax = TaxCalculator.calculate_german_income_tax(annual_income)
    social_security_tax = TaxCalculator.calculate_german_social_security_tax(annual_income)
    annual_income_net = annual_income - income_tax - social_security_tax

    total_required_capital = annual_income_net / interest_rate_low_risk

    if annual_income > annual_income_cap:
        income_tax_cap = TaxCalculator.calculate_german_income_tax(annual_income_cap)
        social_security_tax_cap = TaxCalculator.calculate_german_social_security_tax(annual_income_cap)

        annual_income_net = annual_income_cap - income_tax_cap - social_security_tax_cap

        total_required_capital = annual_income_net / interest_rate_annual


    while total_capital < total_required_capital:
        total_capital = total_capital * (1 + interest_rate_annual) + income_tax
        years += 1

        if years > 50:
            break

    return years, total_required_capital

def create_plot_for_income_and_interest_rate():
    """
        Create a plot to show the number of years to reach a sufficient capital for different annual incomes and interest rates.
    """

    interest_rate_low_risk = 0.05
    
    interest_rates = np.linspace(0.05, 0.2, 4)
    annual_incomes = np.array([20e3,50e3,80e3,100e3,150e3,200e3,300e3])
    years_to_reach_capital = []

    print("I hang here")
    
    for interest_rate in interest_rates:
        for annual_income in annual_incomes:
            years, _ = calculate_number_of_years(interest_rate, interest_rate_low_risk, annual_income, 150e3)
            years_to_reach_capital.append(years)


        plt.plot(annual_incomes, np.array(years_to_reach_capital).copy(), marker="o")
        years_to_reach_capital = []

    plt.legend([f"Interest Rate: {interest_rate*100:.1f} %" for interest_rate in interest_rates])
    plt.xlabel("Annual Income in EUR")
    plt.ylabel("Years to reach sufficient capital")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    income = 150e3
    net_income = income - TaxCalculator.calculate_german_income_tax(income) - TaxCalculator.calculate_german_social_security_tax(income)
    print(net_income/12)
    
    
    #interest_rate = 0.15
    #interest_rate_low_risk = 0.05
    #annual_income = 100e3
    #annual_income_cap = 300e3

    #years, total_required_capital = calculate_number_of_years(interest_rate, interest_rate_low_risk, annual_income, annual_income_cap)
    #print(f"Years to reach capital growth: {years}")    
    #print(total_required_capital)

    #create_plot_for_income_and_interest_rate()
