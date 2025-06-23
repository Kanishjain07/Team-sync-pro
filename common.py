from flask import Blueprint, jsonify
from flask_login import login_required
from model import Project

common_bp = Blueprint('common', __name__)

@common_bp.route('/notification')
@login_required
def notification():
    return jsonify({'message': 'Notification endpoint active'}), 200

@common_bp.route('/video_conference')
@login_required
def video_conference():
    return jsonify({'message': 'Video conference endpoint active'}), 200

@common_bp.route('/chat')
@login_required
def chat():
    return jsonify({'message': 'Chat endpoint active'}), 200

@common_bp.route('/file_upload')
@login_required
def file_upload():
    return jsonify({'message': 'File upload endpoint active'}), 200

@common_bp.route('/task_progress')
@login_required
def task_progress():
    return jsonify({'message': 'Task progress endpoint active'}), 200

@common_bp.route('/calendar')
@login_required
def calendar():
    return jsonify({'message': 'Calendar endpoint active'}), 200

@common_bp.route('/projects')
@login_required
def view_projects():
    projects = Project.query.all()
    project_list = [
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'status': p.status
        } for p in projects
    ]
    return jsonify({'projects': project_list}), 200
    