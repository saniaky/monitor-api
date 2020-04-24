from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db import db
from .incident_update import IncidentUpdate


class Incident(db.Model):
    incident_id = db.Column(db.BigInteger, primary_key=True)
    project_id = db.Column(db.BigInteger, db.ForeignKey('project.project_id'), nullable=False)
    author_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(45), unique=True, nullable=False)
    components = db.Column(db.String(45), unique=True, nullable=False)
    updates = db.relationship('IncidentUpdate', backref='incident', lazy=True)

    def __repr__(self):
        return '<Incident id=%r, name=%r>' % (self.incident_id, self.name)


class IncidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incident


incident_schema = IncidentSchema()
