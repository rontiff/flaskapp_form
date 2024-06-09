
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS 

# Create instance for Flask app
app = Flask(__name__)  

CORS(app)                                                          

# use sqlite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"  

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False            

db = SQLAlchemy(app)  
