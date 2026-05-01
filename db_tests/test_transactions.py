import pytest
import requests


@pytest.mark.db
@pytest.mark.regression
def test_create_order_transaction(db_client):
    user = db_client.execute("SELECT id FROM users ORDER BY id LIMIT 1")[0]
    product = db_client.execute("SELECT id, price FROM products ORDER BY id LIMIT 1")[0]

    inserted_order = db_client.execute(
        """
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (user["id"], product["price"], "new"),
    )
    order_id = inserted_order[0]["id"]

    db_client.execute(
        """
        INSERT INTO order_items (order_id, product_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s)
        """,
        (order_id, product["id"], 1, product["price"]),
    )

    check = db_client.execute(
        """
        SELECT o.id, oi.quantity, oi.unit_price
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.id
        WHERE o.id = %s
        """,
        (order_id,),
    )
    assert len(check) == 1


@pytest.mark.db
def test_transaction_rollback_works(db_client):
    initial_count = db_client.execute("SELECT COUNT(*) AS qty FROM orders")[0]["qty"]

    db_client.execute(
        """
        INSERT INTO orders (user_id, total_amount, status)
        VALUES (1, 10.00, 'new')
        """
    )
    mid_count = db_client.execute("SELECT COUNT(*) AS qty FROM orders")[0]["qty"]
    assert mid_count == initial_count + 1

    db_client.rollback()
    final_count = db_client.execute("SELECT COUNT(*) AS qty FROM orders")[0]["qty"]
    assert final_count == initial_count


@pytest.mark.db
def test_api_and_db_consistency_smoke(db_client):
    api_response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=10)
    assert api_response.status_code == 200
    assert len(api_response.json()) > 0
    db_products = db_client.execute("SELECT COUNT(*) AS qty FROM products")[0]["qty"]
    assert db_products > 0
