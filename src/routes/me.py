from flask import request, jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required

from database.db import db
from database.project import Project
from database.user import User, user_schema
from database.user_project import UserProject
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


@me.route('/me/subquery', methods=['GET'])
def subquery_test():
    # user_id = get_jwt_identity()
    subquery = db.session.query(UserProject.user_id).filter(UserProject.user_id == 1).subquery()
    query = db.session.query(Project).filter(Project.project_id.in_(subquery))
    print(query)
    return jsonify({'result': query})
