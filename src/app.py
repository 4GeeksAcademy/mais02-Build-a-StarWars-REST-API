"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Vehicles, Favorites
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    favorites = Favorites.query.filter_by(user_id=user_id).all()
    return jsonify([fav.serialize() for fav in favorites]), 200





@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([p.serialize() for p in people]), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        raise APIException("Person not found", 404)
    return jsonify(person.serialize()), 200





@app.route('/vehicles', methods=['GET'])
def get_vehicles():
    vehicles = Vehicles.query.all()
    return jsonify([v.serialize() for v in vehicles]), 200


@app.route('/vehicles/<int:vehicle_id>', methods=['GET'])
def get_single_vehicle(vehicle_id):
    vehicle = Vehicles.query.get(vehicle_id)
    if vehicle is None:
        raise APIException("Vehicle not found", 404)
    return jsonify(vehicle.serialize()), 200





@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify([p.serialize() for p in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", 404)
    return jsonify(planet.serialize()), 200




@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)

    person = People.query.get(people_id)
    if not person:
        raise APIException("Person not found", 404)

    fav = Favorites(user_id=user_id, people_id=people_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify(fav.serialize()), 201


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['POST'])
def add_fav_vehicle(vehicle_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)

    vehicle = Vehicles.query.get(vehicle_id)
    if not vehicle:
        raise APIException("Vehicle not found", 404)

    fav = Favorites(user_id=user_id, vehicles_id=vehicle_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify(fav.serialize()), 201



@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)

    planet = Planets.query.get(planet_id)
    if not planet:
        raise APIException("Planet not found", 404)

    fav = Favorites(user_id=user_id, planets_id=planet_id)
    db.session.add(fav)
    db.session.commit()

    return jsonify(fav.serialize()), 201



@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_fav_people(people_id):
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        raise APIException("user_id is required", 400)

    fav = Favorites.query.filter_by(
        user_id=user_id,
        people_id=people_id
    ).first()

    if not fav:
        raise APIException("Favorite person not found", 404)

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Favorite person removed"}), 200


@app.route('/favorite/vehicle/<int:vehicle_id>', methods=['DELETE'])
def delete_fav_vehicle(vehicle_id):
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        raise APIException("user_id is required", 400)

    fav = Favorites.query.filter_by(
        user_id=user_id,
        vehicles_id=vehicle_id
    ).first()

    if not fav:
        raise APIException("Favorite vehicle not found", 404)

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Favorite vehicle removed"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_fav_planet(planet_id):
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        raise APIException("user_id is required", 400)

    fav = Favorites.query.filter_by(
        user_id=user_id,
        planets_id=planet_id
    ).first()

    if not fav:
        raise APIException("Favorite planet not found", 404)

    db.session.delete(fav)
    db.session.commit()

    return jsonify({"msg": "Favorite planet removed"}), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
