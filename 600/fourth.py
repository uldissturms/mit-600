from problem import *
from functools import *
# Problem Set 4

#
# Problem 1
#

def percentsToDecimal(percents):
    return percents * 0.01

def percentageOf(amount, percents):
    return amount * percentsToDecimal(percents)

def fundsAtTheEndOfYear(salary, save, growthRate, fund):
    savings = percentageOf(salary, save)
    if len(fund) == 0:
        return savings

    last_fund = fund[-1]
    income_from_growth = percentageOf(last_fund, growthRate)
    return savings + last_fund + income_from_growth

def nestEggFixed(salary, save, growthRate, years, fund = []):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: the annual percent increase in your investment account (an
      integer between 0 and 100).
    - years: the number of years to work.
    - return: a list whose values are the size of your retirement account at
      the end of each year.
    """

    assert salary >= 0, 'Salary must be greater than or equal to zero'
    assert save >= 0 and save <= 100, 'Save must be a percentage between 0 and 100'
    assert growthRate >= 0 and growthRate <= 100, 'Growth rate must be a percentage between 0 and 100'
    assert years >= 0 and years <= 100, 'Years must be a value between 0 and 100'

    if years == 0:
        return fund

    return nestEggFixed(
        salary,
        save,
        growthRate,
        years - 1,
        append(fundsAtTheEndOfYear(salary, save, growthRate, fund), fund)
    )

def testNestEggFixed():
    salary     = 10000
    save       = 10
    growthRate = 15
    years      = 5
    savingsRecord = nestEggFixed(salary, save, growthRate, years)
    print(savingsRecord)
    # Output should have values close to:
    # [1000.0, 2150.0, 3472.5, 4993.375, 6742.3812499999995]

    # TODO: Add more test cases here.

#
# Problem 2
#

def fundReducer(salary, save):
    yearly_savings = percentageOf(salary, save)
    def fundReducerInner(fund, curr):
        return append(fundsAtTheEndOfYear(salary, save, curr, fund), fund)
    return fundReducerInner

def nestEggVariable(salary, save, growthRates):
    # TODO: Your code here.
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - growthRate: a list of the annual percent increases in your investment
      account (integers between 0 and 100).
    - return: a list of your retirement account value at the end of each year.
    """
    return reduce(fundReducer(salary, save), [0] + growthRates[1:], [])

def testNestEggVariable():
    salary      = 10000
    save        = 10
    growthRates = [3, 4, 5, 0, 3]
    savingsRecord = nestEggVariable(salary, save, growthRates)
    print(savingsRecord)
    # Output should have values close to:
    # [1000.0, 2040.0, 3142.0, 4142.0, 5266.2600000000002]

    # TODO: Add more test cases here.

#
# Problem 3
#

def retirementReducer(savings, expenses):
    def retirementReducerInner(fund, curr):
        percentage = 1 + percentsToDecimal(curr)
        curr_savings = fund[-1] if len(fund) else savings
        return append(curr_savings * percentage - expenses, fund)
    return retirementReducerInner

def postRetirement(savings, growthRates, expenses):
    """
    - savings: the initial amount of money in your savings account.
    - growthRate: a list of the annual percent increases in your investment
      account (an integer between 0 and 100).
    - expenses: the amount of money you plan to spend each year during
      retirement.
    - return: a list of your retirement account value at the end of each year.
    """
    # TODO: Your code here.
    return reduce(retirementReducer(savings, expenses), growthRates, [])

def testPostRetirement():
    savings     = 100000
    growthRates = [10, 5, 0, 5, 1]
    expenses    = 30000
    savingsRecord = postRetirement(savings, growthRates, expenses)
    print(savingsRecord)
    # Output should have values close to:
    # [80000.000000000015, 54000.000000000015, 24000.000000000015,
    # -4799.9999999999854, -34847.999999999985]

#
# Problem 4
#

def maxExpensesFor(savings, postRetireGrowthRates, epsilon):
    return maxExpensesForRange(savings, postRetireGrowthRates, epsilon, 0, savings)

def maxExpensesForRange(savings, postRetireGrowthRates, epsilon, low, high):
    guess = (low + high) / 2.0
    balance = postRetirement(savings, postRetireGrowthRates, guess)[-1]
    if abs(balance) <= epsilon:
        return guess

    if balance < 0:
        return maxExpensesForRange(savings, postRetireGrowthRates, epsilon, low, guess)
    else:
        return maxExpensesForRange(savings, postRetireGrowthRates, epsilon, guess, high)

def findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates,
                    epsilon):
    """
    - salary: the amount of money you make each year.
    - save: the percent of your salary to save in the investment account each
      year (an integer between 0 and 100).
    - preRetireGrowthRates: a list of annual growth percentages on investments
      while you are still working.
    - postRetireGrowthRates: a list of annual growth percentages on investments
      while you are retired.
    - epsilon: an upper bound on the absolute value of the amount remaining in
      the investment fund at the end of retirement.
    """

    savings = nestEggVariable(salary, save, preRetireGrowthRates)[-1]
    return maxExpensesFor(savings, postRetireGrowthRates, epsilon)

def testFindMaxExpenses():
    salary                = 10000
    save                  = 10
    preRetireGrowthRates  = [3, 4, 5, 0, 3]
    postRetireGrowthRates = [10, 5, 0, 5, 1]
    epsilon               = .01
    expenses = findMaxExpenses(salary, save, preRetireGrowthRates, postRetireGrowthRates, epsilon)
    print(expenses)
    # Output should have a value close to:
    # 1229.95548986
