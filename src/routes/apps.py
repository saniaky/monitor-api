from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.app import App
from database.db import db

apps = Blueprint('apps', __name__)


@jwt_required
@apps.route('/apps', methods=['GET'])
def get_apps():
    return jsonify({'apps': list(map(lambda dev: dev.to_dict(), App.query.all()))})


@jwt_required
@apps.route('/apps', methods=['POST'])
def add_app():
    user_id = get_jwt_identity()
    body = request.get_json()
    app = App(**body, owner_id=user_id)
    db.session.add(app)
    db.session.commit()
    return {'app': app.to_dict()}, 200


@jwt_required
@apps.route('/apps/<int:app_id>', methods=['PUT'])
def update_movie(app_id):
    new_name = request.json['name']
    movie = App.query.get(app_id)
    if not movie:
        return {'error': 'App not found'}, 400
    movie.name = new_name
    db.session.add(movie)
    db.session.commit()
    return jsonify(movie.to_dict())


@jwt_required
@apps.route('/apps/<int:app_id>', methods=['DELETE'])
def delete_movie(app_id):
    db.session.delete(App.query.get(app_id))
    db.session.commit()
    return jsonify({'result': True})
