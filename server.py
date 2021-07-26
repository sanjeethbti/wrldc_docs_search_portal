'''
This is the web server that acts as a service that creates outages raw data
'''
from flask import Flask, render_template
from waitress import serve
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from typing import Any, cast
from src.appConfig import initAppConfig
from src.routeControllers.oauth import oauthPage, bcrypt, login_manager
from src.routeControllers.docs import docsPage
from src.routeControllers.user import userPage

from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# get application config
appConfig = initAppConfig()
appPrefix = appConfig["appPrefix"]

app = Flask(__name__)

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# limit max upload file size to 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
# bcrypt = Bcrypt(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# login_manager = LoginManager(app)
# login view is used to tell login manager where is our login route in order to check login_required decorator, login is funtion name
login_manager.login_view = 'login'
# bbotstrap alert category message
login_manager.login_message_category = 'info'


@app.route('/')
def index():
    return render_template('index.html.j2')
    # return "Hello"


app.register_blueprint(oauthPage, url_prefix='/oauth')
app.register_blueprint(docsPage, url_prefix='/docs')
app.register_blueprint(userPage, url_prefix='/user')


hostedApp = Flask(__name__)

cast(Any, hostedApp).wsgi_app = DispatcherMiddleware(NotFound(), {
    appPrefix: app
})

if __name__ == '__main__':
    serverMode: str = appConfig['mode']
    if serverMode.lower() == 'd':
        hostedApp.run(host="0.0.0.0", port=int(
            appConfig['flaskPort']), debug=True)
    else:
        serve(app, host='0.0.0.0', port=int(
            appConfig['flaskPort']), url_prefix=appPrefix, threads=1)
