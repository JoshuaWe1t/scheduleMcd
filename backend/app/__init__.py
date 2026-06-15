import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from scheduleMcd.backend.app import main

app = Flask(__name__, 
            template_folder=r'C:\v_mint_acr\miniProjectSchedule\frontend\src\templates', 
            static_folder=r'C:\v_mint_acr\miniProjectSchedule\frontend\src\static')
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', 'config.py'))
app.config.from_object('config')
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)

from scheduleMcd.backend.app import models