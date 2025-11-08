from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = "canhdepchai22kjajfdhouahdsiuahsdiuhaishg331326#W%@4"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/saleappdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 6

db = SQLAlchemy(app)

login = LoginManager(app)