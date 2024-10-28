#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    # Clear existing data
    print("Deleting existing data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    # Add Restaurants
    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Shack St")
    bistro = Restaurant(name="Sanjay's Pizza", address="456 Bistro Blvd")
    palace = Restaurant(name="Kiki's Pizza Palace", address="789 Palace Pkwy")
    db.session.add_all([shack, bistro, palace])

    # Add Pizzas
    print("Creating pizzas...")
    cheese = Pizza(name="Cheese Delight", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Pepperoni Feast", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="California Special", ingredients="Dough, Ricotta, Red peppers, Mustard")
    db.session.add_all([cheese, pepperoni, california])

    # Add Restaurant-Pizza associations with prices
    print("Creating RestaurantPizza records...")
    db.session.add_all([
        RestaurantPizza(restaurant=shack, pizza=cheese, price=10),
        RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=12),
        RestaurantPizza(restaurant=palace, pizza=california, price=15)
    ])

    db.session.commit()
    print("Seeding done!")
