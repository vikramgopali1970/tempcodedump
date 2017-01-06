import mysql.connector
import autoGoalCalculations
import config
import sqlQueries
from strConstants import *
from mysql.connector import Error


try:
    cnx = mysql.connector.connect(user=config.user,password=config.password,host=config.host,database=config.database)
    if cnx.is_connected():
        print 'connected to db successfully'

    liabilityInfo = cnx.cursor()
    liabilityInfo.execute(sqlQueries.queryLiabilityGoal)
    liabilityInfoResults = liabilityInfo.fetchall()

    algo_liability_table = [[0 for i in range(9)]for j in range(liabilityInfo.rowcount)]
    row = 0
    id =1


    for result in liabilityInfoResults:
        # liability check for liability related calculations
        algo_liability_table[row][0] = id
        algo_liability_table[row][1] = result[L_USERID]
        liability_count = result[LIABILITY_COUNT]
        liability_goal_count = liability_count
        algo_liability_table[row][3] = liability_goal_count
        if liability_count != 0:
            liability_check = True
            algo_liability_table[row][2] = 1
            autoGoalCalculations.liabilityCalculator(result, algo_liability_table, row)
        else:
            liability_check = False
            algo_liability_table[row][2] = 0
        liability_goal_count = liability_count
        row += 1
        id += 1

    childrenInfo = cnx.cursor()
    childrenInfo.execute(sqlQueries.queryChildrenGoal)
    childrenInfoResults = childrenInfo.fetchall()

    row = 0
    id = 1
    for result in childrenInfoResults:
        #children related calculations
        children_count = result[CHILDREN_COUNT]
        algo_children_table = [[0 for k in range(10)] for l in range(children_count)]
        child_check = result[CHILDREN_FLAG]
        if child_check in ['Y', 'y']:
            autoGoalCalculations.childCalculator(result, algo_children_table)
        else:
            algo_children_table[row][2] = 0
        row += 1
        id += 1

    marriageRetirementInfo = cnx.cursor()
    marriageRetirementInfo.execute(sqlQueries.queryMarriageRetirement)
    marriageRetirementInfoResults = marriageRetirementInfo .fetchall()

    algo_married_retirement_table = [[0 for i in range(16)] for j in range(marriageRetirementInfo.rowcount)]
    row = 0
    id = 1

    for result in marriageRetirementInfoResults:
        # marriage check for the marriage related calculation
        algo_married_retirement_table[row][0] = id
        algo_married_retirement_table[row][1] = result[MR_USERID]
        marriage_check = result[MARRIED_FLAG]
        if marriage_check in ['Y', 'y'] and bool(result[MARRIAGE_AMOUNT]) and bool(result[MARRIAGE_YEARS]):
            algo_married_retirement_table[row][2] = 1
            autoGoalCalculations.marraigeCalculator(result, algo_married_retirement_table, row)
        else:
            algo_married_retirement_table[row][2] = 0

        # user income related calculations
        autoGoalCalculations.userRelatedCalculation(result, algo_married_retirement_table, row)

        row += 1
        id += 1



    insertCursor = cnx.cursor();
    for x in range(liabilityInfo.rowcount):
        print algo_liability_table[x],"liability"
        Insertargs = (algo_liability_table[x][1], algo_liability_table[x][2], algo_liability_table[x][3], algo_liability_table[x][4], algo_liability_table[x][5], float(algo_liability_table[x][6]), algo_liability_table[x][7], float(algo_liability_table[x][8]))
        insertCursor.execute(sqlQueries.insertAlgoLiabilityGoalQuery,Insertargs)
        cnx.commit()

    for m in range(children_count):
        print algo_children_table[m],"child"
        Insertargs = (algo_children_table[m][1],algo_children_table[m][2],algo_children_table[m][3],algo_children_table[m][4],algo_children_table[m][5],float(algo_children_table[m][6]),algo_children_table[m][7],algo_children_table[m][8],float(algo_children_table[m][9]))
        insertCursor.execute(sqlQueries.insertAlgoChildrenGoalQuery,Insertargs)
        cnx.commit()

    for n in range(marriageRetirementInfo.rowcount):
        print algo_married_retirement_table[n],"married_retirement"
        Insertargs = (algo_married_retirement_table[n][1], algo_married_retirement_table[n][2], algo_married_retirement_table[n][3], algo_married_retirement_table[n][4], algo_married_retirement_table[n][5], algo_married_retirement_table[n][6], algo_married_retirement_table[n][7], algo_married_retirement_table[n][8], algo_married_retirement_table[n][9], algo_married_retirement_table[n][10], algo_married_retirement_table[n][11], algo_married_retirement_table[n][12], algo_married_retirement_table[n][13], algo_married_retirement_table[n][14], algo_married_retirement_table[n][15])
        insertCursor.execute(sqlQueries.insertAlgoMarriageRetirementQuery,Insertargs)
        cnx.commit()



except Error as e:
    print e

finally:
    print cnx
    cnx.close()