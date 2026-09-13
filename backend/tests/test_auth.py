"""Auth + upload limit tests (Z0 ship gate)."""

from unittest.mock import patch


def test_login_dev_issues_token(client_anon):
    resp = client_anon.post("/api/v1/auth/login", json={"code": "dev-abc"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["access_token"]
    assert body["token_type"] == "bearer"
    assert body["user_id"].startswith("u_")


def test_ask_requires_auth(client_anon):
    resp = client_anon.post("/api/v1/courses/c1/ask", json={"question": "hi"})
    assert resp.status_code == 401


def test_me_and_delete(client):
    me = client.get("/api/v1/auth/me")
    assert me.status_code == 200
    assert me.json()["user_id"].startswith("u_")

    deleted = client.delete("/api/v1/auth/me")
    assert deleted.status_code == 200
    assert deleted.json()["status"] == "deleted"

    again = client.get("/api/v1/auth/me")
    assert again.status_code == 401


def test_upload_rejects_bad_content_type(client):
    resp = client.post(
        "/api/v1/upload/presign",
        json={
            "course_id": "c1",
            "filename": "x.exe",
            "content_type": "application/x-msdownload",
        },
    )
    assert resp.status_code == 400
    assert "content_type" in resp.json()["detail"]


def test_upload_rejects_too_large(client):
    resp = client.post(
        "/api/v1/upload/presign",
        json={
            "course_id": "c1",
            "filename": "big.mp4",
            "content_type": "video/mp4",
            "size_bytes": 10**12,
        },
    )
    assert resp.status_code == 400
    assert "过大" in resp.json()["detail"]


def test_upload_presign_ok_with_auth(client):
    with patch("app.services.storage.presign_put_object", return_value="http://minio/fake"):
        resp = client.post(
            "/api/v1/upload/presign",
            json={"course_id": "c1", "filename": "lecture.mp4", "content_type": "video/mp4"},
        )
    assert resp.status_code == 200
    assert resp.json()["max_bytes"] is not None
