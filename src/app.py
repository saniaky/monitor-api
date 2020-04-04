from dotenv import load_dotenv
from flask import Flask

from database.db import initialize_db
from routes.movies import movies

load_dotenv()

app = Flask(__name__)
initialize_db(app)
app.register_blueprint(movies)
app.run()
