"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
import requests


api = Blueprint('api', __name__)
CORS(api) # Allow CORS requests to this API


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():
    response_body = {}
    response_body["message"] = "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    return jsonify(response_body), 200

@api.route('/users', methods=['GET'])
def users():
    response_body = {}
    url = 'https://jsonplaceholder.typicode.com/users'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['message'] = 'Listado de usuarios'
        response_body['results'] = data
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400

@api.route("/login", methods=["POST"])
def login():
    response_body = {}
    data = request.json
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    row = db.session.execute(db.select(Users).where(Users.email==email, Users.password==password, Users.is_active)).scalar()
    # if the request is successful, row should return something (therefore is true), ifnot it will return none
    if not row:
        response_body['message'] = "Bad email or password"
        return response_body, 401
    Users = row.serialize()
    claims = {'user_id': row['id'],
              'is_admin': row['is_admin']}
    print(claims)

    access_token = create_access_token(identity=email, additional_claims=claims)
    response_body['message'] = 'User logged!'
    response_body['access_token'] = access_token
    return response_body, 200

# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    response_body = {}
    current_user = get_jwt_identity()
    additional_claims = get_jwt()
    response_body['message'] = f'User logged: {current_user} - {additional_claims}'
    return response_body, 200

@api.route('/users/<int:user_id>', methods=['GET'])
def user_id(user_id):
    response_body = {}
    url = f'https://jsonplaceholder.typicode.com/users/{user_id}'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['message'] = 'Un usuario'
        response_body['results'] = data
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400

@api.route('/users/<int:user_id>/favorite-planets', methods=['POST'])
def favorite_planets(user_id):
    response_body = {}
    if request.method == 'POST':
        data = request.json()  
        row = 
        response_body['message'] = 'Planet addedd to favorite'
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400

@api.route('/characters', methods=['GET'])
def characters():
    response_body = {}
    url = 'https://swapi.tech/api/people'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['message'] = 'List of characters'
        response_body['results'] = data['results']
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400

@api.route('/characters/<int:character_id>', methods=['GET'])
def character_id(character_id):
    response_body = {}
    url = f'https://swapi.tech/api/people/{character_id}'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['message'] = 'One Character'
        response_body['results'] = data['result']['properties']
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400

@api.route('/planets', methods=['GET'])
def planets():
    response_body = {}
    url = 'https://swapi.tech/api/planets'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['message'] = 'List of Planets'
        response_body['results'] = data['results']
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400

@api.route('/planets/<int:planet_id>', methods=['GET'])
def planet_id(planet_id):
    response_body = {}
    url = f'https://swapi.tech/api/planets/{planet_id}'
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        data = response.json()
        response_body['message'] = 'One planet'
        response_body['results'] = data['result']['properties']
        return response_body, 200
    response_body['message'] = 'algo salió'
    return response_body, 400