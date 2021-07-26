from typing import Optional, List, Tuple, Any
import datetime as dt


def getDocUploadChanges(doc,regulationName: str,
                      type: str, amendmentNo: int,
                      notificationDate: dt.date, effectiveDate: dt.date,
                      repealDate: dt.date, keyWordsByAdmin: str, docRefNo: int,uploadPDFFile:str,
                      linkToCERCSitePDF:str) -> List[Tuple[str, Any]]:
    """this function returns what info is changed wrt code object

    Args:
        code (ICode): [description]
        codeId (int): [description]
        code_issue_time (Optional[dt.datetime]): [description]
        code_str (str): [description]
        other_ldc_codes (str): [description]
        code_description (str): [description]
        code_execution_time (dt.datetime): [description]
        code_tags (str): [description]
        code_issued_by (str): [description]
        code_issued_to (str): [description]
        is_code_cancelled (bool): [description]

    Returns:
        List[Tuple[str, Any]]: [description]
    """                          
    changedInfo: List[Tuple[str, Any]] = []

    # check if codeIssueTime has changed
    if not doc["regulation_name"] == regulationName:
        changedInfo.append(("regulation_name", regulationName))

    # check if code_str has changed
    if not doc["reg_type"] == type:
        changedInfo.append(("reg_type", type))

    # check if other ldc codes has changed
    if not doc["amendment_no"] == amendmentNo:
        changedInfo.append(("amendment_no", amendmentNo))

    # check if code issued to has changed
    if not doc["notification_date"] == notificationDate:
        changedInfo.append(("notification_date", notificationDate))

    # check if code Description has changed
    if not doc["effective_date"] == effectiveDate:
        changedInfo.append(("effective_date", effectiveDate))

    # check if code execution time has changed
    if not doc["repeal_date"] == repealDate:
        changedInfo.append(("repeal_date", repealDate))

    # check if code issued by has changed
    if not doc["keyWords_admin"] == keyWordsByAdmin:
        changedInfo.append(("keyWords_admin", keyWordsByAdmin))

    # check if code tags has changed
    if not doc["doc_ref_no"] == docRefNo:
        changedInfo.append(("doc_ref_no", docRefNo))

    # check if is code cancelled has changed
    if not doc["pdf_file_name"] == uploadPDFFile:
        changedInfo.append(("pdf_file_name", uploadPDFFile))

    if not doc["cerc_Site_pdf_link"] == linkToCERCSitePDF:
        changedInfo.append(("cerc_Site_pdf_link", linkToCERCSitePDF))

    return changedInfo
