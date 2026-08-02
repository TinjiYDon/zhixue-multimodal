from app.services import course_service, job_service


def test_create_and_get_job(client):
    job_service.clear_jobs_for_tests()
    course_service.clear_courses_for_tests()

    course = client.post("/api/v1/courses", json={"title": "job-demo"}).json()
    resp = client.post(
        "/api/v1/jobs",
        json={"course_id": course["id"], "media_key": "uploads/demo.mp4"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["job_id"].startswith("job_")
    assert body["status"] in {"pending", "running", "failed", "done"}
    assert body["media_key"] == "uploads/demo.mp4"

    got = client.get(f"/api/v1/jobs/{body['job_id']}")
    assert got.status_code == 200
    assert got.json()["job_id"] == body["job_id"]


def test_get_job_not_found(client):
    job_service.clear_jobs_for_tests()
    resp = client.get("/api/v1/jobs/missing")
    assert resp.status_code == 404


def test_course_crud(client):
    course_service.clear_courses_for_tests()
    created = client.post("/api/v1/courses", json={"title": "crud"}).json()
    cid = created["id"]

    got = client.get(f"/api/v1/courses/{cid}")
    assert got.status_code == 200
    assert got.json()["title"] == "crud"

    patched = client.patch(f"/api/v1/courses/{cid}", json={"title": "crud2"})
    assert patched.status_code == 200
    assert patched.json()["title"] == "crud2"

    deleted = client.delete(f"/api/v1/courses/{cid}")
    assert deleted.status_code == 200
    assert client.get(f"/api/v1/courses/{cid}").status_code == 404
