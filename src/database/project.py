from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db import db


class Project(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return '<Project id=%r, name=%r>' % (self.project_id, self.name)


class ProjectSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Project


project_schema = ProjectSchema()