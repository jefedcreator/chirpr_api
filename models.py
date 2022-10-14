from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql.schema import PrimaryKeyConstraint

database_name = "plants"
database_path ="postgres://{}:{}@{}/{}".format('student', 'student','localhost:5432', database_name)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()