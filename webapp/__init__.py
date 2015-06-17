# Setting up the web server

import os
from flask import Flask

ALLOWED_EXTENSIONS = set(['tsv','csv'])
UPLOAD_FOLDER = os.getcwd() + '/webapp/tmp/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['SERVER_NAME'] = 'localhost:50001'
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from webapp import views
