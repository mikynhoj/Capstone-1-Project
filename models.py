
from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """Userinfo"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )
    
    password = db.Column(
        db.Text,
        nullable=False,
    )

    @classmethod
    def signup(cls, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Cryptocurrency(db.Model):
    """usercrypto info"""

    __tablename__ = "crypto"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )

    crypto_name = db.Column(
        db.String(140),
        nullable=False,
    )

    crypto_value = db.Column(
        db.Numeric,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )


def connect_db(app):
    """Connect database to Flask app"""
    db.app = app
    db.init_app(app)
