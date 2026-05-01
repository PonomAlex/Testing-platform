import os

import pytest
import psycopg2
from dotenv import load_dotenv

from common.db_client import DatabaseClient

load_dotenv()


@pytest.fixture(scope="session")
def db_client():
    try:
        client = DatabaseClient(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "testdb"),
            user=os.getenv("DB_USER", "testuser"),
            password=os.getenv("DB_PASS", "testpass"),
            port=int(os.getenv("DB_PORT", "5432")),
        )
    except psycopg2.OperationalError as exc:
        pytest.skip(f"Database is not available: {exc}")
        return

    yield client
    client.close()


@pytest.fixture(autouse=True)
def transaction_guard(db_client):
    yield
    db_client.rollback()
