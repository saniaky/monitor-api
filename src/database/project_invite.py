from datetime import datetime

from marshmallow_enum import EnumField
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db import db
from .user_project import UserProjectRole


class ProjectInvite(db.Model):
    invite_id = db.Column(db.BigInteger, primary_key=True)
    sender_id = db.Column(db.BigInteger, nullable=False)
    project_id = db.Column(db.BigInteger, nullable=False)
    role = db.Column(db.Enum(UserProjectRole), nullable=False, default=UserProjectRole.MEMBER)
    email = db.Column(db.String(45), nullable=False)
    token = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    message = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<ProjectInvite id=%r, project=%r>' % (self.invite_id, self.project_id)


class ProjectInviteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectInvite

    role = EnumField(UserProjectRole)


project_invite_schema = ProjectInviteSchema()
