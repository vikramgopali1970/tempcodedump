

queryLiabilityGoal = ("select l.liability_count, l.liability_amount, l.liability_interest_rate, l.liability_tenure, l.liability_start_date,l.userid "
            "from liabilities l "
            "where l.userid = 4 ")

queryChildrenGoal = ( "select d.children_flag, d.children_count, d.child_1_dob, d.child_1_name, d.child_2_dob, d.child_2_name,d.child_3_dob, d.child_3_name,d.child_4_dob,d.child_4_name,d.child_5_dob,d.child_5_name,a.inflation_marriage,a.inflation_education,a.userid "
               " from demographics d, assumptions a "
               " where a.userid = d.userid AND d.userid = 4 " )

queryMarriageRetirement = ("select e.expense_grocery,e.expense_transportation, e.expense_utilities, e.expense_help, e.expense_phone_internet, e.expense_annual,"
             "e.expense_dining_out, e.expense_entertainment, e.expense_shopping, e.expense_miscellaneous, e.expense_vacation, "
             "a.inflation_living, i.rental_income_self, i.rental_income_spouse, a.life_expectancy, a.userid,d.married_flag, d.marriage_amount,d.marriage_years, a.retirement_age, d.dob , a.userid "
             "from expenses e, assumptions a, income i, demographics d"
             " where e.userid = a.userid and e.userid = i.userid AND e.userid = d.userid and e.userid = 4")

insertAlgoLiabilityGoalQuery = "INSERT INTO `algo_liability_table` (`userid`, `liability_check`, `liability_goal_count`, `liability_remaining_tenure`, `liability_foreclosure`, `liability_foreclosure_outstanding`, `liability_current_tenure`, `liability_today_outstanding`) " \
                                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

insertAlgoChildrenGoalQuery = "INSERT INTO `algo_children_table` (`userid`, `child_check`, `child_age`, `child_college`, `child_college_amount`, `child_college_corpus`, `child_marriage`, `child_marriage_amount`, `child_marriage_corpus`) " \
                              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

insertAlgoMarriageRetirementQuery = "INSERT INTO `algo_marraige_retirement_table` (`userid`, `marriage_check`, `marriage_goal`, `user_age`, `years_retirement`, `retirement_check`, `monthly_expenses_selective`, `monthly_expenses_future`, `debt_rate`, `future_inflation_rate`, `monthly_inflows_other`, `monthly_inflows_future`, `net_growth_rate`, `years_post_retirement`, `retirement_corpus`)" \
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"