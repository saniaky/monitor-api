from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import db
from database.project import Project, project_schema
from database.user import User, user_schema, short_user_schema
from routes.auth_validation import UpdateProfileSchema

me = Blueprint('me', __name__)

update_profile_schema = UpdateProfileSchema()


@me.route('/me', methods=['GET'])
@jwt_required
def user_profile():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify(user_schema.dump(user))


@me.route('/me', methods=['PUT'])
@jwt_required
def update_profile():
    body = request.get_json()
    errors = update_profile_schema.validate(body)
    if errors:
        return jsonify({'error': errors}), 400
    user_id = get_jwt_identity()
    User.query.filter_by(user_id=user_id).update(body)
    db.session.commit()
    return jsonify({'result': True})


@me.route('/projects', methods=['GET'])
@jwt_required
def get_projects():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).scalar()
    return jsonify(project_schema.dump(user.projects, many=True))


@me.route('/projects/<int:project_id>/incidents', methods=['GET'])
@jwt_required
def get_incidents(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))


@me.route('/projects/<int:project_id>/components', methods=['GET'])
@jwt_required
def get_components(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))


@me.route('/projects/<int:project_id>/subscribers', methods=['GET'])
@jwt_required
def get_subscribers(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))


@me.route('/projects/<int:project_id>/members', methods=['GET'])
@jwt_required
def get_project_members(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))
