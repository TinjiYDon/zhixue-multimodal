from app.services import agent


def test_ask_empty_context(client):
    resp = client.post("/api/v1/courses/c1/ask", json={"question": "这节课讲什么"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["course_id"] == "c1"
    assert "暂无索引" in body["answer"]


def test_ask_cjk_match(client):
    agent.set_course_context("c2", ["本节课介绍深度学习的反向传播算法"])
    resp = client.post("/api/v1/courses/c2/ask", json={"question": "反向传播"})
    assert resp.status_code == 200
    assert "反向传播" in resp.json()["answer"]
