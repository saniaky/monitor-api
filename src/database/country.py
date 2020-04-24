from .db import db


class Country(db.Model):
    iso2 = db.Column(db.String(2), primary_key=True)
    iso3 = db.Column(db.String(3), unique=True, nullable=False)
    name = db.Column(db.String(45), unique=True, nullable=False)

    def __repr__(self):
        return '<Country id=%r, name=%r>' % (self.iso2, self.name)
