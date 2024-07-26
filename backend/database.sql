CREATE DATABASE IF NOT EXISTS susans_sushi_shop;
USE susans_sushi_shop;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    order_date DATETIME NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    discount_applied VARCHAR(255),
    final_price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    sushi_type VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

