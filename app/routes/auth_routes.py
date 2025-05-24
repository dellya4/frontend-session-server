from flask_mail import Message
from .. import mail
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models import User, db, TestResult, UserActionLog
import secrets
from datetime import datetime, timedelta
import os
from flask import current_app
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST']) #Route for add new user
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    birth_date_str = data.get('birth_date', '')

    birth_date = None
    if birth_date_str:
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid birth date format. Expected YYYY-MM-DD'}), 400

    if User.query.filter_by(username=username).first(): #Return error if username isn't unique
        return jsonify({'error': 'Username already exists'}), 400

    if User.query.filter_by(email=email).first(): #Return error if email isn't unique
        return jsonify({'error': 'Email already registered'}), 400

    hashed_password = generate_password_hash(password) #Generate hashed_password for security

    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        birth_date=birth_date,
    )

    db.session.add(new_user)
    db.session.commit()

    log = UserActionLog(
        user_id=new_user.id,
        action_type='register',
        description=f"{new_user.username} registered an account."
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'message': 'User registered successfully',
        'username': new_user.username,
        'email': new_user.email,
        'role': new_user.role
    }), 201


@auth_bp.route('/login', methods=['POST']) #Route for login
def login():
    data = request.get_json()
    identifier = data.get('username')  #This var can be username or email
    password = data.get('password')

    #Looking for username or email
    user = User.query.filter(
        (User.username == identifier) | (User.email == identifier)
    ).first()

    if not user or not check_password_hash(user.password, password): #Return error if user not in table or uncorrect password
        return jsonify({'error': 'Incorrect username or password'}), 401

    log = UserActionLog(
        user_id=user.id,
        action_type='login',
        description=f"{user.username} logged in."
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        'username': user.username,
        'email': user.email,
        'role': user.role
    }), 200


@auth_bp.route('/request-password-reset', methods=['POST']) #Route for reset password (Where user write email)
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user: #If we don't have this email in table, return error
        return jsonify({'error': 'User with this email not found'}), 404

    token = secrets.token_urlsafe(32) #Create secret token for person
    user.reset_token = token #Add in the db
    user.reset_token_expiration = datetime.utcnow() + timedelta(minutes=30)
    db.session.commit() #Save changes

    reset_link = f"http://localhost:3000/reset-password?token={token}"
    msg = Message('Reset Your Password', recipients=[email])
    msg.body = f'Click the link to reset your password: {reset_link}\nThis link is valid for 30 minutes.' #It is message which we send

    try:
        mail.send(msg)
        return jsonify({'message': 'Reset link sent to email'}), 200 #Try send message to user
    except Exception as e:
        return jsonify({'error': str(e)}), 500 #Return error if message isn't send


@auth_bp.route('/reset-password', methods=['POST']) #Route for reset password (Page where user write new password)
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('new_password')

    user = User.query.filter_by(reset_token=token).first()
    if not user or user.reset_token_expiration < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired token'}), 400

    user.password = generate_password_hash(new_password) #Generate new  hash password
    user.reset_token = None
    user.reset_token_expiration = None
    db.session.commit() #Save changes

    return jsonify({'message': 'Password successfully reset'}), 200


@auth_bp.route('/profile', methods=['GET']) #Route for showing profile
def get_profile():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({ #Return user's data
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
        'avatar_url': user.avatar_url,
        'theme': user.theme

    })


@auth_bp.route('/profile', methods=['PUT']) #Route for update data in profile
def update_profile():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user: #Return error if user is non
        return jsonify({'error': 'User not found'}), 404

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.theme = data.get('theme', user.theme)

    birth_date_str = data.get('birth_date')
    if birth_date_str:
        try:
            user.birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({'error': 'Invalid birth date format'}), 400

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})


@auth_bp.route('/profile/upload', methods=['POST']) #Route for upload avatar
def upload_avatar():
    if 'file' not in request.files or 'email' not in request.form:
        return jsonify({'error': 'Missing file or email'}), 400

    file = request.files['file']
    email = request.form['email']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    filename = secure_filename(file.filename)
    upload_dir = os.path.join(current_app.root_path, 'static/uploads')
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)

    user.avatar_url = f'http://127.0.0.1:5000/static/uploads/{filename}'
    db.session.commit()

    return jsonify({'message': 'Avatar uploaded', 'avatar_url': user.avatar_url})


@auth_bp.route('/admin/users', methods=['GET']) #Route for show users list
def get_users():
    users = User.query.with_entities(User.id, User.username, User.email, User.role).all()
    return jsonify([user._asdict() for user in users])


@auth_bp.route('/admin/users/<int:user_id>', methods=['DELETE']) #Route for delete user
def delete_user(user_id):
    requester_role = request.headers.get('X-User-Role', 'user')  # Check role

    if requester_role != 'superadmin':
        return jsonify({'error': 'Only superadmin can delete users'}), 403

    user = User.query.get(user_id)
    if user and user.role != 'superadmin':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200

    return jsonify({'error': 'Cannot delete superadmin or user not found'}), 403


@auth_bp.route('/admin/users/<int:user_id>', methods=['PUT']) #Route for change role
def update_user_role(user_id):
    data = request.get_json()
    new_role = data.get('role')
    requester_role = request.headers.get('X-User-Role', 'user')  #Check user's role

    if requester_role not in ['admin', 'superadmin']: #Return error if user doesn't have admin role
        return jsonify({'error': 'Only admin or superadmin can update roles'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.role = new_role
    db.session.commit()
    return jsonify({'message': f"User {user.username}'s role updated to {new_role}"}), 200


@auth_bp.route('/save-test-result', methods=['POST']) #Route for saving user's result
def save_test_result():
    data = request.get_json()
    user_email = data.get('email')
    test_type = data.get('test_type')
    score = data.get('score')

    user = User.query.filter_by(email=user_email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    result = TestResult(user_id=user.id, test_type=test_type, score=score)
    db.session.add(result)
    db.session.commit()

    log = UserActionLog(
        user_id=user.id,
        action_type='test_completed',
        description=f"{user.username} completed the {test_type.title()} test."
    )
    db.session.add(log)

    return jsonify({'message': 'Test result saved'}), 200


@auth_bp.route('/get-test-results', methods=['GET']) #Route for showing tests result
def get_test_results():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    results = TestResult.query.filter_by(user_id=user.id).order_by(TestResult.timestamp.asc()).all()
    data = [
        {
            'test_type': r.test_type,
            'score': r.score,
            'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M')
        } for r in results
    ]
    return jsonify(data), 200


@auth_bp.route('/log-action', methods=['POST']) #Route for dave users action
def log_action():
    data = request.get_json()
    email = data.get('email')
    action_type = data.get('action_type')
    description = data.get('description')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    log = UserActionLog(
        user_id=user.id,
        action_type=action_type,
        description=description
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({'message': 'Action logged'}), 200


@auth_bp.route('/admin/action-logs', methods=['GET']) #Route for show users action (only admin)
def get_action_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role_filter = request.args.get('role')
    search = request.args.get('search', '', type=str)

    query = UserActionLog.query.join(User)

    if role_filter:
        query = query.filter(User.role == role_filter)
    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))

    logs = query.order_by(UserActionLog.timestamp.desc()).paginate(page=page, per_page=per_page)

    data = [{
        'id': log.id,
        'username': log.user.username,
        'role': log.user.role,
        'action_type': log.action_type,
        'description': log.description,
        'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M')
    } for log in logs.items]

    return jsonify({
        'logs': data,
        'total': logs.total,
        'pages': logs.pages,
        'current_page': logs.page
    })
