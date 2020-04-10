import enum

from sqlalchemy.orm import relationship, backref

from .db import db
from .project import Project
from .user import User


class UserProjectRole(enum.Enum):
    ADMIN = 'admin'
    MEMBER = 'member'


class UserProject(db.Model):
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.user_id), primary_key=True)
    project_id = db.Column(db.BigInteger, db.ForeignKey(Project.project_id), primary_key=True)
    role = db.Column(db.Enum(UserProjectRole), nullable=False)

    project = relationship('Project', backref=backref("members"))
    user = relationship('User', backref=backref("projects"))
