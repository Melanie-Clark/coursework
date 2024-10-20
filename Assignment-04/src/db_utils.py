import mysql.connector
from config import HOST, USER, PASSWORD, DATABASE


# Raised if a connection exception occurs in the script below
class DbConnectionError(Exception):
    pass


# Database connection
def _connect_to_db():
    connection = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        auth_plugin="mysql_native_password",
        database=DATABASE
    )
    return connection


# Converts pizza database query results into a dictionary
def _pizza_dictionary(result):
    pizzas = []
    for pizza in result:
        pizzas.append({
            "id": pizza[0],
            "pizza_name": pizza[1],
            "toppings": [pizza[2], pizza[3], pizza[4], pizza[5]],
            "price": float(pizza[6]),
            "availability": "Available" if pizza[7] == 1 else "Unavailable",
        })
    return pizzas


# Converts topping database query results into a dictionary
def _toppings_dictionary(result):
    toppings = []
    for topping in result:
        toppings.append({
            "id": topping[0],
            "topping": topping[1],
        })
    return toppings


# Gets the complete list of pizzas along with their toppings from the database
def get_all_pizzas():
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        query = ("""
        SELECT pizza_id, pizza_name, t1.topping AS topping1, t2.topping AS topping2, t3.topping AS topping3, t4.topping AS topping4, price, p.available 
        FROM pizzas p
        LEFT JOIN toppings t1 
        ON t1.topping_id = p.topping1
        LEFT JOIN toppings t2
        ON t2.topping_id = p.topping2
        LEFT JOIN toppings t3
        ON t3.topping_id = p.topping3
        LEFT JOIN toppings t4
        ON t4.topping_id = p.topping4;""")

        cur.execute(query)
        result = cur.fetchall()

        pizzas = _pizza_dictionary(result)
        print(pizzas)

        cur.close()

        return pizzas

    except Exception:
        raise DbConnectionError("Failed to read data from DB: %s" % DATABASE)

    finally:
        if db_connection:
            db_connection.close()
            print("%s connection is closed" % DATABASE)


# Gets the complete list of pizzas along with their toppings from the database
def get_all_toppings():
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        query = """SELECT * FROM toppings ORDER BY topping_id;"""

        cur.execute(query)
        result = cur.fetchall()
        toppings = _toppings_dictionary(result)
        print(toppings)

        cur.close()

        return toppings

    except Exception:
        raise DbConnectionError("Failed to read data from DB: %s" % DATABASE)

    finally:
        if db_connection:
            db_connection.close()
            print("%s connection is closed" % DATABASE)


# Adds a new topping to the database. If topping already exists an error is returned.
def add_new_topping(new_topping_dict):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        # Query to check if topping already exists
        cur.execute(f"""SELECT * FROM toppings WHERE topping = '%s';""" % new_topping_dict["topping"])
        result = cur.fetchall()

        if result:
            result_message = {"error": "Topping already exists"}
            print("Topping already in database")
            return result_message
        else:
            query = f"""INSERT INTO toppings (topping) VALUES ('%s');""" % new_topping_dict['topping']
            cur.execute(query)
            db_connection.commit()  # Commit permanent action
            cur.close()

            print("%s topping successfully added" % new_topping_dict["topping"])
            return get_all_toppings()


    except Exception:
        raise DbConnectionError("Failed to read data from DB: %s" % DATABASE)

    finally:
        if db_connection:
            db_connection.close()
            print("%s connection is closed" % DATABASE)


# Deletes a pizzas from the database if ID exists
def delete_pizza_by_id(pizza_id):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        # Query to check if pizza exists in database
        cur.execute("""SELECT * FROM pizzas WHERE pizza_id = %s;""" % pizza_id)
        result = cur.fetchall()

        if not result:
            result_message = {"error": "Pizza not found"}
            return result_message
        else:
            delete_query = """DELETE FROM pizzas WHERE pizza_id = %s;""" % pizza_id
            cur.execute(delete_query)
            db_connection.commit()  # Commit permanent action
            cur.close()

            pizzas = get_all_pizzas()
        return pizzas

    except Exception:
        raise DbConnectionError("Failed to read data from DB: %s" % DATABASE)

    finally:
        if db_connection:
            db_connection.close()
            print("%s connection is closed" % DATABASE)


# Deletes a pizzas from the database if ID exists
def update_pizza_price_by_id(new_price_dict):
    db_connection = None
    try:
        db_connection = _connect_to_db()
        cur = db_connection.cursor()
        print("Connected to DB: %s" % DATABASE)

        # Query to check if pizza exists in database
        cur.execute("""SELECT * FROM pizzas WHERE pizza_id = %s;""" % new_price_dict["pizza_id"])
        result = cur.fetchall()

        if not result:
            result_message = {"error": "Pizza not found"}
            return result_message
        else:
            update_query = """UPDATE pizzas SET price = %s WHERE pizza_id = %s;"""
            cur.execute(update_query, (new_price_dict["new_price"], new_price_dict["pizza_id"]))
            db_connection.commit()  # Commit permanent action
            cur.close()

            pizzas = get_all_pizzas()
        return pizzas

    except Exception:
        raise DbConnectionError("Failed to read data from DB: %s" % DATABASE)

    finally:
        if db_connection:
            db_connection.close()
            print("%s connection is closed" % DATABASE)


# sample calls to test db_utils
if __name__ == "__main__":
    pass
    # get_all_pizzas()
    # get_all_toppings()
    # add_new_topping({"topping": "Beef"})
    # delete_pizza_by_id(1)
    # update_pizza_price_by_id({"pizza_id": 1, "new_price": 9.99})
