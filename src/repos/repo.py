import datetime as dt
from src.repos.insertFilesDetails import insertFileDetails
from src.repos.getLoginUser import getLoginUser
from src.repos.getList import getList
from src.repos.addUser import addUser
from src.repos.getUList import getUList
from src.repos.getDocById import getDocById
from src.repos.editDocUploadForm import editDocUploadForm
from src.repos.getListForUser import getListForUser
from src.repos.updateUserKeyword import updateUserKeyword




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
        return getList(self.appDbConnStr)

    def getListForUser(self,userId: int):
        return getListForUser(self.appDbConnStr,userId)

    
    def addUser(self, user_id: int,
                      password: str, role: str,name:str) -> bool:
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = addUser(self.appDbConnStr, user_id, password, role,name)
        return isInsertSuccess



    def getUList(self):
        return getUList(self.appDbConnStr)

    
    def getDocById(self, docId: int):
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        doc = getDocById(self.appDbConnStr, docId)
        return doc

    
    def editDocUploadForm(self,Id,doc, regulationName: str,
                      type: str, amendmentNo: int,
                      notificationDate: dt.date, effectiveDate: dt.date,
                      repealDate: dt.date, keyWordsByAdmin: str, docRefNo: int,uploadPDFFile:str,
                      linkToCERCSitePDF:str) -> bool:
        """inserts a generic code into the app db
        Returns:
            bool: returns true if process is ok
        """
        isInsertSuccess = editDocUploadForm(self.appDbConnStr,Id,doc, regulationName, type, amendmentNo, notificationDate,
                   effectiveDate, repealDate, keyWordsByAdmin, docRefNo, uploadPDFFile,linkToCERCSitePDF)
        return isInsertSuccess

    def updateUserKeyword(self,keywords_user,docid,kid,userid):
        isSuccess=updateUserKeyword(self.appDbConnStr,keywords_user,docid,kid,userid)
        return isSuccess
