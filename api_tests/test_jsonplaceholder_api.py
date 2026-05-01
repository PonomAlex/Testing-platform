import jsonschema
import pytest

from common.data_generators import random_post_payload


@pytest.mark.api
@pytest.mark.smoke
def test_get_posts(api_client, post_schema):
    response = api_client.get("/posts")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) > 0
    jsonschema.validate(payload[0], post_schema)


@pytest.mark.api
def test_get_post_by_id(api_client, post_schema):
    response = api_client.get("/posts/1")
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    jsonschema.validate(payload, post_schema)


@pytest.mark.api
def test_create_post(api_client):
    new_post = random_post_payload()
    response = api_client.post("/posts", new_post)
    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == new_post["title"]
    assert payload["body"] == new_post["body"]


@pytest.mark.api
def test_update_post(api_client):
    updated_post = random_post_payload()
    updated_post["id"] = 1
    response = api_client.put("/posts/1", updated_post)
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 1
    assert payload["title"] == updated_post["title"]


@pytest.mark.api
def test_delete_post(api_client):
    response = api_client.delete("/posts/1")
    assert response.status_code == 200
    assert response.text == "{}"


@pytest.mark.api
@pytest.mark.parametrize(
    "params,expected_user_id",
    [
        ({"userId": 1}, 1),
        ({"userId": 3}, 3),
    ],
)
def test_filter_posts_by_query_params(api_client, params, expected_user_id):
    response = api_client.get("/posts", params=params)
    assert response.status_code == 200
    payload = response.json()
    assert payload, "Expected filtered result to be non-empty"
    assert all(post["userId"] == expected_user_id for post in payload)


@pytest.mark.api
def test_get_post_comments(api_client, comment_schema):
    response = api_client.get("/posts/1/comments")
    assert response.status_code == 200
    payload = response.json()
    assert len(payload) > 0
    jsonschema.validate(payload[0], comment_schema)


@pytest.mark.api
@pytest.mark.parametrize(
    "endpoint,expected_code",
    [
        ("/posts/0", 404),
        ("/posts/-100", 404),
        ("/invalid-endpoint", 404),
    ],
)
def test_negative_404_cases(api_client, endpoint, expected_code):
    response = api_client.get(endpoint)
    assert response.status_code == expected_code


@pytest.mark.api
def test_negative_invalid_payload_returns_400_or_201(api_client):
    """
    JSONPlaceholder is a fake API and may still return 201 for invalid payloads.
    """
    response = api_client.post("/posts", data={"title": 123, "body": None, "userId": "abc"})
    assert response.status_code in (201, 400)
