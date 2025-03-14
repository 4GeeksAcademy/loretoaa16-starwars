"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from api.models import db, Users, PlanetFavorites, CharacterFavorites, Followers
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
    response_body = { }
    rows = db.session.execute(db.select(Users)).scalars()  #Scalars devuelve una lista
    # Opcion 1 : Standard
    """ results = []
    for row in rows:
        results.append(row.serialize()) """
    # Opcion 2 : Comprension de listas - Se usa más que la opción 1
    # Variable = [ target for indivivdual en iterables ]
    results = [ row.serialize() for row in rows ]
    response_body["message"] = f'Listado de Usuarios'
    response_body["results"] = results
    return(response_body), 200

@api.route('/users', methods=['POST'])
def register_user():
    response_body = {}
    data = request.json
    print("soy el data de register", data)
    
    row = Users(first_name=data.get('first_name', ""), last_name=data.get('last_name', ""), email=data['email'], password=data['password'], is_admin=data.get('is_admin', False))
    db.session.add(row)
    db.session.commit()
    
    user = row.serialize()
    claims = {'user_id': user['id'],
              'is_admin': user['is_admin']}
    print(claims)

    access_token = create_access_token(identity=user["email"], additional_claims=claims)
    response_body['message'] = 'User registered!'
    response_body['access_token'] = access_token
    response_body['results'] = user
    return response_body, 200

@api.route('/users2', methods=['PUT'])
@jwt_required()
def prueba():
    response_body = {}
    claims = get_jwt()['user_id']
    response_body['usuario']=claims
    """ data = claims.user_id """
    return response_body, 200

@api.route('/users', methods=['PUT'])
@jwt_required()
def edit_user():
    response_body = {}
    data = request.json
    user_id = get_jwt()['user_id']
    print("soy el data de edit user", data)
    print("soy el userid de edit", user_id)
    row = Users.query.get(user_id)
    print("soy el print de row serialize", row.serialize())
    if not row:
        response_body['message'] = 'User not found'
        return response_body, 404
    row.first_name = data.get('first_name', row.first_name)  # Use .get() to avoid KeyError
    row.last_name = data.get('last_name', row.last_name)
    row.email = data.get('email', row.email)
    row.password = data.get('password', row.password)  # Ideally, hash the password before saving
    row.is_admin = data.get('is_admin', row.is_admin)
    db.session.commit()
    response_body['message'] = 'User edited'
    response_body['results'] = row.serialize()
    return response_body, 200

@api.route("/login", methods=["POST"])
def login():
    response_body = {}
    data = request.json
    print("soy data de login", data)
    email = data.get("email", None)
    password = data.get("password", None)
    row = db.session.execute(db.select(Users).where(Users.email==email, Users.password==password, Users.is_active)).scalar()
    # if the request is successful, row should return something (therefore is true), ifnot it will return none
    if not row:
        response_body['message'] = "Bad email or password"
        return response_body, 401
    user = row.serialize()
    claims = {'user_id': user['id'],
              'is_admin': user['is_admin']}
    print(claims)

    access_token = create_access_token(identity=email, additional_claims=claims)
    response_body['message'] = 'User logged!'
    response_body['access_token'] = access_token
    response_body['results'] = user
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

@api.route('/followers', methods=['POST'])
@jwt_required()
def followers():
    response_body = {}
    additional_claims = get_jwt() #datos adicionales
    follower = additional_claims['user_id']
    following = request.json.get('following_id')

    #valido si ya existe la relacion de seguido y seguidor
    foo = db.session.execute(db.select(Followers).where(Followers.follower_id==follower, Followers.following_id==following)).scalar()
    if foo:
        response_body, 400
    #un usuario no se puede seguir a si mismo
    if follower == following:
        response_body['message'] = 'Error: you cannot follow yourself'
        return response_body, 400

    #agrego la db lo que me están enviando
    row = Followers(follower_id=follower,
                    following_id=following)
    db.session.add(row)
    db.session.commit()
    response_body['message'] = f'followers added'
    response_body['results'] = row.serialize()
    return response_body, 200