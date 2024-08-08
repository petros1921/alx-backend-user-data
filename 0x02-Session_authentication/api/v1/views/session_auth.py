#!/usr/bin/env python3
"""Module of session authenticating views.
"""

from flask import request, jsonify
from api.v1.views import app_views
from models.user import User  # Import the User model
from api.v1.app import auth

@app_views.route('/auth_session/login', methods=['POST'])
def session_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(name=os.getenv('SESSION_NAME'), value=session_id)

    return response