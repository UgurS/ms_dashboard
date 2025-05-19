from flask import Blueprint, request, jsonify
from backend.services.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    result, error = auth_service.login(data['username'], data['password'])
    if error:
        return jsonify({"message": error}), 401
    return jsonify(result), 200


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    old_refresh_token = data.get('refresh_token')
    result, error = auth_service.refresh_session(old_refresh_token)
    if error:
        return jsonify({"message": error}), 401
    return jsonify(result), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    auth_service.logout(refresh_token)
    return jsonify({"message": "Logged out"}), 200