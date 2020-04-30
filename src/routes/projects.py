from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database.db import db
from database.incident import Incident, incident_schema
from database.incident_update import IncidentUpdate, IncidentUpdateSchema
from database.project import Project, project_schema
from database.project_invite import ProjectInvite, project_invite_schema
from database.user import User, short_user_schema
from database.user_project import UserProject, UserProjectRole
from notifications.email import send_invite_member
from utils import random_str

projects = Blueprint('projects', __name__)


@projects.route('/projects', methods=['GET'])
@jwt_required
def get_projects():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).scalar()
    return jsonify(project_schema.dump(user.projects, many=True))


@projects.route('/projects', methods=['POST'])
@jwt_required
def create_project():
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    body = request.get_json()
    project = Project(**body)
    user_project = UserProject(user=user, project=project, role=UserProjectRole.ADMIN)
    project.user_project.append(user_project)
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict())


@projects.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required
def update_project(project_id):
    user_id = get_jwt_identity()
    body = request.get_json()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    Project.query.filter_by(project_id=project_id).update(body)
    db.session.commit()
    print(body)
    return jsonify({'result': True})


@projects.route('/projects/<int:project_id>', methods=['GET'])
@jwt_required
def read(project_id):
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    return jsonify(project.to_dict())


@projects.route('/projects/<int:project_id>', methods=['PUT'])
@jwt_required
def update(project_id):
    new_name = request.json['name']
    project = Project.query.get(project_id)
    if not project:
        return {'error': 'Project not found'}, 400
    project.name = new_name
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict())


@projects.route('/projects/<int:project_id>', methods=['DELETE'])
@jwt_required
def delete(project_id):
    project = Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'result': True})


@projects.route('/projects/<int:project_id>/incidents', methods=['GET'])
def get_incidents(project_id):
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    status = request.args.get('status')
    detailed = request.args.get('detailed')
    if status is not None:
        incidents = Incident.query.filter_by(project_id=project_id, status=status)
    else:
        incidents = Incident.query.filter_by(project_id=project_id)
    return jsonify(incident_schema.dump(incidents, many=True))


@projects.route('/projects/<int:project_id>/incidents/<int:incident_id>', methods=['GET'])
def get_incident_updates(project_id, incident_id):
    incident = Incident.query.filter_by(incident_id=incident_id).first_or_404()
    updates = IncidentUpdate.query.filter_by(incident_id=incident_id).all()
    incident_update_schema = IncidentUpdateSchema()
    return jsonify({
        'incident': incident_schema.dump(incident),
        'updates': incident_update_schema.dump(updates, many=True)
    })


@projects.route('/projects/<int:project_id>/incidents/<int:incident_id>/updates', methods=['POST'])
@jwt_required
def add_incident_update(project_id, incident_id):
    user_id = get_jwt_identity()
    body = request.get_json()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    incident = Incident.query.filter_by(incident_id=incident_id).first_or_404()
    update = IncidentUpdate(incident_id=incident_id, message=body['message'], status=body['status'])
    incident.updates.append(update)
    db.session.add(incident)
    db.session.commit()
    return jsonify({'result': True})


@projects.route('/projects/<int:project_id>/incidents/<int:incident_id>/updates/<int:update_id>', methods=['DELETE'])
@jwt_required
def delete_incident_update(project_id, incident_id, update_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    update = IncidentUpdate.query.filter_by(update_id=update_id).first_or_404()
    db.session.delete(update)
    db.session.commit()
    return jsonify({'result': True})


@projects.route('/projects/<int:project_id>/incidents/<int:incident_id>', methods=['PUT'])
@jwt_required
def update_incident(project_id, incident_id):
    user_id = get_jwt_identity()
    body = request.get_json()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    incident = Incident.query.filter_by(incident_id=incident_id).first_or_404()
    incident.status = body['status'] or 'OPEN'
    db.session.add(incident)
    db.session.commit()
    return jsonify(incident_schema.dump(incident))


@projects.route('/projects/<int:project_id>/incidents', methods=['POST'])
@jwt_required
def create_incident(project_id):
    user_id = get_jwt_identity()
    body = request.get_json()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    new_incident = Incident(
        name=body['name'],
        components=body['components'],
        status='OPEN',
        project_id=project_id,
        author_id=user_id)
    incident_update = IncidentUpdate(
        status=body['status'],
        message=body['message']
    )
    new_incident.updates.append(incident_update)
    project.incidents.append(new_incident)
    db.session.add(project)
    db.session.commit()
    return jsonify(short_user_schema.dump(project.incidents, many=True))


@projects.route('/projects/<int:project_id>/components', methods=['GET'])
@jwt_required
def get_components(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))


@projects.route('/projects/<int:project_id>/subscribers', methods=['GET'])
@jwt_required
def get_subscribers(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401
    return jsonify(short_user_schema.dump(project.members, many=True))


@projects.route('/projects/<int:project_id>/members', methods=['GET'])
@jwt_required
def get_project_members(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401

    response = []
    for up in project.user_project:
        res = short_user_schema.dump(up.user)
        res.update({'role': up.role.value})
        response.append(res)
    return jsonify(response)


@projects.route('/projects/<int:project_id>/invites', methods=['POST'])
@jwt_required
def invite_member(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401

    # Create invite
    body = request.get_json()
    token = random_str()
    invite = ProjectInvite(
        sender_id=user_id, project_id=project_id, token=token,
        email=body['email'], message=body['message'], role=body['role'],
    )
    db.session.add(invite)
    db.session.commit()

    # Send email
    send_invite_member(user, body['email'], token, body['message'])

    # Construct response
    return jsonify(project_invite_schema.dump(invite))


@projects.route('/projects/<int:project_id>/invites', methods=['GET'])
@jwt_required
def get_invites(project_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401

    # Get invites
    invites = ProjectInvite.query.filter_by(project_id=project_id).all()
    return jsonify(project_invite_schema.dump(invites, many=True))


@projects.route('/projects/<int:project_id>/invites/<int:invite_id>', methods=['DELETE'])
@jwt_required
def delete_invite(project_id, invite_id):
    user_id = get_jwt_identity()
    user = User.query.filter_by(user_id=user_id).first_or_404()
    project = Project.query.filter_by(project_id=project_id).first_or_404()
    if user not in project.members:
        return jsonify({'error': 'You dont have rights.'}), 401

    # Get invites
    invite = ProjectInvite.query.filter_by(invite_id=invite_id).first_or_404()
    db.session.delete(invite)
    db.session.commit()
    return jsonify({'result': True})


def is_id_exist(project_id):
    return db.session.query(Project.project_id).filter_by(project_id=project_id).scalar() is not None
