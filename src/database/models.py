from flask_bcrypt import generate_password_hash, check_password_hash

from .db import db


class User(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_token = db.Column(db.String(45))
    password = db.Column(db.String(45), nullable=False)
    password_reset_token = db.Column(db.String(45), nullable=True)
    password_reset_expires = db.Column(db.String(45), nullable=True)
    password_age = db.Column(db.String(45), nullable=False)
    failed_login_attempts = db.Column(db.String(45))
    last_login = db.Column(db.String(45))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    avatar_url = db.Column(db.String(512))

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<User %r>' % self.username


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.username

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
