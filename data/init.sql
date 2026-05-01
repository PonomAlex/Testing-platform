DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price > 0)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    total_amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'new',
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price > 0),
    UNIQUE (order_id, product_id)
);

INSERT INTO users (email, first_name, last_name) VALUES
    ('alice@example.com', 'Alice', 'Smith'),
    ('bob@example.com', 'Bob', 'Brown');

INSERT INTO products (sku, name, price) VALUES
    ('SKU-BACKPACK', 'Sauce Labs Backpack', 29.99),
    ('SKU-BIKE-LIGHT', 'Sauce Labs Bike Light', 9.99),
    ('SKU-TSHIRT', 'Sauce Labs Bolt T-Shirt', 15.99);

INSERT INTO orders (user_id, total_amount, status) VALUES
    (1, 39.98, 'paid');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 29.99),
    (1, 2, 1, 9.99);
