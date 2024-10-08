#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        # Get all plants
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant:
            return jsonify(plant.to_dict())
        return {'message': 'Plant not found'},404

    def post(self):
        # Create a new plant
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')
       

if __name__ == '__main__':
    app.run(port=5555, debug=True)
