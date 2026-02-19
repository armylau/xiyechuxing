"""前端首页可访问性测试"""

from __future__ import annotations

from typing import Any


class TestIndexPage:
    """GET /"""

    def test_index_returns_200(self, client: Any) -> None:
        resp = client.get("/")
        assert resp.status_code == 200

    def test_index_contains_html(self, client: Any) -> None:
        resp = client.get("/")
        text = resp.data.decode("utf-8")
        assert "<!DOCTYPE html>" in text or "<html" in text

    def test_index_has_app_title(self, client: Any) -> None:
        resp = client.get("/")
        text = resp.data.decode("utf-8")
        assert "西野出行" in text
