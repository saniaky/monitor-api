import datetime

from flask import request, Blueprint
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from database.db import db
from database.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    user = User.query.filter_by(email=body.get('email')).first()
    if not user:
        return {'error': 'User is not found'}, 400
    authorized = user.check_password(body.get('password'))
    if not authorized:
        return {'error': 'Email or password invalid'}, 401
    expires7days = datetime.timedelta(days=7)
    expires30days = datetime.timedelta(days=30)
    access_token = create_access_token(identity=str(user.user_id), expires_delta=expires7days)
    refresh_token = create_access_token(identity=str(user.user_id), expires_delta=expires30days)
    return {'access_token': access_token, 'refresh_token': refresh_token}, 200


@auth.route('/register', methods=['POST'])
def register():
    body = request.get_json()
    user = User(**body)
    user.hash_password()
    db.session.add(user)
    db.session.commit()
    return {'id': user.user_id}


@auth.route('/me', methods=['GET'])
@jwt_required
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return {'error': 'User does not exist anymore.'}
    return {'id': user.user_id, 'email': user.email}
