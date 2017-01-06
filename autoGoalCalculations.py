import datetime
import numpy
from strConstants import *

USER_ID = 0
def liabilityCalculator(queryResults, algo_liability_table, row):
    USER_ID = queryResults[L_USERID]
    liability_amount = queryResults[LIABILITY_AMOUNT]
    liability_interest_rate = queryResults[LIABILITY_INTEREST_RATE]
    liability_start_date = queryResults[LIABILITY_START_DATE]
    liability_tenure = queryResults[LIABILITY_TENURE]
    liability_current_tenure = ((datetime.date.today().year - liability_start_date.year) * 12 + (datetime.date.today().month - liability_start_date.month))
    liability_remaining_tenure = (liability_tenure*12) - liability_current_tenure
    algo_liability_table[row][4] = liability_remaining_tenure
    liability_foreclosure = int(round(liability_remaining_tenure * 0.50))
    algo_liability_table[row][5] = liability_foreclosure
    liability_foreclosure_outstanding = numpy.pv(float(liability_interest_rate) / 1200,
                                                 (liability_remaining_tenure - liability_foreclosure),
                                                 -((numpy.pmt(float(liability_interest_rate) / 1200,
                                                              liability_tenure * 12, -(liability_amount), 0, 0)))
                                                 , 0, 0);
    algo_liability_table[row][6] = liability_foreclosure_outstanding
    liability_today_outstanding = numpy.pv(float(liability_interest_rate)/12,liability_current_tenure,numpy.pmt(float(liability_interest_rate)/1200,liability_tenure*12,-(liability_amount),0,0),0,0)
    algo_liability_table[row][7] = liability_current_tenure
    algo_liability_table[row][8] = liability_today_outstanding
    #print liability_remaining_tenure,liability_foreclosure,liability_foreclosure_outstanding,liability_current_tenure,liability_today_outstanding

def marraigeCalculator(queryResult, algo_married_retirement_table, row):
    marriage_amount = queryResult[MARRIAGE_AMOUNT]
    marriage_years = queryResult[MARRIAGE_YEARS]
    inflation_marriage = queryResult[INFLATION_MARRIAGE]
    marriage_goal = marriage_amount * (pow((1 + (float(inflation_marriage) / 100)), marriage_years));
    algo_married_retirement_table[row][3] = float(marriage_goal)


def getChildrenDetailsForMultipleChildren(queryResult, children_details, algo_children_table, row, i):
    #print children_details[i][0]
    child_dob = children_details[i][0]
    child_age = datetime.date.today().year - child_dob.year
    algo_children_table[row][3] = child_age
    if child_age < 15:
        child_college = 17 - child_age
        algo_children_table[row][4] = child_college
        child_college_amount = 2500000
        algo_children_table[row][5] = child_college_amount
        inflation_education = queryResult[INFLATION_EDUCATION]
        child_college_corpus = child_college_amount * (pow(1 + (float(inflation_education) / 100), child_college))
        algo_children_table[row][6] = child_college_corpus
        #print child_age, child_college, child_college_amount, child_college_corpus
    if child_age < 26:
        child_marriage = 28 - child_age
        algo_children_table[row][7] = child_marriage
        child_marriage_amount = 1000000
        algo_children_table[row][8] = child_marriage_amount
        child_marriage_corpus = child_marriage_amount * (pow(1 + (float(float(queryResult[INFLATION_MARRIAGE])) / 100), child_marriage))
        algo_children_table[row][9] = child_marriage_corpus
        #print child_marriage, child_marriage_amount, child_marriage_corpus
    row += 1

