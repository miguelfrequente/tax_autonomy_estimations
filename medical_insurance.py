import sys

"""
It has been stages in some Twitter and LinkedIn posts that public health insurance in Germany is mind boggling high due to the number
of people in it who get services but don't contibute to it.

This was a very quick back on the envelope calculation to check this hypothesis.

There is crude approximation that on average every person would contribute at least 350 EUR/month according to his/her income.

That might not be competely right due to the income distribution in Germany (and the according scheme of paying 14.6 % of income for public medical insurrance.)

"""

insurance_cost = 350

total_payers = 58e6 
total_nonpayers = 74e6-58e6

total_payments = insurance_cost * total_payers

effective_monthly_payment = (total_payers+total_nonpayers)/total_payers*insurance_cost

print(effective_monthly_payment)