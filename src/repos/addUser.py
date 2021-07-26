import cx_Oracle
import datetime as dt
from typing import Optional, Union



def addUser(appDbConnStr: str, user_id: int,
                      password: str, role: str,name:str) -> bool:
    """inserts a generic code into the app db
    Returns:
        bool: returns true if process is ok
    """
    dbConn = None
    dbCur = None
    isInsertSuccess = True
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)
        # column names of the raw data table
        colNames = ["user_id", "password", "role","name"]

       

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        

        sqlVals = [user_id, password, role,name]

        # text for sql place holders
        sqlPlaceHldrsTxt = ','.join([':{0}'.format(x+1)
                                     for x in range(len(colNames))])

        # insert the code
        codeInsSql = 'insert into WRLDC_REST_SUBSET.USER_LOGIN({0}) values ({1})'.format(
            ','.join(colNames), sqlPlaceHldrsTxt)

        dbCur.execute(codeInsSql, sqlVals)

        # commit the changes
        dbConn.commit()
    except Exception as err:
        isInsertSuccess = False
        print('Error while creation of generic code')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isInsertSuccess
