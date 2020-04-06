import datetime

from flask import request, Blueprint, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from database.db import db
from database.user import User
from routes.auth_validation import RegisterSchema

auth = Blueprint('auth', __name__)

register_schema = RegisterSchema()


@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    errors = register_schema.validate(body)
    if errors:
        return jsonify({'error': errors})
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
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@auth.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    errors = register_schema.validate(body)
    if errors:
        return jsonify({'error': errors})
    user = User(**body)
    user.hash_password()
    db.session.add(user)
    db.session.commit()
    return {'id': user.user_id}, 201


@auth.route('/me', methods=['GET'])
@jwt_required
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user: return {'error': 'User does not exist anymore.'}, 400
    return {'id': user.user_id, 'email': user.email}
