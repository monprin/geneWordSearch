# Setting up the web server

from flask import Flask

app = Flask(__name__)
app.config['SERVER_NAME'] = '127.0.0.1:50001'
app.config['DEBUG'] = True
from webapp import views
