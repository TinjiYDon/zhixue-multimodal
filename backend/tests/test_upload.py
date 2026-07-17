from unittest.mock import patch

from app.services import agent


def test_upload_presign_ok(client):
    with patch("app.services.storage.presign_put_object", return_value="http://minio/fake"):
        resp = client.post(
            "/api/v1/upload/presign",
            json={"course_id": "c1", "filename": "lecture.mp4", "content_type": "video/mp4"},
        )
    assert resp.status_code == 200
    body = resp.json()
    assert body["media_key"].startswith("courses/c1/")
    assert body["upload_url"] == "http://minio/fake"
    assert body["content_type"] == "video/mp4"


def test_upload_complete_requires_object(client):
    with patch("app.services.storage.object_exists", return_value=False):
        resp = client.post(
            "/api/v1/upload/complete",
            json={"course_id": "c1", "media_key": "courses/c1/abc.mp4"},
        )
    assert resp.status_code == 400
    assert "尚未上传" in resp.json()["detail"]


def test_upload_complete_ok(client):
    with patch("app.services.storage.object_exists", return_value=True):
        resp = client.post(
            "/api/v1/upload/complete",
            json={"course_id": "c1", "media_key": "courses/c1/abc.mp4"},
        )
    assert resp.status_code == 200
    assert resp.json()["media_key"] == "courses/c1/abc.mp4"


def test_upload_complete_bad_prefix(client):
    resp = client.post(
        "/api/v1/upload/complete",
        json={"course_id": "c1", "media_key": "courses/other/abc.mp4"},
    )
    assert resp.status_code == 400
