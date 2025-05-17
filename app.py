import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from sqlalchemy import asc, desc, nullslast

app = Flask(__name__)

app.secret_key = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)

    def __repr__(self):
        return f"<Task {self.title}>"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.context_processor
def inject_current_year():
    return {'SCRIPT_START_YEAR': datetime.utcnow().year}

# --- Routes ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    current_form_data = {} 
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        current_form_data['username'] = username 

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('register.html', current_form_data=current_form_data)
        if len(username) < 3:
            flash('Username must be at least 3 characters long.', 'danger')
            return render_template('register.html', current_form_data=current_form_data)
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'danger')
            return render_template('register.html', current_form_data=current_form_data)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'warning')
            return render_template('register.html', current_form_data=current_form_data)

        new_user = User(username=username)
        new_user.set_password(password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred during registration. Please try again.', 'danger')
            app.logger.error(f"Registration error: {e}")
            return render_template('register.html', current_form_data=current_form_data)
    return render_template('register.html', current_form_data=current_form_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    current_form_data = {}
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        current_form_data['username'] = username

        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('login.html', current_form_data=current_form_data)

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user) 
            flash(f'Welcome back, {user.username}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html', current_form_data=current_form_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    filter_status = request.args.get('filter_status', 'all')
    sort_by = request.args.get('sort_by', 'due_date') 
    sort_order = request.args.get('sort_order', 'asc')   

    query = Task.query.filter_by(user_id=current_user.id)

    if filter_status and filter_status != 'all':
        query = query.filter(Task.status == filter_status)

    order_expression = None
    if sort_by == 'due_date':
        order_expression = Task.due_date.asc().nullslast() if sort_order == 'asc' else Task.due_date.desc().nullslast()
    elif sort_by == 'status':
        order_expression = Task.status.asc() if sort_order == 'asc' else Task.status.desc()
    elif sort_by == 'title':
        order_expression = Task.title.asc() if sort_order == 'asc' else Task.title.desc()
    elif sort_by == 'created_at':
        order_expression = Task.created_at.asc() if sort_order == 'asc' else Task.created_at.desc()
    
    if order_expression is not None:
        query = query.order_by(order_expression)
    
    if sort_by != 'created_at':
        query = query.order_by(Task.created_at.desc())

    tasks = query.all()
    
    return render_template('dashboard.html', tasks=tasks,
                           current_filter_status=filter_status,
                           current_sort_by=sort_by,
                           current_sort_order=sort_order)

@app.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    current_task_data = {}
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        due_date_str = request.form.get('due_date')
        status = request.form.get('status', 'Pending')
        current_task_data = request.form.to_dict()

        if not title:
            flash('Task title is required.', 'danger')
            return render_template('add_edit_task.html', task=None, current_task_data=current_task_data, form_action_label="Add Task")

        due_date_obj = None
        if due_date_str:
            try:
                due_date_obj = date.fromisoformat(due_date_str)
            except ValueError:
                flash('Invalid due date format. Please use YYYY-MM-DD.', 'danger')
                return render_template('add_edit_task.html', task=None, current_task_data=current_task_data, form_action_label="Add Task")

        new_task = Task(title=title, description=description, due_date=due_date_obj, status=status, author=current_user)
        try:
            db.session.add(new_task)
            db.session.commit()
            flash('Task added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding task. Please try again.', 'danger')
            app.logger.error(f"Add task error: {e}")
            return render_template('add_edit_task.html', task=None, current_task_data=current_task_data, form_action_label="Add Task")
    return render_template('add_edit_task.html', task=None, current_task_data=current_task_data, form_action_label="Add Task")

@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        flash('Task not found.', 'danger')
        return redirect(url_for('dashboard'))
    if task.user_id != current_user.id:
        flash('You are not authorized to edit this task.', 'danger')
        return redirect(url_for('dashboard'))

    current_task_data = {}
    if request.method == 'POST':
        current_task_data = request.form.to_dict()
        task.title = request.form.get('title', '').strip()
        task.description = request.form.get('description', '').strip()
        due_date_str = request.form.get('due_date')
        task.status = request.form.get('status', 'Pending')

        if not task.title:
            flash('Task title is required.', 'danger')
            return render_template('add_edit_task.html', task=task, current_task_data=current_task_data, form_action_label="Save Changes")
        
        if due_date_str:
            try:
                task.due_date = date.fromisoformat(due_date_str)
            except ValueError:
                flash('Invalid due date format. Please use YYYY-MM-DD.', 'danger')
                return render_template('add_edit_task.html', task=task, current_task_data=current_task_data, form_action_label="Save Changes")
        else:
            task.due_date = None
        
        try:
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating task. Please try again.', 'danger')
            app.logger.error(f"Edit task error: {e}")
            return render_template('add_edit_task.html', task=task, current_task_data=current_task_data, form_action_label="Save Changes")
    else: 
        current_task_data = {
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.isoformat() if task.due_date else '',
            'status': task.status
        }
    return render_template('add_edit_task.html', task=task, current_task_data=current_task_data, form_action_label="Save Changes")

@app.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        flash('Task not found.', 'danger')
    elif task.user_id != current_user.id:
        flash('You are not authorized to delete this task.', 'danger')
    else:
        try:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting task. Please try again.', 'danger')
            app.logger.error(f"Delete task error: {e}")
    return redirect(url_for('dashboard'))

# Command to create database tables
@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables."""
    try:
        db.create_all()
        print("Initialized the database and created tables.")
    except Exception as e:
        print(f"Error initializing database: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
