import cx_Oracle
import datetime as dt
from typing import Optional, Union



def insertFileDetails(appDbConnStr: str, regulationName: str,
                      type: str, amendmentNo: int,
                      notificationDate: dt.date, effectiveDate: dt.date,
                      repealDate: dt.date, keyWordsByAdmin: str, docRefNo: int,uploadPDFFile:str,
                      linkToCERCSitePDF:str) -> bool:
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
        colNames = ["regulation_name", "reg_type", "amendment_no", "notification_date",
                    "effective_date", "repeal_date", "keyWords_admin", "doc_ref_no", "pdf_file_name","cerc_Site_pdf_link"]

       

        # get cursor for raw data table
        dbCur = dbConn.cursor()

        

        sqlVals = [regulationName, type, amendmentNo, notificationDate,
                   effectiveDate, repealDate, keyWordsByAdmin, docRefNo, uploadPDFFile,linkToCERCSitePDF]

        # text for sql place holders
        sqlPlaceHldrsTxt = ','.join([':{0}'.format(x+1)
                                     for x in range(len(colNames))])

        # insert the code
        codeInsSql = 'insert into WRLDC_REST_SUBSET.FILE_INFO({0}) values ({1})'.format(
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
