import cx_Oracle
import datetime as dt
from typing import Optional, Union


def updateUserKeyword(appDbConnStr: str, keywords_user: str,
                      docid: int, kid: int,
                      userid: int) -> bool:
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
        # get cursor for raw data table
        dbCur = dbConn.cursor()
        # column names of the raw data table
        if(kid == 'None'):
            colNames = ["keyWords_user", "doc_id", "user_id"]
            sqlVals = [keywords_user, docid, userid]

            # text for sql place holders
            sqlPlaceHldrsTxt = ','.join([':{0}'.format(x+1)
                                        for x in range(len(colNames))])

            # insert the code
            codeInsSql = 'insert into WRLDC_REST_SUBSET.USER_KEYWORD({0}) values ({1})'.format(
                ','.join(colNames), sqlPlaceHldrsTxt)

            dbCur.execute(codeInsSql, sqlVals)
        else:
            colNames1 = ["KEYWORDS_USER"]

            testsql = "UPDATE WRLDC_REST_SUBSET.user_keyword SET keywords_user = 'test' WHERE kid = 3"

            # codeEditSql = 'update WRLDC_REST_SUBSET.USER_KEYWORD set {0}="{1}" where KID={2}'.format(
            # colNames1[0], keywords_user, int(kid))
            kid = int(kid)
            codeEditSql = f"""update WRLDC_REST_SUBSET.USER_KEYWORD set {colNames1[0]}= '{keywords_user}' where KID = {kid}"""
            # dbCur.execute(testsql)
            dbCur.execute(codeEditSql)
        # commit the changes
        # commit the changes
        dbConn.commit()
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
