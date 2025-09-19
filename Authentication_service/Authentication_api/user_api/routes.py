from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from passlib.hash import sha256_crypt

from .. import db
from ..models import User
from . import user_blueprint



def hash_password(password):
    return sha256_crypt.hash(password)


def verify_password(password, hashed):
    return sha256_crypt.verify(password, hashed)


@user_blueprint.route('/user_api/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and verify_password(password, user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": user.serialize()
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


@user_blueprint.route('/user_api/register', methods=['POST'])
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
        is_admin=False
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user": user.serialize()}), 201



@user_blueprint.route('/user_api/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = [user.serialize() for user in User.query.all()]
    return jsonify(users), 200


@user_blueprint.route('/user_api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200


@user_blueprint.route('/user_api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
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


@user_blueprint.route('/user_api/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user.serialize()), 200
