from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from model import db, User, Project
from role_required import role_required

lead_bp = Blueprint('lead', __name__, url_prefix='/lead')

@lead_bp.route('/dashboard', methods=['GET'])
@login_required
@role_required('Team Lead')
def dashboard():
    total_members = User.query.filter_by(role='Member').count()
    team_projects = Project.query.all()  # Optional: filter by assigned lead if you implement assignment

    return jsonify({
        'message': 'Team Lead Dashboard',
        'total_members': total_members,
        'total_projects': len(team_projects)
    }), 200
