from flask import Blueprint, request, jsonify

from database.db import db
from database.models import Movie

movies = Blueprint('movies', __name__)


@movies.route('/')
def hello():
    return {'response': 'Hello world!'}


@movies.route('/movies', methods=['GET'])
def get_movies():
    return jsonify({'movies': list(map(lambda dev: dev.to_dict(), Movie.query.all()))})


@movies.route('/movies', methods=['POST'])
def add_movie():
    movie = Movie()
    movie.name = request.json['name']
    db.session.add(movie)
    db.session.commit()
    return {'movie': movie.to_dict()}, 200


@movies.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    new_name = request.json['name']
    movie = Movie.query.get(movie_id)
    if not movie:
        return {'error': 'Movie not found'}, 400
    movie.name = new_name
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict())


@movies.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    db.session.delete(Movie.query.get(movie_id))
    db.session.commit()
    return jsonify({'result': True})
