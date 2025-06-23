from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from role_required import role_required
from model import db, Project

project_bp = Blueprint('project', __name__, url_prefix='/project')

@project_bp.route('/all', methods=['GET'])
@login_required
@role_required(['Admin', 'Team Lead'])
def get_all_projects():
    projects = Project.query.all()
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'status': p.status
        } for p in projects
    ]), 200

@project_bp.route('/create', methods=['POST'])
@login_required
@role_required(['Admin', 'Team Lead'])
def create_project():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'active')

    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400

    project = Project(title=title, description=description, status=status)
    db.session.add(project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 201

@project_bp.route('/edit/<int:project_id>', methods=['PUT'])
@login_required
@role_required(['Admin', 'Team Lead'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)
    db.session.commit()
    return jsonify({'message': 'Project updated successfully'}), 200

@project_bp.route('/delete/<int:project_id>', methods=['DELETE'])
@login_required
@role_required(['Admin', 'Team Lead'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200
