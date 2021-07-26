from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, abort
from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField, DateField, SubmitField, FileField, SelectField,PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.repos.repo import cRepo
from src.appConfig import getAppConfig
import secrets
from flask_login import login_required
from src.security.decorators import roles_required
from flask_bcrypt import Bcrypt




class UserForm(FlaskForm):
    name = StringField('Name',
                                 validators=[DataRequired(), Length(min=2, max=50)])
    userId = IntegerField('User Id',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('a', 'Admin'), ('b', 'Normal User')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit')


bcrypt=Bcrypt()


userPage = Blueprint('user', __name__,
                     template_folder='templates')



@userPage.route("/addUser", methods=['GET', 'POST'])
@login_required
@roles_required(["a"])
def addUser():
    form = UserForm()
    if form.validate_on_submit():
        appConf = getAppConfig()
        cRepo_init = cRepo(appConf['appDbConnStr'])
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        isInsertSuccess = cRepo_init.addUser(user_id=form.userId.data, password=hashed_password, role=form.role.data,name=form.name.data)
        if isInsertSuccess:
            flash('New user added successfully!', 'success')
            return redirect(url_for('user.ulist'))
        else:
            flash('New user adding failed!', 'danger')
    return render_template('addUser.html.j2', title='Add User', form=form)





@userPage.route('uList/', methods=['GET'])
@roles_required(['a'])
def uList():
    appConf = getAppConfig()
    cRepo_init = cRepo(appConf['appDbConnStr'])
    userDetails= cRepo_init.getUList()
    
    return render_template('uList.html.j2', data={'userDetails': userDetails})