def childCalculator(queryResult, algo_children_table):
    children_count = queryResult[CHILDREN_COUNT]
    children_details = [[0 for x in range(CHILD_DOB_NAME)] for y in range(children_count)]
    row = 0
    id = 1
    if children_count < 6:
        CHILD_DOB_FIELD = CHILD_1_DOB
        CHILD_NAME_FIELD = CHILD_1_NAME
        for i in range(children_count):
            algo_children_table[row][0] = id
            algo_children_table[row][1] = queryResult[C_USERID]
            algo_children_table[row][2] = 1
            children_details[i][0] = queryResult[CHILD_DOB_FIELD]
            children_details[i][1] = queryResult[CHILD_NAME_FIELD]
            CHILD_NAME_FIELD += 2
            CHILD_DOB_FIELD += 2
            getChildrenDetailsForMultipleChildren(queryResult, children_details, algo_children_table, row,i)
            row += 1
            id += 1

def userRelatedCalculation(queryResult, algo_married_retirement_table, row):
    user_dob = queryResult[DOB]
    user_age = datetime.date.today().year - user_dob.year
    algo_married_retirement_table[row][4] = user_age
    retirement_age = queryResult[MR_RETIREMENT_AGE]
    years_retirement = retirement_age - user_age
    algo_married_retirement_table[row][5] = years_retirement
    if years_retirement > 0:
        retirement_check = True
        algo_married_retirement_table[row][6] = 1
    else:
        algo_married_retirement_table[row][6] = 0
    expense_grocery = queryResult[EXPENSE_GROCERY]
    expense_transportation = queryResult[EXPENSE_TRANSPORTATION]
    expense_utilities = queryResult[EXPENSE_UTILITIES]
    expense_help = queryResult[EXPENSE_HELP]
    expense_phone_internet = queryResult[EXPENSE_PHONE_INTERNET]
    expense_annual = queryResult[EXPENSE_ANNUAL]
    expense_dining_out = queryResult[EXPENSE_DINING_OUT]
    expense_entertainment = queryResult[EXPENSE_ENTERTAINMENT]
    expense_shopping = queryResult[EXPENSE_SHOPPING]
    expense_miscellaneous = queryResult[EXPENSE_MISCELLANEOUS]
    expense_vacation = queryResult[EXPENSE_VACATION]
    monthly_expenses_selective = (expense_grocery + expense_transportation + expense_utilities + expense_help
                                  + expense_phone_internet + expense_annual + expense_dining_out + expense_entertainment
                                  + expense_shopping + expense_miscellaneous + expense_vacation) * 1.5
    algo_married_retirement_table[row][7] = monthly_expenses_selective
    inflation_living = queryResult[INFLATION_LIVING]
    monthly_expenses_future = monthly_expenses_selective * (pow((1 + (float(inflation_living)) / 100), years_retirement))
    algo_married_retirement_table[row][8] = float(monthly_expenses_future)
    debt_rate = 4.0
    algo_married_retirement_table[row][9] = float(debt_rate)
    future_inflation_rate = 6.0
    algo_married_retirement_table[row][10] = float(future_inflation_rate)
    rental_income_self = queryResult[RENTAL_INCOME_SELF]
    rental_income_spouse = queryResult[RENTAL_INCOME_SPOUSE]
    years_retirement = queryResult[MR_RETIREMENT_AGE] - (datetime.date.today().year - queryResult[DOB].year)
    monthly_inflows_other = float(rental_income_self + rental_income_spouse) / 12
    algo_married_retirement_table[row][11] = float(monthly_inflows_other)
    monthly_inflows_future = monthly_inflows_other * (pow(1 + (5.0 / 100), years_retirement))
    algo_married_retirement_table[row][12] = float(monthly_inflows_future)
    net_growth_rate = ((1 + (debt_rate / 100)) / (1 + (future_inflation_rate / 100))) - 1
    #print debt_rate, future_inflation_rate
    algo_married_retirement_table[row][13] = float(net_growth_rate)
    retirement_age = queryResult[MR_RETIREMENT_AGE]
    life_expectancy = queryResult[LIFE_EXPECTANCY]
    years_post_retirement = life_expectancy - retirement_age
    algo_married_retirement_table[row][14] = years_post_retirement
    retirement_corpus = numpy.pv(float(net_growth_rate) / 12, years_post_retirement * 12,-(monthly_expenses_future - monthly_inflows_future), 0, 0)
    algo_married_retirement_table[row][15] = float(retirement_corpus)

