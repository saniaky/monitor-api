import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from database.db import initialize_db
from routes.routes import init_routes

load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

bcrypt = Bcrypt(app)
jwt = JWTManager(app)
initialize_db(app)
init_routes(app)

app.run()
