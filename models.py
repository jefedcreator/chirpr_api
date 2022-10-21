from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.ext.mutable import Mutable
from settings import DB_NAME, DB_USER, DB_PASSWORD

database_path ="postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD,'localhost:5432', DB_NAME)
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    def pop(self, index=0):
        value = list.pop(self, index)
        self.changed()
        return value

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value




# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:hemid8th@localhost:5432/chirpr'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), nullable=False)
    avatar_url = db.Column(db.String(), nullable=False)
    tweet_id = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    # tweets = db.relationship('tweets', backref='users', lazy = True)
    # bookmarks = db.relationship('bookmarks', backref='users', lazy = True)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.name}>'

class Tweets(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.String(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    timestamp = db.Column(BIGINT, nullable=False)
    likes = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replies = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replying_to = db.Column(db.String())
    # user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.text}>'

class Bookmarks(db.Model):
    __tablename__ = 'bookmarks'
    id = db.Column(db.String(), primary_key=True)
    text = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    timestamp = db.Column(BIGINT, nullable=False)
    likes = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replies = db.Column(MutableList.as_mutable(ARRAY(db.String())))
    replying_to = db.Column(db.String())
    # user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Person ID: {self.id}, name: {self.text}>'

