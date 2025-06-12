from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user
from role_required import role_required 
from datetime import datetime

import pymysql
pymysql.install_as_MySQLdb()

from model import Message, Project, SystemLog, db, User  
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/team_sync'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin':
        
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
        return render_template('admin_dashboard.html', stats=stats)

    elif current_user.role == 'Team Lead':
        return render_template('lead_dashboard.html')
    
    else:
        return render_template('member_dashboard.html')

@app.route('/lead/dashboard')
@login_required
@role_required('Team Lead')
def lead_dashboard():
    return render_template('team_lead_dashboard.html')

@app.route('/member/dashboard')
@login_required
@role_required('Member')
def member_dashboard():
    return render_template('member_dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Invalid email or password.', 'danger')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered. Please log in.', 'danger')
            return redirect(url_for('login'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(username=username, email=email, password=hashed_password)
        role = request.form['role']
        new_user = User(username=username, email=email, password=hashed_password, role=role)

        
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/notification')
@login_required
def notification():
    return render_template('notification.html')

@app.route('/video_conference')
@login_required
def video_conference():
    return render_template('video_conference.html')
@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/file_upload')
@login_required
def file_upload():
    return render_template('file_upload.html')

@app.route('/task_progress')
@login_required
def task_progress():
    return render_template('task_progress.html')

@app.route('/calendar')
@login_required
def calendar():
    return render_template('calendar.html')

@app.route('/manage_users')
@login_required
@role_required('Admin')
def manage_users():
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@role_required('Admin')
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('manage_users'))

    return render_template('edit_user.html', user=user)


@app.route('/delete_user/<int:user_id>')
@login_required
@role_required('Admin')
def delete_user(user_id):
    new_log = SystemLog(username=current_user.username, action=f"Deleted user {user.username}")
    db.session.add(new_log)
    db.session.commit()
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('manage_users'))

@app.route('/system_logs')
@login_required
@role_required('Admin')
def system_logs():
    logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).all()
    return render_template('system_logs.html', logs=logs)

@app.route('/projects')
@login_required
def view_projects():
    projects = Project.query.all()  
    return render_template('project.html', projects=projects)

@app.route('/create_project', methods=['GET', 'POST'])
@login_required
@role_required(['Admin', 'Team Lead'])
def create_project():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']

        new_project = Project(title=title, description=description, status=status)
        db.session.add(new_project)
        db.session.commit()

        flash('Project created successfully!', 'success')
        return redirect(url_for('view_projects'))

    return render_template('create_project.html')

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
@role_required(['Admin', 'Team Lead'])
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.status = request.form['status']

        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('view_projects'))

    return render_template('edit_project.html', project=project)

@app.route('/delete_project/<int:project_id>')
@login_required
@role_required(['Admin', 'Team Lead'])
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()

    flash('Project deleted successfully!', 'success')
    return redirect(url_for('view_projects'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()
    print("✅ Connected to MySQL and tables created.")

if __name__ == '__main__':
    app.run(debug=True)
