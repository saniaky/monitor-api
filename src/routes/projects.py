from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.db import db
from database.project import Project

projects = Blueprint('projects', __name__)


@jwt_required
@projects.route('/', methods=['GET'])
def get_all():
    Project.query.filter_by({})
    return jsonify({'projects': list(map(lambda dev: dev.to_dict(), Project.query.all()))})


@jwt_required
@projects.route('/<int:entity_id>', methods=['GET'])
def read(entity_id):
    # TODO query for user
    return jsonify({entity_id: 'entity_id'})


@jwt_required
@projects.route('/', methods=['POST'])
def create():
    user_id = get_jwt_identity()
    body = request.get_json()
    app = Project(**body)
    db.session.add(app)

    db.session.commit()
    return jsonify(app.to_dict())


@jwt_required
@projects.route('/<int:entity_id>', methods=['PUT'])
def update(entity_id):
    new_name = request.json['name']
    project = Project.query.get(entity_id)
    if not project:
        return {'error': 'Project not found'}, 400
    project.name = new_name
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict())


@jwt_required
@projects.route('/<int:entity_id>', methods=['DELETE'])
def delete(entity_id):
    db.session.delete(Project.query.get(entity_id))
    db.session.commit()
    return jsonify({'result': True})


def is_id_exist(project_id):
    return db.session.query(Project.project_id).filter_by(project_id=project_id).scalar() is not None
