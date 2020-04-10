from marshmallow import Schema, fields, validate, validates, ValidationError

from database.db import db
from database.user import User

first_name_validate = validate.Length(min=1, max=45)
last_name_validate = validate.Length(min=1, max=45)
email_validate = validate.Email()
avatar_validate = validate.URL(relative=False, schemes=['http', 'https'])
password_validate = validate.Length(min=5, max=45)


class LoginSchema(Schema):
    email = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    password = fields.Str(required=True, validate=password_validate)

    @validates('email')
    def user_exist(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("User is not found")


class RegisterSchema(Schema):
    first_name = fields.Str(required=True, validate=first_name_validate)
    last_name = fields.Str(required=True, validate=last_name_validate)
    email = fields.Str(required=True, validate=email_validate)
    password = fields.Str(required=True, validate=password_validate)

    @validates('email')
    def not_exist(self, email):
        # SQL: SELECT user.user_id AS user_user_id FROM user WHERE user.email = %s
        exist = db.session.query(User.user_id).filter_by(email=email).scalar() is not None
        if exist:
            raise ValidationError("Such email already registered.")


class UpdateProfileSchema(Schema):
    first_name = fields.Str(required=False, validate=first_name_validate)
    last_name = fields.Str(required=False, validate=last_name_validate)
    password = fields.Str(required=False, validate=password_validate)
    avatar_url = fields.Str(required=False, validate=avatar_validate)
