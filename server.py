'''
This is the web server that acts as a service that creates outages raw data
'''
from flask import Flask, render_template
from waitress import serve
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from typing import Any, cast
from src.appConfig import initAppConfig

# get application config
appConfig = initAppConfig()
appPrefix = appConfig["appPrefix"]

app = Flask(__name__)

# Set the secret key to some random bytes
app.secret_key = appConfig['flaskSecret']

# limit max upload file size to 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024


@app.route('/')
def index():
    return render_template('home.html.j2')
    # return "Hello"


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