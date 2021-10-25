import cx_Oracle
import datetime as dt


def deleteDoc(appDbConnStr: str, docId: int) -> bool:
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
            "DELETE FROM  WRLDC_REST_SUBSET.FILE_INFO where ID=:1", (docId,))
        dbConn.commit()
    except Exception as err:
        isDeleteSuccess = False
        print('Error while deleted a code')
        print(err)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isDeleteSuccess
