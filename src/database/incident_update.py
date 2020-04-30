from datetime import datetime

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db import db


class IncidentUpdate(db.Model):
    update_id = db.Column(db.BigInteger, primary_key=True)
    incident_id = db.Column(db.BigInteger, db.ForeignKey('incident.incident_id'), nullable=False)
    message = db.Column(db.String(512), nullable=False)
    status = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<IncidentUpdate id=%r, name=%r>' % (self.update_id, self.message)


class IncidentUpdateSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = IncidentUpdate


incident_update_schema = IncidentUpdateSchema()
