from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.models.ong import ONG
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión de una ONG y devuelve un token de acceso JWT.
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: PayloadLogin
          properties:
            name:
              type: string
              description: "El nombre de la ONG."
              example: "prueba_ong"
            password:
              type: string
              description: "La contraseña de la ONG."
              example: "password123"
    responses:
      200:
        description: Inicio de sesión exitoso, devuelve un token de acceso.
      400:
        description: Falta el nombre o la contraseña de la ONG.
      401:
        description: Nombre de ONG o contraseña incorrectos.
    """
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"msg": "Falta el nombre o la contraseña de la ONG"}), 400

    # Buscamos la ONG por su nombre
    ong = ONG.query.filter_by(name=name).first()

    # Verificamos si la ONG existe y si el hash de la contraseña coincide
    if ong and check_password_hash(ong.password, password):
        # Creamos el token de acceso, identificando al usuario por su ID
        access_token = create_access_token(identity=str(ong.id))
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Nombre de ONG o contraseña incorrectos"}), 401

@auth.route('/register', methods=['POST'])
def register():
    """
    Registra una nueva ONG en la base de datos.
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: PayloadRegistro
          properties:
            name:
              type: string
              description: "El nombre deseado para la nueva ONG."
              example: "prueba_ong"
            password:
              type: string
              description: "La contraseña para la nueva ONG."
              example: "password123"
    responses:
      201:
        description: ONG creada exitosamente.
      400:
        description: Falta el nombre o la contraseña de la ONG.
      409:
        description: El nombre de la ONG ya existe.
    """
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"msg": "Falta el nombre o la contraseña de la ONG"}), 400
    
    # Verificamos si ya existe una ONG con ese nombre
    if ONG.query.filter_by(name=name).first():
        return jsonify({"msg": "El nombre de la ONG ya existe"}), 409

    # Creamos un hash de la contraseña antes de guardarla
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    # Creamos la nueva instancia de la ONG
    new_ong = ONG(name=name, password=hashed_password)
    
    # Añadimos la nueva ONG a la sesión de la db y guardamos cambios
    db.session.add(new_ong)
    db.session.commit()

    return jsonify({"msg": "ONG creada exitosamente"}), 201