from flask import Flask, request, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import secrets
from dotenv import load_dotenv
import pymysql

from model import Message, Project, SystemLog, db, User
from auth import auth_bp
from admin import admin_bp
from common import common_bp
from role_required import role_required
from lead import lead_bp
pymysql.install_as_MySQLdb()
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/team_sync'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

API_KEY = os.getenv("API_KEY", secrets.token_hex(32))


app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(common_bp)
app.register_blueprint(lead_bp)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Team Sync Pro '}), 200

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    role = current_user.role.lower()
    if role == 'admin':
        return redirect(url_for('admin.dashboard'))
    elif role == 'team lead':
        return redirect(url_for('lead_dashboard'))
    elif role == 'member':
        return redirect(url_for('member_dashboard'))
    else:
        return jsonify({'error': 'Unauthorized Role'}), 403

@app.route('/lead/dashboard', methods=['GET'])
@login_required
@role_required('Team Lead')
def lead_dashboard():
    return jsonify({'message': 'Welcome to Team Lead Dashboard'}), 200

@app.route('/member/dashboard', methods=['GET'])
@login_required
@role_required('Member')
def member_dashboard():
    return jsonify({'message': 'Welcome to Member Dashboard'}), 200

@app.route('/create_project', methods=['POST'])
@login_required
@role_required(['Admin', 'Team Lead'])
def create_project():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')

    new_project = Project(title=title, description=description, status=status)
    db.session.add(new_project)
    db.session.commit()

    return jsonify({'message': 'Project created successfully'}), 201

@app.route('/edit_project/<int:project_id>', methods=['PUT'])
@login_required
@role_required(['Admin', 'Team Lead'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    data = request.json

    project.title = data.get('title', project.title)
    project.description = data.get('description', project.description)
    project.status = data.get('status', project.status)

    db.session.commit()
    return jsonify({'message': 'Project updated successfully'}), 200

@app.route('/delete_project/<int:project_id>', methods=['DELETE'])
@login_required
@role_required(['Admin', 'Team Lead'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully'}), 200

with app.app_context():
    db.create_all()
    print("✅ Connected to MySQL and tables created.")

if __name__ == '__main__':
    app.run(debug=True)
