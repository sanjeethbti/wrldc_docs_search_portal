from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, abort
from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField, DateField, SubmitField, FileField, SelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.repos.repo import cRepo
from src.appConfig import getAppConfig
import os
import secrets
from flask_login import login_required
from src.security.decorators import roles_required


class docUploadForm(FlaskForm):
    regulationName = StringField('Regulation Name',
                                 validators=[DataRequired(), Length(min=2, max=20)])
    type = SelectField('Type', choices=[('Regulation', 'Regulation'), ('SOR', 'SOR'), ('Corrigendum', 'Corrigendum')],
                       validators=[DataRequired()])
    amendmentNo = IntegerField('Amendment No', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',
    #                                  validators=[DataRequired(), EqualTo('password')])
    notificationDate = DateField('Notification Date',
                                 validators=[DataRequired()])
    effectiveDate = DateField('Effective Date',
                              validators=[DataRequired()])
    repealDate = DateField('Repeal Date',
                           validators=[DataRequired()])
    keyWordsByAdmin = StringField('Key Words by Admin',
                                  validators=[DataRequired()])
    docRefNo = IntegerField('Doc Ref No', validators=[DataRequired()])
    uploadPDFFile = FileField('Upload PDF File', validators=[
                              FileAllowed(['pdf'])])
    linkToCERCSitePDF = StringField('Link to CERC Site PDF',
                                    validators=[DataRequired()])
    submit = SubmitField('Submit')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).first()
    #     if user:
    #         raise ValidationError('That username is taken. Please choose a different one.')

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')


docsPage = Blueprint('docs', __name__,
                     template_folder='templates')


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    # in python if unused varible can be named as _ in order to throw it,slpitext split filename and extension
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    # join concatenate aii three value
    # form_pdf=secure_filename(picture_fn)
    appConf = getAppConfig()
    picture_path = os.path.join(appConf['upload_folder'], picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@docsPage.route("/fileUpload", methods=['GET', 'POST'])
@roles_required(["a"])
def fileUpload():
    form = docUploadForm()
    if form.validate_on_submit():
        if form.uploadPDFFile.data:
            fileName = save_picture(form.uploadPDFFile.data)
        appConf = getAppConfig()
        cRepo_init = cRepo(appConf['appDbConnStr'])
        isInsertSuccess = cRepo_init.insertFileDetails(regulationName=form.regulationName.data, type=form.type.data, amendmentNo=form.amendmentNo.data,
                                                       notificationDate=form.notificationDate.data, effectiveDate=form.effectiveDate.data, repealDate=form.repealDate.data, keyWordsByAdmin=form.keyWordsByAdmin.data,
                                                       docRefNo=form.docRefNo.data, uploadPDFFile=fileName, linkToCERCSitePDF=form.linkToCERCSitePDF.data)
        if isInsertSuccess:
            flash('Your Document uploaded successfully!', 'success')
            return render_template('home.html.j2')
        else:
            flash('Document uploading failed!', 'danger')
    return render_template('docUpload.html', title='Upload Doc', form=form)


@docsPage.route('/download', defaults={'req_path': ''})
@docsPage.route('/download/<path:req_path>')
@roles_required(["a"])
def downloadDocument(req_path):
    appConf = getAppConfig()
    BASE_DIR = appConf['upload_folder']

    # Joining the base and the requested path
    abs_path = os.path.join(BASE_DIR, req_path)

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)
    else:
        return abort(404)
