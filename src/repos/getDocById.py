import datetime as dt
import cx_Oracle
from typing import List



def getDocById(appDbConnStr: str, docId:int):
    targetColumns = ['REGULATION_NAME', 'REG_TYPE', 'AMENDMENT_NO', 'NOTIFICATION_DATE',
                     'EFFECTIVE_DATE', 'REPEAL_DATE', 'KEYWORDS_ADMIN', 'DOC_REF_NO',
                     'PDF_FILE_NAME', 'CERC_SITE_PDF_LINK']

    metricsFetchSql = """
            select {0} from 
            WRLDC_REST_SUBSET.FILE_INFO where ID = :1 """.format(','.join(targetColumns))
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
        dbCur.execute(metricsFetchSql,(docId,))
        print(dbCur.statement)
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
    
    regulation_name = dbRows[colNames.index('REGULATION_NAME')]
    reg_type = dbRows[colNames.index(
            'REG_TYPE')]
    amendment_no = dbRows[colNames.index('AMENDMENT_NO')]
    notification_date = dbRows[colNames.index(
            'NOTIFICATION_DATE')]
    effective_date = dbRows[colNames.index(
            'EFFECTIVE_DATE')]
    repeal_date = dbRows[colNames.index(
            'REPEAL_DATE')]
    keyWords_admin = dbRows[colNames.index(
            'KEYWORDS_ADMIN')]
    doc_ref_no = dbRows[colNames.index(
            'DOC_REF_NO')]
    pdf_file_name = dbRows[colNames.index('PDF_FILE_NAME')]
    cerc_Site_pdf_link = dbRows[colNames.index(
            'CERC_SITE_PDF_LINK')]
        
    docDetail = {
            "id": docId,
            "regulation_name": regulation_name,
            "reg_type": reg_type,
            "amendment_no": amendment_no,
            "notification_date": notification_date,
            "effective_date": effective_date,
            "repeal_date": repeal_date,
            "keyWords_admin": keyWords_admin,
            "doc_ref_no": doc_ref_no,
            "pdf_file_name": pdf_file_name,
            "cerc_Site_pdf_link": cerc_Site_pdf_link
    }
    
    return docDetail
