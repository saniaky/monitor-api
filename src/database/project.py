from marshmallow import Schema, INCLUDE

from .db import db


class ProjectSchema(Schema):
    class Meta:
        unknown = INCLUDE


project_schema = ProjectSchema()


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return '<Project %r>' % self.username

    def to_dict(self):
        return project_schema.dump(self)
