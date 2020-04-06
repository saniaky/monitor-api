from .db import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return '<Movie %r>' % self.username

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
