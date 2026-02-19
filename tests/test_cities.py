"""城市列表 API 测试"""

from __future__ import annotations

from typing import Any

import app as app_module


class TestGetCities:
    """GET /api/cities"""

    def test_returns_success(self, client: Any) -> None:
        resp = client.get("/api/cities")
        data = resp.get_json()
        assert resp.status_code == 200
        assert data["code"] == 0

    def test_returns_all_cities(self, client: Any) -> None:
        data = client.get("/api/cities").get_json()
        assert len(data["data"]) == len(app_module.CITIES)

    def test_city_has_required_fields(self, client: Any) -> None:
        data = client.get("/api/cities").get_json()
        for city in data["data"]:
            assert "id" in city
            assert "name" in city
            assert "lat" in city
            assert "lng" in city

    def test_city_ids_are_unique(self, client: Any) -> None:
        data = client.get("/api/cities").get_json()
        ids = [c["id"] for c in data["data"]]
        assert len(ids) == len(set(ids))

    def test_known_cities_exist(self, client: Any) -> None:
        data = client.get("/api/cities").get_json()
        names = {c["name"] for c in data["data"]}
        for expected in ["北京", "上海", "广州", "成都", "杭州", "西安", "重庆", "昆明", "南京", "武汉"]:
            assert expected in names, f"缺少城市: {expected}"
