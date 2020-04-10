from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.app import App
from database.db import db

apps = Blueprint('apps', __name__)


@jwt_required
@apps.route('', methods=['GET'])
def get_all():
    return jsonify({'apps': list(map(lambda dev: dev.to_dict(), App.query.all()))})


@jwt_required
@apps.route('/<int:entity_id>', methods=['GET'])
def read(entity_id):
    return jsonify({entity_id: 'ok'})


@jwt_required
@apps.route('/', methods=['POST'])
def create():
    user_id = get_jwt_identity()
    body = request.get_json()
    app = App(**body, owner_id=user_id)
    db.session.add(app)
    db.session.commit()
    return {'app': app.to_dict()}, 200


@jwt_required
@apps.route('/<int:entity_id>', methods=['PUT'])
def update(entity_id):
    new_name = request.json['name']
    app = App.query.get(entity_id)
    if not app:
        return {'error': 'App not found'}, 400
    app.name = new_name
    db.session.add(app)
    db.session.commit()
    return jsonify(app.to_dict())


@jwt_required
@apps.route('/<int:entity_id>', methods=['DELETE'])
def delete(entity_id):
    db.session.delete(App.query.get(entity_id))
    db.session.commit()
    return jsonify({'result': True})
