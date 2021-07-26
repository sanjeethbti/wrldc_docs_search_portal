from src.repos.repo import cRepo



def editDocUploadViaForm(docId: int, cRepo: cRepo, form,doc,fileName):
    isSuccess = cRepo.editDocUploadForm(Id=docId,doc=doc,
                                      regulationName=form.regulationName.data,
                                      type=form.type.data,
                                      amendmentNo=form.amendmentNo.data,
                                      notificationDate=form.notificationDate.data,
                                      effectiveDate=form.effectiveDate.data,
                                      repealDate=form.repealDate.data, keyWordsByAdmin=form.keyWordsByAdmin.data,
                                      docRefNo=form.docRefNo.data,
                                      uploadPDFFile=fileName,
                                      linkToCERCSitePDF=form.linkToCERCSitePDF.data)
    return isSuccess
