from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField, DateField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class editDocUploadForm(FlaskForm):
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