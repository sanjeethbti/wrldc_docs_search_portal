import cx_Oracle
import datetime as dt
from typing import Optional, List, Tuple, Any
from src.repos.getDocUploadChanges import getDocUploadChanges



def editDocUploadForm(appDbConnStr: str,Id, doc,regulationName: str,
                      type: str, amendmentNo: int,
                      notificationDate: dt.date, effectiveDate: dt.date,
                      repealDate: dt.date, keyWordsByAdmin: str, docRefNo: int,uploadPDFFile:str,
                      linkToCERCSitePDF:str) -> bool:
    """updates a generic code into the app db
    Returns:
        bool: returns true if process is ok
    """
    # code: ICode = getCodeById(appDbConnStr, codeId)

    changedInfo: List[Tuple[str, Any]] = getDocUploadChanges(doc, regulationName,
                                                               type, amendmentNo,
                                                               notificationDate, effectiveDate,
                                                               repealDate, keyWordsByAdmin, docRefNo,
                                                               uploadPDFFile,linkToCERCSitePDF)

    isEditSuccess = True
    if len(changedInfo) == 0:
        return isEditSuccess
    dbConn = None
    dbCur = None
    try:
        # get connection with raw data table
        dbConn = cx_Oracle.connect(appDbConnStr)
        sqlSetString = ','.join(["{0}=:{1}".format(cInf[0], iInd+1)
                                 for iInd, cInf in enumerate(changedInfo)])

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        # edit the code
        codeEditSql = 'update WRLDC_REST_SUBSET.FILE_INFO set {0} where id=:{1}'.format(
            sqlSetString, len(changedInfo)+1)

        sqlVals: List[Any] = [cInf[1] for cInf in changedInfo]
        sqlVals.append(Id)

        dbCur.execute(codeEditSql, sqlVals)

        # commit the changes
        dbConn.commit()
    except Exception as e:
        isEditSuccess = False
        print('Error while updating of DocUpload Form')
        print(e)
    finally:
        # closing database cursor and connection
        if dbCur is not None:
            dbCur.close()
        if dbConn is not None:
            dbConn.close()
    return isEditSuccess
