from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.associationproxy import association_proxy

from .country import Country
from .db import db


# Fields to expose
# user_project_table = db.Table(
#     'user_project',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
#     db.Column('project_id', db.Integer, db.ForeignKey('project.project_id')),
# )


class User(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    avatar_url = db.Column(db.String(512), nullable=True)
    country_id = db.Column(db.String(2), db.ForeignKey(Country.iso2), nullable=True)
    email = db.Column(db.String(45), nullable=False)
    email_verified = db.Column(db.Boolean, default=False, nullable=False)
    email_verification_token = db.Column(db.String(45))
    password = db.Column(db.String(45), nullable=False)
    password_reset_token = db.Column(db.String(45), nullable=True)
    password_reset_expires = db.Column(db.String(45), nullable=True)
    password_age = db.Column(db.DateTime(45), nullable=False, default=datetime.utcnow)
    failed_login_attempts = db.Column(db.String(45))
    last_login = db.Column(db.String(45))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # bidirectional attribute/collection of "user"/"user_project"
    projects = association_proxy('user_project', 'project')

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User id=%r, first_name=%r>' % (self.user_id, self.first_name)


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = (
            'email_verification_token',
            'password', 'password_reset_token', 'password_reset_expires', 'failed_login_attempts'
        )


user_schema = UserSchema()
short_user_schema = UserSchema(only=('user_id', 'first_name', 'last_name', 'email', 'avatar_url'))
