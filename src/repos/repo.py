import datetime as dt
from src.repos.insertFilesDetails import insertFileDetails
from src.repos.getLoginUser import getLoginUser
from src.repos.getList import getList

class cRepo():
    """Repository class for Codes data of application
    """
    appDbConnStr: str = ""

    def __init__(self, dbConStr: str) -> None:
        """constructor method
        Args:
            dbConStr (str): database connection string
        """
        self.appDbConnStr = dbConStr
        

    def insertFileDetails(self, regulationName: str,
                      type: str, amendmentNo: int,
                      notificationDate: dt.date, effectiveDate: dt.date,
                      repealDate: dt.date, keyWordsByAdmin: str, docRefNo: int,uploadPDFFile:str,
                      linkToCERCSitePDF:str) -> bool:
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = insertFileDetails(self.appDbConnStr, regulationName, type, amendmentNo, notificationDate,
                   effectiveDate, repealDate, keyWordsByAdmin, docRefNo, uploadPDFFile,linkToCERCSitePDF)
        return isInsertSuccess


    def getLoginUser(self, userId: int):
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        user = getLoginUser(self.appDbConnStr, userId)
        return user


    def getList(self):
        """fetches codes between 2 dates from app db

        Args:
            startDt (dt.datetime): [description]
            endDt (dt.datetime): [description]

        Returns:
            List[ICode]: list of code objects
        """
        return getList(self.appDbConnStr)
