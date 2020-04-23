from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from .db import db


class Incident(db.Model):
    incident_id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(45), unique=True, nullable=False)
    components = db.Column(db.String(45), unique=True, nullable=False)

    project_id = db.Column(db.BigInteger)
    author_id = db.Column(db.Integer)

    # members = association_proxy('user_project', 'user')

    def __repr__(self):
        return '<Incident id=%r, name=%r>' % (self.incident_id, self.name)


class IncidentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Incident


project_schema = IncidentSchema()
