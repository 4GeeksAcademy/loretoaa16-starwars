"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, PlanetFavorites, CharacterFavorites
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

@api.route('/users/<int:user_id>/favorite-character', methods=['POST', 'DELETE'])
def favorite_character(user_id):
    print(user_id)
    response_body = {}
    if request.method == 'POST':
        data = request.json
        print(data)
        row = CharacterFavorites(user_id=user_id, character_id=data['character_id'])
        db.session.add(row)
        db.session.commit()
        response_body['message'] = 'Character addedd to favorite'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        data = request.json
        print(data)
        row = CharacterFavorites.query.filter_by(user_id=user_id, character_id=data['character_id']).first()
        if not row:
            return {"message": "Favorite character not found"}, 404  # Return 404 if not found
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = 'Character deleted from favorite'
        response_body['results'] = row.serialize()
        return response_body, 200
    response_body['message'] = 'unexpected error'
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

@api.route('/users/<int:user_id>/favorite-planet', methods=['POST', 'DELETE'])
def favorite_planet(user_id):
    print(user_id)
    response_body = {}
    if request.method == 'POST':
        data = request.json
        print(data)
        row = PlanetFavorites(user_id=user_id, planet_id=data['planet_id'])
        db.session.add(row)
        db.session.commit()
        response_body['message'] = 'Planet addedd to favorite'
        response_body['results'] = row.serialize()
        return response_body, 200
    if request.method == 'DELETE':
        data = request.json
        print(data)
        row = PlanetFavorites.query.filter_by(user_id=user_id, planet_id=data['planet_id']).first()
        if not row:
            return {"message": "Favorite planet not found"}, 404  # Return 404 if not found
        db.session.delete(row)
        db.session.commit()
        response_body['message'] = 'Planet deleted from favorite'
        response_body['results'] = row.serialize()
        return response_body, 200
    response_body['message'] = 'unexpected error'
    return response_body, 400

@api.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    response_body = {}

    # Query favorite characters
    character_favorites = CharacterFavorites.query.filter_by(user_id=user_id).all()
    characters = [fav.serialize() for fav in character_favorites]

    # Query favorite planets
    planet_favorites = PlanetFavorites.query.filter_by(user_id=user_id).all()
    planets = [fav.serialize() for fav in planet_favorites]

    # Prepare response
    response_body['message'] = 'Favorites retrieved successfully'
    response_body['favorites'] = {
        'characters': characters,
        'planets': planets
    }

    return jsonify(response_body), 200