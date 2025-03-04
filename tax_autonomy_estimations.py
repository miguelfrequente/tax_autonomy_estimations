
import numpy as np
import matplotlib.pyplot as plt
import sys

import logging


class IncomeDistribution:
    """
    This class contains the annual income distributions for Germany in 2025 and US in 2025.
    The income distribution in Germany based on data from https://www.iwkoeln.de/presse/interaktive-grafiken/judith-niehues-maximilian-stockhausen-einkommensverteilung-in-deutschland.html
    which was digitalized using a plot digitalizer. Further it was transformed from monthly net income to annual pretax income using the official German tax formulas for 2025 and the assumption 
    that everybody has the same tax-class, i.e. does not receive particular tax benefits due to kids or mariage status.

    The income distribution in the US was taken from https://en.wikipedia.org/wiki/Personal_income_in_the_United_States
    """

    income_distribution_germany_monthly_net_2025 =  [
                    [254, 0.018142335],
                    [507, 0.0368473],
                    [745, 0.05746718],
                    [999, 0.074790248],
                    [1253, 0.086605468],
                    [1498, 0.094857368],
                    [1752, 0.09815418],
                    [1998, 0.095133748],
                    [2251, 0.083585036],
                    [2497, 0.06955878],
                    [2751, 0.055818774],
                    [2997, 0.043717303],
                    [3250, 0.033264238],
                    [3496, 0.025298588],
                    [3750, 0.019800612],
                    [4003, 0.015951041],
                    [4249, 0.012920738],
                    [4503, 0.009623927],
                    [4749, 0.007146382],
                    [5002, 0.005497977],
                    [5248, 0.004402329],
                    [5502, 0.003849571],
                    [5755, 0.00412595],
                    [6001, 0.005497977],
                    [6247, 0.006327115],
                    [6501, 0.007422762],
                    [6754, 0.007699141],
                    [7000, 0.0165038]]
    
    # Values given in EUR for 2025
    income_distribution_germany_annual_pretax_2025 = [[3048.0, 0.018142335], 
                                                      [6084.0, 0.0368473], 
                                                      [8940.0, 0.05746718], 
                                                      [11988.0, 0.074790248],
                                                      [21408.6796875, 0.086605468],
                                                      [26297.890020525545, 0.094857368],
                                                      [32402.37806481606, 0.09815418],
                                                      [38404.916015625, 0.095133748],
                                                      [44456.68841170119, 0.083585036],
                                                      [51254.11145067215, 0.06955878],
                                                      [58019.106321155494, 0.055818774],
                                                      [65692.49251496955, 0.043717303],
                                                      [71238.10499621322, 0.033264238],
                                                      [76630.28155900352, 0.025298588],
                                                      [82197.8134571691, 0.019800612],
                                                      [86562.43176269531, 0.015951041],
                                                      [91882.03161621094, 0.012920738],
                                                      [97374.62658691406, 0.009623927],
                                                      [102694.22644042969, 0.007146382],
                                                      [108165.19702148438, 0.005497977],
                                                      [113484.796875, 0.004402329],
                                                      [118977.39184570312, 0.003849571],
                                                      [124448.36242675781, 0.00412595],
                                                      [129767.96228027344, 0.005497977],
                                                      [133547.9080920462, 0.006327115],
                                                      [138977.90147373016, 0.007422762],
                                                      [144386.51692871458, 0.007699141],
                                                      [149645.4868968022, 0.0165038]]
    
    # Values given in USD for 2022
    income_distribution_us_annual_pretax_2022 = [[1250.0, 13240.0],
                                                [3749.5, 5285000.0],
                                                [6249.5, 5411000.0],
                                                [8749.5, 5490000.0],
                                                [11249.5, 9765000.0],
                                                [13749.5, 6906000.0],
                                                [16249.5, 9029000.0],
                                                [18749.5, 6320000.0],
                                                [21249.5, 9624000.0],
                                                [23749.5, 6241000.0],
                                                [26249.5, 8413000.0],
                                                [28749.5, 5158000.0],
                                                [31249.5, 10380000.0],
                                                [33749.5, 4575000.0],
                                                [36249.5, 7769000.0],
                                                [38749.5, 4304000.0],
                                                [41249.5, 8576000.0],
                                                [43749.5, 3214000.0],
                                                [46249.5, 6357000.0],
                                                [48749.5, 3875000.0],
                                                [51249.5, 8743000.0],
                                                [53749.5, 3185000.0],
                                                [56249.5, 5339000.0],
                                                [58749.5, 2513000.0],
                                                [61249.5, 7021000.0],
                                                [63749.5, 2284000.0],
                                                [66249.5, 4088000.0],
                                                [68749.5, 1974000.0],
                                                [71249.5, 5002000.0],
                                                [73749.5, 1706000.0],
                                                [76249.5, 3715000.0],
                                                [78749.5, 1795000.0],
                                                [81249.5, 3899000.0],
                                                [83749.5, 1502000.0],
                                                [86249.5, 2552000.0],
                                                [88749.5, 1218000.0],
                                                [91249.5, 2660000.0],
                                                [93749.5, 1068000.0],
                                                [96249.5, 1914000.0],
                                                [98749.5, 998000.0],
                                                [125000.0, 19674000.0],
                                                [175000.0, 7765000.0],
                                                [225000.0, 3336000.0],
                                                [250000.0, 5238000.0]
                                            ]
                                                
    def check_sum_probability(distribution: list) -> None:
        """
        This function checks if the sum of the frequences in the income distribution is 1.

        params:
            distribution: list, list of income values and their probabilities
        """

        total_probability = sum([x[1] for x in distribution])
        if round(total_probability,1)-1.0 > 1e-6:
            raise Warning("Income distribution does not sum up to 1, it is {:.3f}".format(total_probability))

    def cutoff_income_distribution(income_distribution: list, cutoff: float) -> list:
        """
        Cut the income distribution at a certain cutoff value, i.e. removes all incomes that are lower than the cutoff value parameter.

        params:
            income_distribution: list, list of income values and their probabilities
            cutoff: float, cutoff value in EUR
        """
        return [[income, percentage] for income, percentage in income_distribution if income >= cutoff]

    def transform_distrubtion_to_annual_income() -> list:
        """
        Transform the monthly net income distribution to annual pretax income distribution for Germany in 2025.
        It uses the official German tax formulas for 2025 to calculate the annual pretax income and an adjusted binary search to find the correct value.

        returns:
            income_distribution_germany_annual_pretax_2025: list, list of annual pretax income values and their probabilities                    
        """

        income_distribution_germany_annual_pretax_2025 = []

        for income_monthly_net,percentage in IncomeDistribution.income_distribution_germany_monthly_net_2025:
            logging.debug(f"Now processing income: {income_monthly_net}")

            income_annual_net = income_monthly_net * 12

            income_annual_delta = 0
            income_annual_pretax_estimation = 0
            epsilon_threshold = 0.01
            epsilon = 1
            multiplicator = 2

            while np.abs(epsilon) > epsilon_threshold:
                income_annual_pretax_estimation = income_annual_net*multiplicator

                income_annual_posttax_estimation = income_annual_pretax_estimation - TaxCalculator.calculate_german_income_tax(income_annual_pretax_estimation) - TaxCalculator.calculate_german_social_security_tax(income_annual_pretax_estimation)

                income_annual_delta = income_annual_posttax_estimation-income_annual_net

                
                if income_annual_delta > 0:
                    multiplicator = multiplicator - multiplicator/2
                elif income_annual_delta < 0:
                    multiplicator = multiplicator + multiplicator/2

                epsilon = income_annual_delta / income_annual_net
    
            logging.debug("Income net in EUR : " + str(income_annual_net) + " Income pre tax in EUR: " + str(int(income_annual_pretax_estimation)))
            logging.debug("Monthly Income post tax in EUR: " + str(int(TaxCalculator.calculcate_post_tax_income(income_annual_pretax_estimation)/12)))

            income_distribution_germany_annual_pretax_2025.append([income_annual_pretax_estimation,percentage])

        return income_distribution_germany_annual_pretax_2025
    
    def plot_income_distribution_as_bar_chart(income_distribution: list, figure_name = "") -> None:
        """
        Plots the income distribution as a bar chart.

        params:
            income_distribution: list, list of income values and their probabilities
            figure_name: str, name of the figure to save the plot
        """
        income_values = [x[0] for x in income_distribution]
        income_probabilities = [x[1]*100 for x in income_distribution]

        bin_width = (income_values[1] - income_values[0])*0.8

        plt.bar(income_values, income_probabilities, width=bin_width, edgecolor="black", alpha = 0.7)
        plt.xlabel("Annual Pretax Income in EUR")
        plt.ylabel("Part of Population [%]")
        plt.grid()
        if figure_name != "":
            plt.savefig(figure_name)
        plt.show()
    


