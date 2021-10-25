import cx_Oracle
import datetime as dt


def deleteUser(appDbConnStr: str, userId: int) -> bool:
    """delete a code with id
    If an rto row is associated with a code, it is not deleted in the vendor db, 
    the user should manually delete the rto entry by himself.
    We intentionally skipped deletion for safety.
    Args:
        codeId (int): [description]
    Returns:
        bool: returns true if code is deleted successfully
    """
    dbConn = None
    dbCur = None
    isDeleteSuccess = True
    try:
        # get connection with application db
        dbConn = cx_Oracle.connect(appDbConnStr)
        # get cursor
        dbCur = dbConn.cursor()

        dbCur.execute(
            "DELETE FROM  WRLDC_REST_SUBSET.USER_LOGIN where ID=:1", (userId,))
        dbConn.commit()
        
    except Exception as err:
        isDeleteSuccess = False
        print('Error while deleted a user')
        print(err)
    finally:
        # closing database cursor and connection
        print(dbCur)
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isDeleteSuccess
