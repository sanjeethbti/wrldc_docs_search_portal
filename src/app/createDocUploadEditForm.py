from src.app.editDocUploadForm import editDocUploadForm


def createDocUploadEditForm(doc,form):
    form.regulationName.data = doc["regulation_name"]
    form.type.data = doc["reg_type"]
    form.amendmentNo.data = doc["amendment_no"]
    form.notificationDate.data = doc["notification_date"]
    form.effectiveDate.data = doc["effective_date"]
    form.repealDate.data = doc["repeal_date"]
    form.keyWordsByAdmin.data = doc["keyWords_admin"]
    form.docRefNo.data = doc["doc_ref_no"]
    form.uploadPDFFile.data =  doc["pdf_file_name"]
    form.linkToCERCSitePDF.data =  doc["cerc_Site_pdf_link"]
    return form