class TaxCalculator:
    """
    This class allows to calculate the German income tax and social security tax for 2025 for a given annual income.

    The formulas and values are taken from https://de.wikipedia.org/wiki/Einkommensteuer_(Deutschland)#
    """

    # Tax Brackets for 2025
    E0 = 12097 # 10348 for 2022
    E1 = 17444 # 14927 for 2022
    E2 = 68481 # 58497 for 2022
    E3 = 277286 # 277826 for 2022

    # Progression Zone Coefficients (official values)
    sg1, p1 = 0.14, 998*1e-8
    sg2, p2 = 0.2397, 181.19*1e-8

    # Proportional Tax Offsets (corrected)
    sg3, C3 = 0.42, -10911
    sg4, C4 = 0.45, -19256.67

    @staticmethod
    def calculate_german_income_tax(income: float) -> float:
        """
        German income tax calculation for 2025 using the official tax formula according to
        https://de.wikipedia.org/wiki/Einkommensteuer_(Deutschland)#

        Validity checked according to the 2022 curve with the 2022 values for E0, E1, E2 and E3.

        params:
            income: float, annual income in EUR

        returns:
            tax: float, annual income tax in EUR
        """

        E0 = TaxCalculator.E0
        E1 = TaxCalculator.E1
        E2 = TaxCalculator.E2
        E3 = TaxCalculator.E3

        sg1, p1 = TaxCalculator.sg1, TaxCalculator.p1
        sg2, p2 = TaxCalculator.sg2, TaxCalculator.p2

        sg3, C3 = TaxCalculator.sg3, TaxCalculator.C3
        sg4, C4 = TaxCalculator.sg4, TaxCalculator.C4

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
        German social security tax calculation for 2025 using the official tax formula.
        In does not take into account different tax classes or other tax benefits.

        params:
            income: float, annual income in EUR    

        returns:
            tax: float, annual social security tax in EUR
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
        """
        Print the results of the income tax calculation for a given annual income.

        Used to validate manually the tax calculation.

        params:
            income: float, annual income in EUR
        """


        tax = TaxCalculator.calculate_german_income_tax(income)
        average_tax = tax / income
        print(f"Monthly income: {income} €. Absolute Tax to pay: {tax} €. Average tax rate: {average_tax*100:.2f}%")

    @staticmethod
    def validate_output_income_tax() -> None:
        """
        Validate the output of the income tax calculation for different annual incomes by comparing it to the expected average tax rate.

        Comparison values taken from:
            https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/ESt_D_Splittingtarif_2022_zvE_bis_150000.svg/2880px-ESt_D_Splittingtarif_2022_zvE_bis_150000.svg.png
        """

        TaxCalculator.print_results_income_tax(10e3) # For 2022 expected average tax rate: 0 %
        TaxCalculator.print_results_income_tax(20e3) # For 2022 expected aexiverage tax rate: 11 %
        TaxCalculator.print_results_income_tax(50e3) # For 2022 expected average tax rate: 23 %
        TaxCalculator.print_results_income_tax(80e3) # For 2022 expected average tax rate: 28 %
        TaxCalculator.print_results_income_tax(100e3) # For 2022 expected average tax rate: 32 %
        TaxCalculator.print_results_income_tax(200e3) # For 2022 expected average tax rate: 37 %

    @staticmethod
    def print_results_social_security_tax(income:float) -> None:
        """
        Prints the results of the social security tax calculation for a given annual income.

        Used to validate manually the tax calculation.
        """
        tax = TaxCalculator.calculate_german_social_security_tax(income)
        average_tax = tax / income
        print(f"Monthly income: {income} €. Absolute Tax to pay: {tax} €. Average tax rate: {average_tax*100:.2f}%")

    def validate_output_social_security_tax() -> None:
        """
        Validate the output of the social security tax calculation for different annual incomes by comparing it to the expected average tax rate.
        """

        TaxCalculator.print_results_social_security_tax(10e3) # For 2022 expected average tax rate: 0 %
        TaxCalculator.print_results_social_security_tax(20e3) # For 2022 expected average tax rate: 19.7 %
        TaxCalculator.print_results_social_security_tax(50e3) # For 2022 expected average tax rate: 19.7 %
        TaxCalculator.print_results_social_security_tax(80e3) # For 2022 expected average tax rate: < 19.7 %
        TaxCalculator.print_results_social_security_tax(100e3) # For 2022 expected average tax rate: < 19.7 %

    def calculcate_post_tax_income(income: float) -> float:
        """
        Calculate the post tax income for a given annual income.

        params:
            income: float, annual income in EUR
        returns:
            post_tax_income: float, annual post tax income in EUR
        """

        return income - TaxCalculator.calculate_german_income_tax(income) - TaxCalculator.calculate_german_social_security_tax(income)



