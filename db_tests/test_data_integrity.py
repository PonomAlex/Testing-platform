import json
from pathlib import Path

import pytest


@pytest.mark.db
def test_required_tables_exist(db_client):
    rows = db_client.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        """
    )
    table_names = {row["table_name"] for row in rows}
    assert {"users", "products", "orders", "order_items"}.issubset(table_names)


@pytest.mark.db
def test_foreign_keys_exist(db_client):
    rows = db_client.execute(
        """
        SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name
        FROM information_schema.table_constraints AS tc
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        """
    )
    relations = {(r["table_name"], r["column_name"], r["foreign_table_name"]) for r in rows}
    assert ("orders", "user_id", "users") in relations
    assert ("order_items", "order_id", "orders") in relations
    assert ("order_items", "product_id", "products") in relations


@pytest.mark.db
def test_email_is_unique(db_client):
    rows = db_client.execute(
        """
        SELECT email, COUNT(*) AS qty
        FROM users
        GROUP BY email
        HAVING COUNT(*) > 1
        """
    )
    assert rows == []


@pytest.mark.db
def test_price_consistency_order_items_vs_products(db_client):
    rows = db_client.execute(
        """
        SELECT oi.id
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        WHERE oi.unit_price <> p.price
        """
    )
    assert rows == []


@pytest.mark.db
def test_db_seed_matches_test_products_file(db_client):
    products_file = Path(__file__).resolve().parents[1] / "data" / "test_products.json"
    with products_file.open("r", encoding="utf-8") as file_obj:
        expected_products = json.load(file_obj)

    db_products = db_client.execute("SELECT sku, name, price FROM products ORDER BY sku")
    normalized = sorted(
        [{"sku": p["sku"], "name": p["name"], "price": float(p["price"])} for p in db_products],
        key=lambda item: item["sku"],
    )
    assert normalized == sorted(expected_products, key=lambda item: item["sku"])
