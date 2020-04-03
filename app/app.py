from dotenv import load_dotenv
from flask import Flask, jsonify, request

from database.db import initialize_db, db
from database.models import Movie

load_dotenv(verbose=True)
app = Flask(__name__)
initialize_db(app)


# Tutorial
# https://github.com/paurakhsharma/flask-rest-api-blog-series/blob/master/Part%20-%201/movie-bag/app.py

# Request
# https://flask.palletsprojects.com/en/1.1.x/api/#flask.Request

# SQL Examples
# https://www.bradcypert.com/writing-a-restful-api-in-flask-sqlalchemy/

@app.route('/')
def hello():
    return {'response': 'Hello world!'}


@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify({
        'movies': list(map(lambda dev: dev.to_dict(), Movie.query.all()))})


@app.route('/movies', methods=['POST'])
def add_movie():
    movie = Movie()
    movie.name = request.json['name']
    db.session.add(movie)
    db.session.commit()
    return {'movie': len(movie.to_dict())}, 200


@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    if (not request.json):
        return {'error': 'Object is not a JSON', 'request': request.json}, 400

    print(request.json)
    movie = Movie.query.get(movie_id)
    movie.name = request.json['name']
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    db.session.delete(Movie.query.get(movie_id))
    db.session.commit()
    return jsonify({'result': True})


app.run()
