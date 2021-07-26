import cx_Oracle
import datetime as dt
from typing import List



def getUList(appDbConnStr: str):
    """fetches codes between 2 dates from app db

    Args:
        appDbConnStr (str): app db connection string
        startDt (dt.datetime): [description]
        endDt (dt.datetime): [description]

    Returns:
        List[ICode]: list of code objects
    """
    targetColumns = ['ID', 'USER_ID', 'ROLE', 'NAME']

    codesFetchSql = """
            select {0}
            from WRLDC_REST_SUBSET.USER_LOGIN """.format(','.join(targetColumns))

    # initialise codes to be returned
    UDetails = []
    colNames = []
    dbRows = []
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)

        # get cursor and execute fetch sql
        dbCur = dbConn.cursor()
        dbCur.execute(codesFetchSql)

        colNames = [row[0] for row in dbCur.description]

        # fetch all rows
        dbRows = dbCur.fetchall()
    except Exception as err:
        dbRows = []
        print('Error while creation of fetching codes between dates')
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
    for row in dbRows:
        id = row[colNames.index('ID')]
        user_id = row[colNames.index('USER_ID')]
        role = row[colNames.index(
            'ROLE')]
        name = row[colNames.index('NAME')]
        
        
        UDetail = {
            "id": id,
            "user_id": user_id,
            "role": role,
            "name": name
        }
        UDetails.append(UDetail)
    return UDetails
