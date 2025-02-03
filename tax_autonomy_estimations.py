
import numpy as np

annual_income = 100000
monthly_income = annual_income / 12

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

    @staticmethod
    def print_results(income:float) -> None:
        tax = TaxCalculator.calculate_german_income_tax(income)
        average_tax = tax / income
        print(f"Monthly income: {income} €. Absolute Tax to pay: {tax} €. Average tax rate: {average_tax*100:.2f}%")

    @staticmethod
    def validate_output() -> None:
        TaxCalculator.print_results(10e3) # For 2022 expected average tax rate: 0 %
        TaxCalculator.print_results(20e3) # For 2022 expected average tax rate: 11 %
        TaxCalculator.print_results(50e3) # For 2022 expected average tax rate: 23 %
        TaxCalculator.print_results(80e3) # For 2022 expected average tax rate: 28 %
        TaxCalculator.print_results(100e3) # For 2022 expected average tax rate: 32 %
        TaxCalculator.print_results(200e3) # For 2022 expected average tax rate: 37 %


if __name__ == "__main__":
    TaxCalculator.validate_output()