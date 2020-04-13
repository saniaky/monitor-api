import datetime

from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token

from database.db import db
from database.project import Project
from database.user import User, user_schema
from database.user_project import UserProjectRole, UserProject
from notifications.email import welcome_email, email_verified
from routes.auth_validation import RegisterSchema, LoginSchema
from utils import random_str

auth = Blueprint('auth', __name__)

login_schema = LoginSchema()
register_schema = RegisterSchema()


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
    user.email_verification_token = random_str()

    # Create default project for user
    # INSERT INTO project (name) VALUES (%s)
    # INSERT INTO user (...) VALUES ()
    # INSERT INTO user_project (user_id, project_id, `role`) VALUES (%s, %s, %s)
    project = Project(name='First project')
    user_project = UserProject(user=user, project=project, role=UserProjectRole.ADMIN)
    project.user_project.append(user_project)
    db.session.add(user)
    db.session.commit()
    welcome_email(user)
    return jsonify(user_schema.dump(user)), 201


@auth.route('/auth/verify/<token>', methods=['POST'])
def verify_email(token):
    user = User.query.filter_by(email_verification_token=token).scalar()
    if not user:
        return jsonify({'error': 'invalid token'}), 400
    user.email_verified = True
    db.session.add(user)
    db.session.commit()
    email_verified(user)
    return jsonify(user_schema.dump(user)), 200


@auth.route('/auth/resend', methods=['POST'])
def resend_email():
    body = request.get_json()
    if not body or not body.get('email'):
        return jsonify({'error': 'Email required.'}), 400
    user = User.query.filter_by(email=body.get('email')).scalar()
    if not user:
        return jsonify({'error': 'Email is not registered with us.'}), 400
    welcome_email(user)
    return jsonify({'result': True}), 200
