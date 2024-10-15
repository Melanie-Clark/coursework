import requests
import json


# Retrieves JSON data from API for all pizzas
def get_all_pizzas_front_end():
    endpoint = "http://127.0.0.1:5000/pizzas"
    data = requests.get(endpoint).json()
    return data


# Retrieves JSON data from API for all toppings
def get_all_toppings_front_end():
    endpoint = "http://127.0.0.1:5000/toppings"
    data = requests.get(endpoint).json()
    return data


# Adds a new topping to the API
def add_topping_front_end(new_topping_dict):
    endpoint = "http://127.0.0.1:5000/toppings/add"
    data = requests.post(
        endpoint,
        headers={'content-type': 'application/json'},
        data=json.dumps(new_topping_dict)
    )
    return data.json()


# Deletes a pizza from the API and returns server response
def delete_pizza_by_id_front_end(pizza_id_to_delete):
    endpoint = f"http://127.0.0.1:5000/pizzas/delete/{pizza_id_to_delete}"
    data = requests.delete(endpoint).json()
    return data


# Updates the price for a pizza on the API
def update_pizza_price_front_end(new_price_dict):
    endpoint = "http://127.0.0.1:5000/pizzas/update-price"
    data = requests.put(
        endpoint,
        headers={'content-type': 'application/json'},
        json=new_price_dict
    )
    return data.json()


# Welcome message presented to the user in the terminal
def welcome_message():
    print("\n🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕")
    print("🍕 Welcome to PizzaHouse! 🍕")
    print("🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕🍕")

    print(f"\nChoose one of the following options:")
    print("A: View all pizzas")
    print("B: View all toppings")
    print("C: Add a new topping")
    print("D: Delete a pizza permanently from the menu")
    print("E: Update pizza price")



# Asks user to choose one of 5 options and returns appropriate response
def user_options():
    answer = input("Enter A, B, C, D or E: ").strip().upper()

    if answer == "A": answer_a()
    elif answer == "B": answer_b()
    elif answer == "C": answer_c()
    elif answer == "D": answer_d()
    elif answer == "E": answer_e()
    else:
        print("Invalid option. Please enter A, B, C, D or E: ")


# User answer A: Shows user a list of all pizzas
def answer_a():
    if get_all_pizzas_front_end() is None:
        print("Failed to retrieve records.")
    else:
        print(f"\nHere's the range of pizzas:")
        list_of_pizzas()


# User answer B: Shows user a list of all toppings
def answer_b():
    if get_all_toppings_front_end() is None:
        print("Failed to retrieve records.")
    else:
        print(f"\nHere's a list of toppings:")
        list_of_toppings()


# User answer C: Adds new topping
def answer_c():
    new_topping = input(f"Enter new topping name: ").strip().title()
    new_topping_dict = {"topping": new_topping}

    new_topping_response = add_topping_front_end(new_topping_dict)
    if new_topping_response is not None:
        if "error" in new_topping_response:
            print(f"\n{new_topping_response}")
        else:
            print(f"\n{new_topping} topping added to the database")
            print("\nHere's the latest set of toppings:")
            list_of_toppings()
    else:
        print("Failed to retrieve records.")


# User answer D: Deletes a pizza
def answer_d():
    if get_all_pizzas_front_end() is not None:
        print(f"\nHere's a list of pizzas to choose from:")
        list_of_pizzas()

        while True:
            try:
                pizza_id_to_delete = int(input(f"\nWhich pizza would you like to delete (Enter number): ").strip())
                if pizza_id_to_delete > 0:
                    new_topping_response = delete_pizza_by_id_front_end(pizza_id_to_delete)
                    if "error" in new_topping_response:
                        print(new_topping_response)
                    else:
                        print(f"\nPizza id ({pizza_id_to_delete}) successfully deleted."
                              f"\n\nHere's the updated list of pizzas:")
                        list_of_pizzas()
                        break
            except ValueError:
                print("Invalid answer. Please enter a number: ")
    else:
        print("Failed to retrieve records.")


# User answer E: Update pizza price
def answer_e():
    pizzas = get_all_pizzas_front_end()
    if pizzas is not None:
        print(f"\nHere's a list of pizzas to choose from:")
        list_of_pizzas()

        while True:
            try:
                pizza_id_to_update = int(input(f"\nWhich pizza would you like to update (Enter number): ").strip())
                # any checks if any items in a list is True
                if any(pizza_id_to_update == pizza["id"] for pizza in pizzas):
                    break
                else:
                    print(f"Invalid answer. Please enter a valid pizza id number from the list above: ")
            except ValueError:
                print(f"Invalid answer. Please enter a valid pizza id number from the list above: ")

        while True:
            try:
                pizza_price_to_update = float(input(f"Enter new pizza_price (i.e. 12.99): ").strip())
                if pizza_price_to_update >= 0:
                    new_price_dict = {"pizza_id": pizza_id_to_update, "new_price": pizza_price_to_update}

                    if pizza_id_to_update > 0:
                        update_response = update_pizza_price_front_end(new_price_dict)
                        if "error" in update_response:
                            print(update_response)
                        else:
                            print(f"\nPizza id ({pizza_id_to_update}) successfully updated."
                                  f"\n\nHere's the updated list of pizzas:")
                            list_of_pizzas()
                            break
                else:
                    print("Invalid answer. Please enter a price i.e. 12.99: ")
            except ValueError:
                print("Invalid answer. Please enter a price i.e. 12.99: ")
    else:
        print("Failed to retrieve records.")


# Returns a list of pizzas or error message
def list_of_pizzas():
    if get_all_pizzas_front_end() is not None:
        for pizza in get_all_pizzas_front_end():
            print(
                f"{pizza['id']}: {pizza['pizza_name']} - Extra toppings ({', '.join(p if p else "NULL" for p in pizza['toppings'])}), "
                f"£{pizza['price']}, {pizza['availability']}")
    else:
        print("Failed to retrieve records.")


# Returns a list of toppings or error message
def list_of_toppings():
    if get_all_toppings_front_end() is not None:
        for topping in get_all_toppings_front_end():
            print(f"{topping['id']}: {topping['topping']}")
    else:
        print("Failed to retrieve records.")


# runs main program
def run():
    welcome_message()
    user_options()


if __name__ == "__main__":
    run()
