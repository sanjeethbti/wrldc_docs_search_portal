import cx_Oracle
import datetime as dt
from typing import List



def getList(appDbConnStr: str):
    """fetches codes between 2 dates from app db

    Args:
        appDbConnStr (str): app db connection string
        startDt (dt.datetime): [description]
        endDt (dt.datetime): [description]

    Returns:
        List[ICode]: list of code objects
    """
    targetColumns = ['ID', 'REGULATION_NAME', 'REG_TYPE', 'AMENDMENT_NO', 'NOTIFICATION_DATE',
                     'EFFECTIVE_DATE', 'REPEAL_DATE', 'KEYWORDS_ADMIN', 'DOC_REF_NO',
                     'PDF_FILE_NAME', 'CERC_SITE_PDF_LINK']

    codesFetchSql = """
            select {0}
            from WRLDC_REST_SUBSET.FILE_INFO """.format(','.join(targetColumns))

    # initialise codes to be returned
    docDetails = []
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
        regulation_name = row[colNames.index('REGULATION_NAME')]
        reg_type = row[colNames.index(
            'REG_TYPE')]
        amendment_no = row[colNames.index('AMENDMENT_NO')]
        notification_date = row[colNames.index(
            'NOTIFICATION_DATE')]
        effective_date = row[colNames.index(
            'EFFECTIVE_DATE')]
        repeal_date = row[colNames.index(
            'REPEAL_DATE')]
        keyWords_admin = row[colNames.index(
            'KEYWORDS_ADMIN')]
        doc_ref_no = row[colNames.index(
            'DOC_REF_NO')]
        pdf_file_name = row[colNames.index('PDF_FILE_NAME')]
        cerc_Site_pdf_link = row[colNames.index(
            'CERC_SITE_PDF_LINK')]
        
        docDetail = {
            "id": id,
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
        docDetails.append(docDetail)
    return docDetails
