import enum

from marshmallow import INCLUDE, Schema
from sqlalchemy.orm import relationship, backref

from .db import db
from .project import Project
from .user import User


class UserProjectRole(enum.Enum):
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'


class UserProjectSchema(Schema):
    class Meta:
        unknown = INCLUDE


user_project_schema = UserProjectSchema()


class UserProject(db.Model):
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.user_id), primary_key=True)
    project_id = db.Column(db.BigInteger, db.ForeignKey(Project.project_id), primary_key=True)
    role = db.Column(db.Enum(UserProjectRole), nullable=False, default=UserProjectRole.MEMBER)

    user = relationship(User, backref=backref("user_project", cascade="all, delete-orphan"))
    project = relationship(Project)

    def to_dict(self):
        return user_project_schema.dump(self)
