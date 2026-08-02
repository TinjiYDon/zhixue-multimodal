def test_timeline_placeholder(client):
    resp = client.get("/api/v1/courses/demo/timeline")
    assert resp.status_code == 200
    body = resp.json()
    assert body["course_id"] == "demo"
    assert body["status"] == "placeholder"
    assert len(body["cues"]) >= 1
    assert len(body["slides"]) >= 1
