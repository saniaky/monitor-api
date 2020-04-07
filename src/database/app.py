from marshmallow import Schema, INCLUDE

from .db import db


class AppSchema(Schema):
    class Meta:
        unknown = INCLUDE


app_schema = AppSchema()


class App(db.Model):
    app_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    team_id = db.Column(db.Integer)
    name = db.Column(db.String(45), unique=True, nullable=False)
    checks_per_minute = db.Column(db.Integer)
    default_url = db.Column(db.String(512))

    def __repr__(self):
        return '<App %r>' % self.username

    def to_dict(self):
        return app_schema.dump(self)
