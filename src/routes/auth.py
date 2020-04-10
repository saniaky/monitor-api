import datetime

from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from database.db import db
from database.project import Project, project_schema
from database.user import User, user_schema, short_user_schema
from database.user_project import UserProjectRole, UserProject
from routes.auth_validation import RegisterSchema, LoginSchema, UpdateProfileSchema

auth = Blueprint('auth', __name__)

login_schema = LoginSchema()
register_schema = RegisterSchema()
update_profile_schema = UpdateProfileSchema()


@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    errors = login_schema.validate(body)
    if errors:
        return jsonify({'error': errors}), 400
    user = User.query.filter_by(email=body.get('email')).first()
    authorized = user.check_password(body.get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401
    user.last_login = datetime.datetime.now()
    db.session.commit()
    expires7days = datetime.timedelta(days=7)
    expires30days = datetime.timedelta(days=30)
    access_token = create_access_token(identity=str(user.user_id), expires_delta=expires7days)
    refresh_token = create_access_token(identity=str(user.user_id), expires_delta=expires30days)
    return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200


@auth.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    errors = register_schema.validate(body)
    if errors:
        return jsonify({'error': errors}), 400
    user = User(**body)
    user.hash_password()

    # Create default project for user
    project = Project(name='Test')
    project.members.extend([UserProject(user=user, project=project, role=UserProjectRole.ADMIN)])
    db.session.add(user)
    db.session.commit()
    return jsonify(user_schema.dump(user)), 201


@auth.route('/me', methods=['GET'])
@jwt_required
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {'error': 'Such user no longer exist.'}, 400
    return jsonify(user_schema.dump(user))


@auth.route('/me', methods=['PUT'])
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


@auth.route('/me/projects', methods=['GET'])
@jwt_required
def get_projects():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).scalar()
    return jsonify(project_schema.dump(user.projects, many=True))


@auth.route('/me/projects/<int:project_id>/members', methods=['GET'])
@jwt_required
def get_project_members(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))
