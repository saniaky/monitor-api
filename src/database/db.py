import os

from flask_sqlalchemy import SQLAlchemy

# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
db = SQLAlchemy()


def initialize_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
