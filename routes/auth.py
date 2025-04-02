from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.db import execute_query

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.get_by_email(data['email']):
        return jsonify({"error": "Email already exists"}), 400

    hashed_pw = generate_password_hash(data['password'])
    execute_query(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (data['email'], hashed_pw)
    )
    
    user = User.get_by_email(data['email'])
    login_user(user)
    return jsonify({"message": "Registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.get_by_email(data['email'])
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"})