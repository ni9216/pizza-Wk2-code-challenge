from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)
    restaurant_pizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    # add relationship

    # add serialization rules
    serialize_only = ("address", "id", "name", "restaurant_pizzas")

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurants = db.relationship("RestaurantPizza", back_populates="pizza")

    # add serialization rules
    serialize_only = ("id", "ingredients", "name")

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    # add relationships
    restaurant = db.relationship("Restaurant", back_populates="restaurant_pizzas")
    pizza = db.relationship("Pizza", back_populates="restaurants")
    # add serialization rules
    serialize_only = ("id", "pizza", "pizza_id", "price", "restaurant_id")

    # add validation
    def validate_price(self, price):
        if price < 1 or price > 30:
            raise ValueError({"errors": ["validation errors"]})

    def __init__(self, price, pizza_id, restaurant_id):
        self.validate_price(int(price))
        self.price = price
        self.pizza_id = pizza_id
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"