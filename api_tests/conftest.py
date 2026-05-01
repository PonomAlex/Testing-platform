import os
from typing import Dict

import pytest
from dotenv import load_dotenv

from common.api_client import APIClient

load_dotenv()


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    return APIClient(base_url=os.getenv("API_BASE_URL"))


@pytest.fixture(scope="session")
def post_schema() -> Dict:
    return {
        "type": "object",
        "required": ["userId", "id", "title", "body"],
        "properties": {
            "userId": {"type": "number"},
            "id": {"type": "number"},
            "title": {"type": "string"},
            "body": {"type": "string"},
        },
    }


@pytest.fixture(scope="session")
def comment_schema() -> Dict:
    return {
        "type": "object",
        "required": ["postId", "id", "name", "email", "body"],
        "properties": {
            "postId": {"type": "number"},
            "id": {"type": "number"},
            "name": {"type": "string"},
            "email": {"type": "string"},
            "body": {"type": "string"},
        },
    }
