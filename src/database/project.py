from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.ext.associationproxy import association_proxy

from .db import db
from .incident import Incident


class Project(db.Model):
    project_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)
    incidents = db.relationship(Incident, backref='project', lazy=True)
    members = association_proxy('user_project', 'user')

    def __repr__(self):
        return '<Project id=%r, name=%r>' % (self.project_id, self.name)

    def to_dict(self):
        return project_schema.dump(self)


class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project


project_schema = ProjectSchema()
