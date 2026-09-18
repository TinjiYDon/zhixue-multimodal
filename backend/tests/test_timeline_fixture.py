from app.services import timeline_store


def test_fixture_timeline_ingest(client):
    timeline_store.clear_for_tests()
    course = client.post("/api/v1/courses", json={"title": "tl"}).json()
    cid = course["id"]
    resp = client.post(f"/api/v1/courses/{cid}/timeline/from-fixture")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert len(body["cues"]) >= 2

    got = client.get(f"/api/v1/courses/{cid}/timeline")
    assert got.status_code == 200
    assert got.json()["status"] == "ok"
    assert got.json()["cues"][0]["text"]

    ask = client.post(f"/api/v1/courses/{cid}/ask", json={"question": "核心概念"})
    assert ask.status_code == 200
    assert ask.json()["answer"]
