from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from .db import db
from .incident_update import IncidentUpdate, IncidentUpdateSchema


class Incident(db.Model):
    incident_id = db.Column(db.BigInteger, primary_key=True)
    project_id = db.Column(db.BigInteger, db.ForeignKey('project.project_id'), nullable=False)
    author_id = db.Column(db.BigInteger, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    status = db.Column(db.String(45), nullable=False)
    components = db.Column(db.String(45), nullable=True)
    updates = db.relationship(IncidentUpdate, backref='incident', lazy=True, cascade="all,delete")

    def __repr__(self):
        return '<Incident id=%r, name=%r>' % (self.incident_id, self.name)


class IncidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incident
        include_relationships = True
        load_instance = True

    # Override updates field to use a nested representation rather than pks
    updates = Nested(IncidentUpdateSchema, many=True)


incident_schema = IncidentSchema()
