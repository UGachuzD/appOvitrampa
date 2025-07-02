from flask import Blueprint, request, jsonify
from .utils import load_users, save_users, verify_password, hash_password, generate_token
from flask import jsonify
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    users = load_users()
    user = next((u for u in users if u['email'] == email), None)
    
    if not user or not verify_password(password, user['password_hash']):
        return jsonify({'msg': 'Credenciales inválidas'}), 401

    token = generate_token(email)
    return jsonify({'access_token': token})


@auth_bp.route('/change-password', methods=['POST'])
def change_password():
    data = request.json
    email = data.get('email')
    old_pass = data.get('old_password')
    new_pass = data.get('new_password')

    users = load_users()
    user = next((u for u in users if u['email'] == email), None)

    if not user or not verify_password(old_pass, user['password_hash']):
        return jsonify({'msg': 'Contraseña actual incorrecta'}), 401

    user['password_hash'] = hash_password(new_pass)
    save_users(users)
    return jsonify({'msg': 'Contraseña actualizada correctamente'})
