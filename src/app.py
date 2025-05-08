import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planets, Films, Favorites

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Error handler
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# ------------------ USERS ------------------

@app.route('/users', methods=['POST'])
def create_user():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "No input data provided"}), 400

    email = body.get("email")
    password = body.get("password")
    is_active = body.get("is_active", True)

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 409

    new_user = User(email=email, password=password, is_active=is_active)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully", "user": new_user.serialize()}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    if len(users) < 1:
        return jsonify({"msg": "not found"}), 404
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize()), 200

# ------------------ PLANETS ------------------

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    if len(planets) < 1:
        return jsonify({"msg": "not found"}), 404
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_by_id(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# ------------------ CHARACTERS ------------------

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    if len(characters) < 1:
        return jsonify({"msg": "not found"}), 404
    return jsonify([char.serialize() for char in characters]), 200

@app.route('/characters/<int:char_id>', methods=['GET'])
def get_character_by_id(char_id):
    char = Character.query.get(char_id)
    if not char:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(char.serialize()), 200

# Crear un nuevo personaje
@app.route('/characters', methods=['POST'])
def create_character():
    body = request.get_json()
    if not body:
        return jsonify({"msg": "No input data provided"}), 400

    try:
        new_character = Character(
            name=body["name"],
            eye_color=body["eye_color"],
            hair_color=body["hair_color"]
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify({"msg": "Character created successfully", "character": new_character.serialize()}), 201
    except KeyError as e:
        return jsonify({"msg": f"Missing field: {str(e)}"}), 400

# Editar un personaje existente
@app.route('/characters/<int:char_id>', methods=['PUT'])
def update_character(char_id):
    body = request.get_json()
    if not body:
        return jsonify({"msg": "No input data provided"}), 400

    character = Character.query.get(char_id)
    if character is None:
        return jsonify({"msg": f"Character with id {char_id} not found"}), 404

    for key, value in body.items():
        if hasattr(character, key):
            setattr(character, key, value)

    db.session.commit()
    return jsonify({"msg": "Character updated successfully", "character": character.serialize()}), 200

# ------------------ FILMS ------------------

@app.route('/films', methods=['GET'])
def get_films():
    films = Films.query.all()
    if len(films) < 1:
        return jsonify({"msg": "not found"}), 404
    return jsonify([film.serialize() for film in films]), 200

@app.route('/films/<int:film_id>', methods=['GET'])
def get_film_by_id(film_id):
    film = Films.query.get(film_id)
    if not film:
        return jsonify({"msg": "Film not found"}), 404
    return jsonify(film.serialize()), 200

# ------------------ FAVORITES ------------------

@app.route('/favorites', methods=['POST'])
def add_favorite():
    body = request.get_json()

    favorite = Favorites(
        user_id=body["user_id"],
        character_id=body.get("character_id"),
        planets_id=body.get("planets_id"),
        films_id=body.get("films_id")
    )

    if not favorite.character_id and not favorite.planets_id and not favorite.films_id:
        return jsonify({"msg": "Must provide at least one type of favorite"}), 400

    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    if not favorite:
        return jsonify({"msg": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user.serialize_favorites()), 200

# ------------------ MAIN ------------------

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)