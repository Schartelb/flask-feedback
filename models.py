from re import U
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    username = db.Column(db.String(20),
                         unique=True,
                         nullable=False)

    password = db.Column(db.Text,
                         unique=True)

    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)

    first_name = db.Column(db.String(30),
                           nullable=False)

    last_name = db.Column(db.String(30),
                          nullable=False)

    @classmethod
    def register(cls, pwd):
        """hash password for push to db"""
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')
        return cls(password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):
    __tablename__ = "feedback"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    title = db.Column(db.String(100),
                      nullable=False)

    content = db.Column(db.String, nullable=False)

    username = db.Column(db.Text, db.ForeignKey("users.username"))

    user = db.relationship('User', backref='feedback')
