import cx_Oracle
import datetime as dt
from typing import Optional, Union



def editUser(appDbConnStr: str, id: int,
                      password: str, role: str) -> bool:
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
        colNames = ["password", "role"]

       

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        

        sqlVals = [ password, role]

        # text for sql place holders
        sqlPlaceHldrsTxt = ','.join([':{0}'.format(x+1)
                                     for x in range(len(colNames))])
        kid = int(id)
        # insert the code
        codeInsSql = f"""update WRLDC_REST_SUBSET.USER_LOGIN set {colNames[0]}= '{password}',{colNames[1]}= '{role}' where ID = {kid}"""

        dbCur.execute(codeInsSql)

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
