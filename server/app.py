#!/usr/bin/env python3

from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api, reqparse
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class RestaurantResource(Resource):
    def get(self, id=None):
        if id != None:
            restaurant = Restaurant.query.filter_by(id=id).first()
            # restaurant["restaurant_pizzas"] = (
            #     RestaurantPizza.query.filter_by(restaurant=id).first().to_dict()
            # )
            if restaurant != None:
                return restaurant.to_dict(), 200
            return {"error": "Restaurant not found"}, 404
        else:
            answer = [
                {
                    "address": restaurant.to_dict()["address"],
                    "id": restaurant.to_dict()["id"],
                    "name": restaurant.to_dict()["name"],
                }
                for restaurant in Restaurant.query.all()
            ]
            return answer, 200

    def delete(self, id):
        Restaurant.query.filter_by(id=id)

        if Restaurant.query.filter_by(id=id).delete():

            restauran = RestaurantPizza.query.filter_by(restaurant_id=id)
            if RestaurantPizza.query.filter_by(restaurant_id=id).delete():
                Pizza.query.filter_by(id=restauran.first().pizza_id).delete()
                restauran.delete()

            db.session.commit()
            return {}, 204
        return {"error": "Restaurant not found"}, 404


class PizzaResource(Resource):
    def get(self):
        return [pizza.to_dict() for pizza in Pizza.query.all()], 200


class Restaurant_pizzasResource(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            for keyed in ["price", "pizza_id", "restaurant_id"]:

                parser.add_argument(keyed, required=True, help=f"Missing {keyed}")

            args = parser.parse_args()

            new_restaurant_pizza = RestaurantPizza(
                price=int(args.get("price")),
                pizza_id=args.get("pizza_id"),
                restaurant_id=args.get("restaurant_id"),
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            return RestaurantPizza.query.first().to_dict(), 201
        except ValueError as e:
            return e, 500


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"


api.add_resource(RestaurantResource, "/restaurants", "/restaurants/<int:id>")
api.add_resource(PizzaResource, "/pizzas")
api.add_resource(Restaurant_pizzasResource, "/restaurant_pizzas")
if __name__ == "__main__":
    app.run(port=5555, debug=True)