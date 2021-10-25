from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file, abort
from wtforms import Form, StringField, validators, DateTimeField, BooleanField, IntegerField, DateField, SubmitField, FileField, SelectField,PasswordField,HiddenField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from src.repos.repo import cRepo
from src.appConfig import getAppConfig
import secrets
from flask_login import login_required
from src.security.decorators import roles_required
from flask_bcrypt import Bcrypt
import werkzeug




class UserForm(FlaskForm):
    name = StringField('Name',
                                 validators=[DataRequired(), Length(min=2, max=50)])
    userId = IntegerField('User Id',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('a', 'Admin'), ('b', 'Normal User')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit')


class EditUserForm(FlaskForm):
    id=HiddenField('Id')
    password = PasswordField('Password', validators=[DataRequired()])
    cpassword = PasswordField('Confirm Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('a', 'Admin'), ('b', 'Normal User')],
                       validators=[DataRequired()])
    submit = SubmitField('Submit')

class CPassForm(FlaskForm):
    id=HiddenField('Id')
    password = PasswordField('Password', validators=[DataRequired()])
    cpassword = PasswordField('Confirm Password', validators=[DataRequired()])
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
            return redirect(url_for('user.uList'))
        else:
            flash('New user adding failed!', 'danger')
    return render_template('addUser.html.j2', title='Add User', form=form)





@userPage.route('/uList', methods=['GET'])
@login_required
@roles_required(['a'])
def uList():
    appConf = getAppConfig()
    cRepo_init = cRepo(appConf['appDbConnStr'])
    userDetails= cRepo_init.getUList()
    
    return render_template('uList.html.j2', data={'userDetails': userDetails})


@userPage.route('/edit/<Id>', methods=['GET', 'POST'])
@login_required
@roles_required(["a"])
def editUser(Id: int):
    appConf = getAppConfig()
    cRepo_init = cRepo(appConf['appDbConnStr'])
    user = cRepo_init.getUserById(Id)
    if user == None:
        raise werkzeug.exceptions.NotFound()
    form = EditUserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            isSuccess = cRepo_init.editUser(id=Id, password=hashed_password, role=form.role.data)
            if isSuccess:
                    flash('Successfully edited user details ', category='success')
            else:
                    flash('Could not edit the user details ', category='danger')
            return redirect(url_for('user.uList'))
    else:
        form.id.data=Id
        return render_template('editUser.html.j2', form=form)


@userPage.route('/cPass/<Id>', methods=['GET', 'POST'])
@login_required
@roles_required(["b"])
def cPassword(Id: int):
    appConf = getAppConfig()
    cRepo_init = cRepo(appConf['appDbConnStr'])
    user = cRepo_init.getUserById(Id)
    if user == None:
        raise werkzeug.exceptions.NotFound()
    form = CPassForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            isSuccess = cRepo_init.cPassword(id=Id, password=hashed_password)
            if isSuccess:
                    flash('Password changed successfully', category='success')
                    return redirect(url_for('docs.list'))
            else:
                    flash('Password could not be changed ', category='danger')
                    return redirect(url_for('user.cPassword'))
    else:
        form.id.data=Id
        return render_template('cPass.html.j2', form=form)


@userPage.route('/delete/<userId>', methods=['GET', 'POST'])
@login_required
@roles_required(['a'])
def delete(userId: int):
    appConf = getAppConfig()
    cRepo_init = cRepo(appConf['appDbConnStr'])
    user = cRepo_init.getUserById(userId)
    if user == None:
        raise werkzeug.exceptions.NotFound()
    if request.method == 'POST':
        isSuccess = cRepo_init.deleteUser(userId)
        print(isSuccess)
        if isSuccess:
            flash('Successfully deleted the user', category='success')
            return redirect(url_for('user.uList'))
        else:
            flash('Could not delete the user', category='error')
    return render_template('deleteU.html.j2')