import enum

from sqlalchemy.orm import relationship, backref

from .db import db
from .project import Project
from .user import User


class UserProjectRole(enum.Enum):
    ADMIN = 'ADMIN'
    MEMBER = 'MEMBER'


class UserProject(db.Model):
    user_id = db.Column(db.BigInteger, db.ForeignKey(User.user_id), primary_key=True)
    project_id = db.Column(db.BigInteger, db.ForeignKey(Project.project_id), primary_key=True)
    role = db.Column(db.Enum(UserProjectRole), nullable=False, default=UserProjectRole.MEMBER)
    # added_at?
    # invited_by?

    user = relationship(User, backref=backref("user_project", cascade="all, delete-orphan"), lazy='joined')
    project = relationship(Project, backref=backref("user_project", cascade="all, delete-orphan"), lazy='joined')

    def __repr__(self):
        return '<UserProject user_id=%r, project_id=%r, role=%r>' % (self.user_id, self.project_id, self.role)
