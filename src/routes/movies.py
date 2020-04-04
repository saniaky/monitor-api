from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.db import db
from database.models import Movie

movies = Blueprint('movies', __name__)


@movies.route('/')
def hello():
    return {'response': 'Hello world!'}


@movies.route('/movies', methods=['GET'])
def get_movies():
    return jsonify({'movies': list(map(lambda dev: dev.to_dict(), Movie.query.all()))})


@jwt_required
@movies.route('/movies', methods=['POST'])
def add_movie():
    user_id = get_jwt_identity()
    body = request.get_json()
    movie = Movie(**body, author_id=user_id)
    db.session.add(movie)
    db.session.commit()
    return {'movie': movie.to_dict()}, 200


@jwt_required
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


@jwt_required
@movies.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    db.session.delete(Movie.query.get(movie_id))
    db.session.commit()
    return jsonify({'result': True})
