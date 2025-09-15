from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_login import current_user, login_required, login_user, logout_user, login_manager
from passlib.hash import sha256_crypt

from Authentication_service.Authentication_api import db
from ..models import User
from . import user_blueprint


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Bearer ', '')
        user = User.query.filter_by(api_key=api_key).first()
        return user
    return None



def hash_password(password):
    return sha256_crypt.hash(password)


def verify_password(password, hashed):
    return sha256_crypt.verify(password, hashed)



@user_blueprint.route('/api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and verify_password(password, user.password):
        user.encode_api_key()
        db.session.commit()
        login_user(user, remember=True)
        return jsonify({"message": "Login successful", "api_key": user.api_key})

    return jsonify({"message": "Invalid credentials"}), 401


@user_blueprint.route('/api/logout', methods=['POST'])
@jwt_required()
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({"message": "Logout successful"})
    return jsonify({"message": "User not authenticated"}), 401


@user_blueprint.route('/api/register', methods=['POST'])
def register():
    data = request.get_json(force=True)
    required_fields = ['email', 'username', 'first_name', 'last_name', 'password']

    for field in required_fields:
        if not data.get(field):
            return jsonify({"message": f"{field} is required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = hash_password(data['password'])
    user = User(
        email=data['email'],
        username=data['username'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=hashed_password,
        is_authenticated=True,
        is_admin=True
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": user.serialize()}), 201

@user_blueprint.route('/api/users', methods=['GET'])
@jwt_required()
@login_required
def get_all_users():
    users = [user.serialize() for user in User.query.all()]
    return jsonify(users)


@user_blueprint.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
@login_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize())


@user_blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@login_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json(force=True)
    allowed_fields = ['email', 'username', 'first_name', 'last_name', 'password']

    for field in allowed_fields:
        if field in data:
            if field == 'password':
                user.password = hash_password(data['password'])
            else:
                setattr(user, field, data[field])

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.serialize()}), 200


@user_blueprint.route('/api/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200
