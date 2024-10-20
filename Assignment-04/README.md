# Assignment Four

## Purpose
The **pizzas database** is used for storing pizzas, toppings, price and availability. 

The **terminal** will ask the user to choose from one of the following options:
- A: View all pizzas
- B: View all toppings
- C: Add a new topping
- D: Delete a pizza permanently from the menu
- E: Update the price of a pizza

The **API** will also return dictionaries contained within a list using the following endpoints:

**GET**: http://127.0.0.1:5000/pizzas

**GET**: http://127.0.0.1:5000/toppings

**POST**: http://127.0.0.1:5000/toppings/add

_In the event a topping already exists, the user will be presented with the following message:\
{"error": "Topping already exists"}_

**DELETE**: http://127.0.0.1:5000/pizzas/delete/{pizza_id}

Replace {pizza_id} with a number mapping to the pizza_id

_In the event the user is trying to delete a pizza that doesn't exist in the database, the following error will be returned:\
{"error": "Pizza not found"}_

**UPDATE**: http://127.0.0.1:5000/pizzas/update-price

_In the event the user is trying to update a pizza that doesn't exist in the database, the following error will be returned:\
{"error": "Pizza not found"}_

## Set-up and running order

The files should be actioned in the following order:

### 1. config.py
Add your user and password into the relevant fields in order for the API to connect to the database.

### 2. requirements.txt
Refer to this document for any additional installations required.
 
### 3. pizzas_db.sql
Run the `pizza_db.sql` script _(i.e. in SQLWorkbench or similar programme)_ to create the database
 
### 4. pizzas_app.py
Run this file to start Flask
 
### 5. main.py
Run this file to start the front end program and enter any required user inputs