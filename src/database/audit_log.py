from .db import db
from .project import Project


class AuditLog(db.Model):
    event_id = db.Column(db.BigInteger, primary_key=True)
    project_id = db.Column(db.BigInteger, db.ForeignKey(Project.project_id), nullable=False)
    user_id = db.Column(db.BigInteger, nullable=False)
    user_ip = db.Column(db.String(45), nullable=True)
    time = db.Column(db.DateTime, nullable=False)
    action = db.Column(db.String(45), nullable=False)

    def __repr__(self):
        return '<AuditLog id=%r, name=%r>' % (self.event_id, self.action)
