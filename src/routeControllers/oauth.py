from flask import Blueprint, redirect, request, url_for, session, render_template,flash
from wtforms import Form, StringField, validators, DateTimeField, BooleanField,IntegerField,DateField,SubmitField,FileField,SelectField,PasswordField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
# from server import app, bcrypt
from flask_login import login_user, current_user, logout_user, login_required,LoginManager
from src.repos.repo import cRepo
from src.appConfig import getAppConfig
from flask_bcrypt import Bcrypt
from src.security.user import User
from src.security.decorators import roles_required



class LoginForm(FlaskForm):
    userId = IntegerField('User Id',
                        validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

bcrypt=Bcrypt()
login_manager = LoginManager()
oauthPage = Blueprint('oauth', __name__,
                      template_folder='templates')

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login helper to retrieve a user from our db
    sUser = session['SUSER']
    return User(sUser['id'], sUser['name'], sUser['password'], sUser['roles'],sUser['rid'])


@oauthPage.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('docs.list'))
    form=LoginForm()
    if request.method == 'POST' and form.validate():
        appConf = getAppConfig()
        cRepo_init = cRepo(appConf['appDbConnStr'])
        userDetails = cRepo_init.getLoginUser(userId=form.userId.data)
        if userDetails and bcrypt.check_password_hash(userDetails['password'], form.password.data):
            user = User(id_=userDetails['userId'], name=userDetails['name'], password=userDetails['password'], roles=userDetails['role'],rid=userDetails['Id'])

            session['SUSER'] = {'id': userDetails['userId'],'rid': userDetails['Id'],
                        'password': userDetails['password'], 'name': userDetails['name'], 'roles': userDetails['role']}
            login_user(user, remember=form.remember.data)
            #it make to redirect to initial request user raised before it was not login
            #get method will return none if next key doent exit,so we use get rather than []
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('docs.list'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login',form=form)



@oauthPage.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



# @oauthPage.route('/home')
# @login_required
# def home():
#     return render_template('home.html.j2')
