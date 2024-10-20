from flask import Flask, jsonify, request
from db_utils import get_all_pizzas, get_all_toppings, add_new_topping, delete_pizza_by_id, update_pizza_price_by_id

app = Flask(__name__)


# Retrieves all pizzas
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    return jsonify(get_all_pizzas())


# Retrieves all toppings
@app.route("/toppings", methods=["GET"])
def get_toppings():
    return jsonify(get_all_toppings())


# Adds a new topping
@app.route("/toppings/add", methods=["POST"])
def add_topping():
    new_topping_dict = request.get_json()
    return jsonify(add_new_topping(new_topping_dict))


# Deletes a pizza by id
@app.route("/pizzas/delete/<int:pizza_id>", methods=["DELETE"])
def delete_pizza_id(pizza_id):
    return jsonify(delete_pizza_by_id(pizza_id))


# Updates price by pizza id
@app.route("/pizzas/update-price", methods=["PUT"])
def update_pizza_price():
    new_price_dict = request.get_json()
    return jsonify(update_pizza_price_by_id(new_price_dict))


if __name__ == "__main__":
    app.run(debug=True)