def calculate_compound_capital_growth(annual_capital_increase_capital: float, interest_rate:float, years: int, monthly_investment: bool) -> float:
    """
    Calculate the compound growth of a capital over the given number of years.

    params:
        annual_capita_increase_capital: float, initial capital in EUR
        interest_rate: float, annual interest rate in percent
        years: float, number of years to calculate the compound
        monthly_investment: bool, if True, monthly investment is considered, otherwise only the annual capital increase is considered
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


def calculate_number_of_years(interest_rate_annual: float, interest_rate_low_risk: float, annual_income: float, annual_income_cap: float, income_support: float = 0.0) -> float: 
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

    if annual_income >= annual_income_cap:
        income_tax_cap = TaxCalculator.calculate_german_income_tax(annual_income_cap)
        social_security_tax_cap = TaxCalculator.calculate_german_social_security_tax(annual_income_cap)

        annual_income_net = annual_income_cap - income_tax_cap - social_security_tax_cap

        total_required_capital = annual_income_net / interest_rate_low_risk

    while total_capital < total_required_capital:
        total_capital = total_capital * (1 + interest_rate_annual) + income_tax + income_support
        years += 1

        if years > 100:
            break

    logging.debug("Annual income: " + str(annual_income))
    logging.debug("Annual income net: " + str(annual_income_net))
    logging.debug("Income tax: " + str(income_tax))
    logging.debug("Income support: " + str(income_support))
    logging.debug("Total required capital: " + str(total_required_capital))
    logging.debug("Total capital: " + str(total_capital))
    logging.debug(" Years: " + str(years))

    return years, total_required_capital


def create_plot_for_income_and_interest_rate(income_distribution: list, interest_rate_low_risk: float = 0.05, interest_rates: list = [0.03, 0.07, 0.14, 0.2],
                                             annual_income_cap: float = 500e3, 
                                             number_of_citizens: float = 1, economy_subsidy:float = 0, 
                                             save_plot_to_disk: bool = False) -> None:
    """
    Create a plot to show the number of years to reach a sufficient capital for different annual incomes and interest rates.

    Depending on the parameters, either redistribution effects (if the annual_income_cap is lower than the maximum annual income in the income distribution) are considered
    and additional income support through the use of profits from the economy (through the economy_subsidy parameter) are be considered.

    They are added as an income support for capital build-up for the income brackets below the annual_income_cap.

    params:
        income_distribution: list, list of annual income values and their probabilities
        interest_rate_low_risk: float, assumed annual interest rate for the time when the capital serves as passive income
        interest_rates: list of assumed annual interest rates for the capital growth phase

        annual_income_cap: float, annual income in EUR that would represent "the maximum income needed" even if the current annual income is higher. 

        number_of_citizens: float, number of citizens in the country - used to compute the additional income subsidy through profits of the companies in a country.
        economy_subsidy: float, additional income subsidy through economic profits in EUR

        save_plot_to_disk: bool, if True, the plot is saved to the disk
    """     


    IncomeDistribution.check_sum_probability(income_distribution)
   
    income_support_per_income_bracket,_ = calculate_income_support(income_distribution, annual_income_cap, number_of_citizens, economy_subsidy)

    logging.debug("Annual income cap: " + str(annual_income_cap))
    logging.debug("Income distribution:")
    logging.debug(income_distribution)
    logging.debug("Income support per income bracket:")
    logging.debug(income_support_per_income_bracket)
  

    annual_incomes = [x[0] for x in income_distribution]
    
    years_to_reach_capital = []
    years_to_reach_capital_no_support = []
    
    for interest_rate in interest_rates:
        logging.debug("Running for nterest rate: " + str(interest_rate))

        for annual_income, income_support in zip(annual_incomes, income_support_per_income_bracket):

            years, _ = calculate_number_of_years(interest_rate, interest_rate_low_risk, annual_income, annual_income_cap, income_support)
            years_to_reach_capital.append(years)

            years_no_support, _ = calculate_number_of_years(interest_rate, interest_rate_low_risk, annual_income, annual_income_cap, 0)
            years_to_reach_capital_no_support.append(years_no_support)

            logging.debug(" Annual income: " + str(annual_income) + " - Year reduction with support: " + str(years_no_support - years))

        #line_temp, = plt.plot(annual_incomes, np.array(years_to_reach_capital_no_support).copy(), marker="o")

        line_temp, = plt.plot(annual_incomes, np.array(years_to_reach_capital_no_support).copy(), marker="o", alpha=0.5, linestyle="-.")
        plt.plot(annual_incomes, np.array(years_to_reach_capital).copy(), marker="x", color = line_temp.get_color())
        
        years_to_reach_capital = []
        years_to_reach_capital_no_support = []

    legend = []

    for interest_rate in interest_rates:
        legend.append(interest_rate)
        legend.append(interest_rate)


    plt.legend([f"Annual return rate: {interest_rate*100:.1f} %" for interest_rate in legend])
    
    plt.xlabel("Annual Income in EUR")
    plt.gca().get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))
    plt.ylabel("Years to reach sufficient capital")
    
    plt.grid()
    
    if save_plot_to_disk:
        if annual_income_cap > max(annual_incomes):
            plt.savefig("growthtime_estimations_nocap.png")
        else:
            tag = "_redistributed" if income_support > 0 else ""
            tag = tag + "_subsidy_" + str(int(economy_subsidy/1e9)) + "b" if economy_subsidy > 0 else tag
            plt.savefig("growthtime_estimations_cap_" + str(int(annual_income_cap/1e3)) + "k" + str(tag)+".png")

    plt.show()


def calculate_income_support(income_distribution: list, annual_income_cap: float, number_of_citizens: float = 1, economy_subsidy: float = 0) -> list:
    """
    This function calculates the income support for each income bracket below the annual income cap.

    The support is based on two components:
        1. Support from the redistribution of the total income tax difference above the income tax at the annual income cap.
        In this case the annual support is distributed to the income brackets below the annual income cap according their occurence in the income distribution.
        2. Support from the economy through profits of the companies in the country. It is only distributed to people below the annual income cap.
        This support is distributed also according to the occurence of the income brackets in the income distribution.

    params:
        income_distribution: list, list of annual income values and their probabilities
        annual_income_cap: float, annual income in EUR that would represent "the maximum income needed" even if the current annual income is higher.
        number_of_citizens: float, number of citizens in the country - used to compute the additional income subsidy through profits of the companies in a country.
        economy_subsidy: float, additional income subsidy through economic profits in EUR

    returns:
        support_per_income_bracket: list, list of income support for each income bracket below the annual income cap
        accumulated_support_difference: float, accumulated income tax difference above the annual income cap
    """

    support_per_income_bracket = np.zeros((len(income_distribution)))


    accumulated_income_tax_under_cap = 0
    accumulated_income_tax_over_cap = 0

    total_percentage_below_income_cap = 0
    
    for i in range(len(income_distribution)):
        annual_income, percentage = income_distribution[i]
  

        if annual_income < annual_income_cap:
            income_tax = TaxCalculator.calculate_german_income_tax(annual_income)
            income_tax_at_cap = TaxCalculator.calculate_german_income_tax(annual_income_cap)

            income_tax_deviation_from_cap = income_tax_at_cap - income_tax
            accumulated_income_tax_under_cap += income_tax_deviation_from_cap * percentage
            total_percentage_below_income_cap += percentage

        if annual_income >= annual_income_cap:

            
            income_tax = TaxCalculator.calculate_german_income_tax(annual_income)
            income_tax_at_cap = TaxCalculator.calculate_german_income_tax(annual_income_cap)

            logging.debug(f"Annual income: {annual_income}")
            logging.debug(f"Income tax: {income_tax}")
            logging.debug("Income tax at cap:" + str(income_tax_at_cap))

            income_tax_deviation_from_cap = income_tax_at_cap - income_tax
            accumulated_income_tax_over_cap += income_tax_deviation_from_cap * percentage

            support_per_income_bracket[i] = income_tax_deviation_from_cap

            logging.debug("Support per income bracked: " +str(support_per_income_bracket[i]))

    accumulated_support_difference = accumulated_income_tax_under_cap - np.abs(accumulated_income_tax_over_cap)
    
    number_of_citizens_below_income_cap = number_of_citizens * total_percentage_below_income_cap

    logging.debug("total percentage below income cap: " + str(total_percentage_below_income_cap))


    for i in range(len(income_distribution)):
        annual_income, percentage = income_distribution[i]
        
        logging.debug(f"percentage pre normalization: {percentage}")
        
        percentage = percentage / total_percentage_below_income_cap

        logging.debug(f"percentage post normalization: {percentage}")
        
        if annual_income <= annual_income_cap:
            support_per_income_bracket[i] = (np.abs(accumulated_income_tax_over_cap)+economy_subsidy/number_of_citizens_below_income_cap) * percentage

    return support_per_income_bracket, accumulated_support_difference
    






if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO, format='%(funcName)s:  %(message)s')

    
    annual_income_cap = 100e3
    number_of_citizens = 83e6
    economy_subsidy = 1000e9

    interest_rate_low_risk = 0.05
    

    interest_rates = np.array([0.07, 0.14])


    #income_distribution = [[20e3,0.2], [50e3,0.3], [80e3,0.2], [100e3,0.1], [150e3,0.1], [200e3,0.05], [300e3,0.05]]
    income_distribution = IncomeDistribution.cutoff_income_distribution(IncomeDistribution.income_distribution_germany_annual_pretax_2025, 20e3)



    create_plot_for_income_and_interest_rate(income_distribution=income_distribution, interest_rate_low_risk=interest_rate_low_risk, interest_rates=interest_rates,
                                             annual_income_cap=annual_income_cap, number_of_citizens=number_of_citizens,economy_subsidy=economy_subsidy, 
                                             save_plot_to_disk=False)
    

    #IncomeDistribution.plot_income_distribution_as_bar_chart(income_distribution, "toy_income_distribution.png")
    
