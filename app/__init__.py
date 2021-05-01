from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from .config import Config
import logging
from flask_jwt_extended import JWTManager


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": ["https://groceryscape.web.app"]}})
csrf = CSRFProtect(app)
app.config.from_object(Config)
uploaddir = app.config['UPLOAD_FOLDER']
jwt = JWTManager(app)
db = SQLAlchemy(app)
from app import routes