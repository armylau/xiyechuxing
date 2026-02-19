"""景点列表与详情 API 测试"""

from __future__ import annotations

from typing import Any

import app as app_module


class TestGetAttractions:
    """GET /api/attractions"""

    def test_missing_city_id_returns_400(self, client: Any) -> None:
        data = client.get("/api/attractions").get_json()
        assert data["code"] == 400

    def test_returns_bj_attractions(self, client: Any) -> None:
        data = client.get("/api/attractions?city_id=BJ").get_json()
        assert data["code"] == 0
        assert len(data["data"]) > 0
        assert data["city"] == "北京"

    def test_list_excludes_detail_fields(self, client: Any) -> None:
        """列表接口不应返回 detail, gallery, tips"""
        data = client.get("/api/attractions?city_id=BJ").get_json()
        for a in data["data"]:
            assert "detail" not in a
            assert "gallery" not in a
            assert "tips" not in a

    def test_list_has_summary_fields(self, client: Any) -> None:
        data = client.get("/api/attractions?city_id=BJ").get_json()
        for a in data["data"]:
            assert "id" in a
            assert "name" in a
            assert "image" in a
            assert "desc" in a
            assert "rating" in a
            assert "ticket_price" in a

    def test_all_cities_have_attractions(self, client: Any) -> None:
        for city in app_module.CITIES:
            data = client.get(f"/api/attractions?city_id={city['id']}").get_json()
            assert data["code"] == 0
            assert len(data["data"]) >= 1, f"{city['name']}应至少有1个景点"

    def test_unknown_city_returns_empty(self, client: Any) -> None:
        data = client.get("/api/attractions?city_id=ZZ").get_json()
        assert data["code"] == 0
        assert len(data["data"]) == 0


class TestGetAttractionDetail:
    """GET /api/attractions/<attraction_id>"""

    def test_valid_id_returns_full_data(self, client: Any) -> None:
        data = client.get("/api/attractions/bj_gugong").get_json()
        assert data["code"] == 0
        a = data["data"]
        assert a["name"] == "故宫博物院"
        assert "detail" in a
        assert "gallery" in a
        assert isinstance(a["gallery"], list)
        assert "tips" in a
        assert isinstance(a["tips"], list)
        assert "city" in data

    def test_detail_has_all_fields(self, client: Any) -> None:
        data = client.get("/api/attractions/bj_gugong").get_json()
        a = data["data"]
        required = {"id", "name", "image", "gallery", "desc", "detail",
                     "rating", "ticket_price", "open_time", "address", "tips"}
        assert required.issubset(a.keys())

    def test_invalid_id_returns_404(self, client: Any) -> None:
        data = client.get("/api/attractions/nonexistent").get_json()
        assert data["code"] == 404

    def test_gallery_has_images(self, client: Any) -> None:
        data = client.get("/api/attractions/bj_gugong").get_json()
        gallery = data["data"]["gallery"]
        assert len(gallery) >= 2
        for url in gallery:
            assert url.startswith("http")
