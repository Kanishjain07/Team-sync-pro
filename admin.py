from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from model import Message, Project, SystemLog, db, User
from role_required import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'Admin':
        return jsonify({'error': 'Unauthorized access'}), 403

    total_users = User.query.count()
    active_projects = Project.query.filter_by(is_active=True).count()
    messages_today = Message.query.filter(
        db.func.date(Message.timestamp) == datetime.utcnow().date()
    ).count()

    stats = {
        'total_users': total_users,
        'active_projects': active_projects,
        'messages_today': messages_today
    }
    return jsonify({'stats': stats}), 200

@admin_bp.route('/manage_users')
@login_required
@role_required('Admin')
def manage_users():
    users = User.query.all()
    user_data = [
        {
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role
        } for u in users
    ]
    return jsonify({'users': user_data}), 200

@admin_bp.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('Admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)

    db.session.commit()
    return jsonify({'message': 'User updated successfully'}), 200

@admin_bp.route('/delete_user/<int:user_id>', methods=['DELETE'])
@login_required
@role_required('Admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    new_log = SystemLog(username=current_user.username, action=f"Deleted user {user.username}")
    db.session.add(new_log)

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@admin_bp.route('/system_logs')
@login_required
@role_required('Admin')
def system_logs():
    logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).all()
    log_data = [
        {
            'id': log.id,
            'username': log.username,
            'action': log.action,
            'timestamp': log.timestamp.isoformat()
        } for log in logs
    ]
    return jsonify({'logs': log_data}), 200
