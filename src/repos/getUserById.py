import datetime as dt
import cx_Oracle
from typing import List



def getUserById(appDbConnStr: str, Id:int):
    targetColumns = ['ID','USER_ID','PASSWORD' ,'ROLE', 'NAME']

    metricsFetchSql = """
            select {0} from 
            WRLDC_REST_SUBSET.USER_LOGIN where ID = :1 """.format(','.join(targetColumns))
    # initialise codes to be returned
    # dataRecords = []
    colNames = []
    dbRows = None
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(metricsFetchSql,(Id,))
        #print(dbCur.statement)
        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchone()
    except Exception as err:
        dbRows = []
        print('Error while fetching login user details')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()

    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []

    # iterate through each row to populate result outage rows
    Id = dbRows[colNames.index(
            'ID')]
    userId = dbRows[colNames.index(
            'USER_ID')]
    password = dbRows[colNames.index(
            'PASSWORD')]
    role = dbRows[colNames.index(
            'ROLE')]
    name = dbRows[colNames.index(
            'NAME')]
    sampl = {
            "Id":Id,
            "userId": userId,
            "password": password,
            "role": role,
            "name": name
    }
    
    return sampl
