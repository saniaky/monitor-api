from marshmallow import Schema, fields, validate, validates, ValidationError

from database.user import User


class LoginSchema(Schema):
    email = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=45))

    @validates('email')
    def user_exist(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValidationError("User is not found")


class RegisterSchema(Schema):
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    email = fields.Str(required=True, validate=validate.Length(min=1, max=45))
    password = fields.Str(required=True, validate=validate.Length(min=5, max=45))

    @validates('email')
    def not_exist(self, email):
        user = User.query.filter_by(email=email).first()
        if user:
            raise ValidationError("Such email already registered.")
