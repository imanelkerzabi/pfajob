from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_mail import Mail

import os
# Get the absolute path of the current Python file
current_file = os.path.abspath(__file__)

# Get the directory containing the current file
current_directory = os.path.dirname(current_file)

# Obtain the path of the 'pythonic' folder
pythonic_folder = os.path.join(current_directory)
print(pythonic_folder)
os.chdir(f'{pythonic_folder}\static')
print(os.listdir())

# Change the current working directory to the 'pythonic' folder

upload_folder = 'user_pics'
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)

app = Flask(__name__)

app.config['SECRET_KEY']='3a08691f86b5a33af338c1c9037c1e2b32af9025963c0a13f3c9c279857e3e79'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///mydb.db' 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = 'user_pics'
os.chdir('.')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
ckeditor = CKEditor(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

app.config["MAIL_SERVER"] = "smtp.googlemail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")
mail = Mail(app)
from pythonic import routes
