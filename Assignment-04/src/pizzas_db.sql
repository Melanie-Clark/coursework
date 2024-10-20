	DROP DATABASE if exists pizzas_db;

CREATE DATABASE pizzas_db;
USE pizzas_db;

-- Table creation for pizzas and their toppings
CREATE TABLE toppings (
	topping_id INT AUTO_INCREMENT,
    topping VARCHAR(255) UNIQUE,
    PRIMARY KEY(topping_id)
	);
    
CREATE TABLE pizzas (
	pizza_id INT AUTO_INCREMENT,
    pizza_name VARCHAR(50) NOT NULL UNIQUE,
	topping1 INT,
	topping2 INT,
	topping3 INT,
	topping4 INT,
	price DECIMAL(6,2) NOT NULL,
	available BOOLEAN NOT NULL,
    PRIMARY KEY(pizza_id),
	FOREIGN KEY (topping1) REFERENCES toppings(topping_id),
    FOREIGN KEY (topping2) REFERENCES toppings(topping_id),
    FOREIGN KEY (topping3) REFERENCES toppings(topping_id),
    FOREIGN KEY (topping4) REFERENCES toppings(topping_id),
    -- Constraint added to ensure toppings must be filled in numerical order
    -- This would be a good example to use for testing to ensure all constraints are met
	CONSTRAINT CHK_pizzas CHECK (
    -- We don't want the scenario where T2 IS NOT NULL and T1 IS NULL, so reverse what it's looking for and change to OR to add constraint
    -- This way the constraint will fail, as neither condition will be met
		(topping2 IS NULL OR topping1 IS NOT NULL) AND -- repeated for other topping scenarios
		(topping3 IS NULL OR topping2 IS NOT NULL) AND
   		(topping4 IS NULL OR topping3 IS NOT NULL)        
	)
    );

-- Insert statements to add data to tables
INSERT INTO toppings (topping)
VALUES
    ("Chicken"),
	("Ham"),
    ("Mushrooms"), 
    ("Onions"),
    ("Peppers"),
    ("Pepperoni"),
    ("Sausage"), 
    ("Sweetcorn"),
    ("Tomatoes"), 
    ("Pumpkin"), 
    ("Eerie Egg"), 
    ("Spooky Sausage"), 
    ("Ghoulish Gherkins");
    
INSERT INTO pizzas (pizza_name, topping1, topping2, topping3, topping4, price, available)
VALUES 
("Margherita", NULL, NULL, NULL, NULL, 12.99, true),
("Pepperoni", 6, NULL, NULL, NULL, 15.99, true),
("Meat Feast", 6, 7, 2, 4, 15.99, true),
("Chicken Feast", 1, 3, 8, NULL, 15.99, true),
("Vegetarian", 3, 4, 5, 9, 12.99, true),
("Halloween Special", 10, 11, 12, 13, 17.99, false);

-- Queries to evidence results
SELECT * FROM pizzas;

SELECT * FROM toppings
ORDER BY topping_id;

SELECT pizza_id, pizza_name, t1.topping AS topping1, t2.topping AS topping2, t3.topping AS topping3, t4.topping AS topping4, price, p.available 
FROM pizzas p
LEFT JOIN toppings t1
ON t1.topping_id = p.topping1
LEFT JOIN toppings t2
ON t2.topping_id = p.topping2
LEFT JOIN toppings t3
ON t3.topping_id = p.topping3
LEFT JOIN toppings t4
ON t4.topping_id = p.topping4;
        
-- UPDATE pizzas
-- SET price = 20.00
-- WHERE pizza_id = 2;