from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from marshmallow import Schema
from sqlalchemy import ForeignKey

from .db import db
#
# user_project_table = db.Table(
#     'user_project',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
#     db.Column('project_id', db.Integer, db.ForeignKey('project.project_id')),
# )


# Fields to expose
class UserSchema(Schema):
    class Meta:
        fields = (
            'user_id', 'email', 'first_name', 'last_name', 'avatar_url',
            'created_at', 'last_login', 'password_age')


user_schema = UserSchema()


class User(db.Model):
    user_id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    avatar_url = db.Column(db.String(512), nullable=True)
    # country_id = db.Column(db.BigInteger, ForeignKey('country_id'))
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

    # Relations
    # projects = db.relationship(
    #     'Project',
    #     secondary=user_project_table,
    #     lazy='select',
    #     backref=db.backref('members', lazy=True)
    # )

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return user_schema.dump(self)

    def __repr__(self):
        return '<User %r>' % self.username
