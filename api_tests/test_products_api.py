import pytest


@pytest.mark.api
def test_get_all_posts_count_is_100(api_client):
    response = api_client.get("/posts")
    assert response.status_code == 200
    assert len(response.json()) == 100


@pytest.mark.api
@pytest.mark.parametrize("post_id", [1, 25, 50, 75, 100])
def test_post_ids_are_accessible(api_client, post_id):
    response = api_client.get(f"/posts/{post_id}")
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == post_id


@pytest.mark.api
def test_comments_filter_by_post_id(api_client):
    response = api_client.get("/comments", params={"postId": 1})
    assert response.status_code == 200
    comments = response.json()
    assert comments
    assert all(comment["postId"] == 1 for comment in comments)
