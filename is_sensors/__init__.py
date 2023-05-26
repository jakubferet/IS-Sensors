from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_breadcrumbs import Breadcrumbs
from sqlalchemy_utils.functions import database_exists, create_database

###   POSTGRES CONNECTION   ###

connectionstring = 'postgresql+psycopg2://postgres:postgres@localhost:5432/sensors'
if not database_exists(connectionstring):
    try:
        create_database(connectionstring)
        print('Database created')
    except Exception as e:
        print('Database does not exists and cannot be created')
        raise
else:
    print('Database already exists')

###   FLASK SETTINGS   ###

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = connectionstring
app.config['SECRET_KEY'] = 'ca7fb489025995d56d442f328715e746'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Breadcrumbs(app=app)
db = SQLAlchemy(app)

from is_sensors import routes

#db.drop_all()
#db.create_all()