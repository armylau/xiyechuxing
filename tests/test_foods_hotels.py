"""美食推荐与酒店推荐 API 测试"""

from __future__ import annotations

from typing import Any

import app as app_module


class TestGetFoods:
    """GET /api/foods"""

    def test_missing_city_id_returns_400(self, client: Any) -> None:
        data = client.get("/api/foods").get_json()
        assert data["code"] == 400

    def test_returns_bj_foods(self, client: Any) -> None:
        data = client.get("/api/foods?city_id=BJ").get_json()
        assert data["code"] == 0
        assert len(data["data"]) > 0
        assert data["city"] == "北京"

    def test_food_has_required_fields(self, client: Any) -> None:
        data = client.get("/api/foods?city_id=BJ").get_json()
        required = {"name", "type", "rating", "price_per_person", "icon", "address", "desc", "tags"}
        for f in data["data"]:
            assert required.issubset(f.keys()), f"美食缺少字段: {required - f.keys()}"

    def test_food_tags_is_list(self, client: Any) -> None:
        data = client.get("/api/foods?city_id=CD").get_json()
        for f in data["data"]:
            assert isinstance(f["tags"], list)
            assert len(f["tags"]) >= 1

    def test_all_cities_have_foods(self, client: Any) -> None:
        for city in app_module.CITIES:
            data = client.get(f"/api/foods?city_id={city['id']}").get_json()
            assert data["code"] == 0
            assert len(data["data"]) >= 1, f"{city['name']}应至少有1个美食推荐"

    def test_unknown_city_returns_empty(self, client: Any) -> None:
        data = client.get("/api/foods?city_id=ZZ").get_json()
        assert data["code"] == 0
        assert len(data["data"]) == 0


class TestGetHotels:
    """GET /api/hotels"""

    def test_missing_city_id_returns_400(self, client: Any) -> None:
        data = client.get("/api/hotels").get_json()
        assert data["code"] == 400

    def test_returns_bj_hotels(self, client: Any) -> None:
        data = client.get("/api/hotels?city_id=BJ").get_json()
        assert data["code"] == 0
        assert len(data["data"]) > 0
        assert data["city"] == "北京"

    def test_hotel_has_required_fields(self, client: Any) -> None:
        data = client.get("/api/hotels?city_id=BJ").get_json()
        required = {"name", "stars", "rating", "price", "icon", "address", "distance", "tags", "desc"}
        for h in data["data"]:
            assert required.issubset(h.keys()), f"酒店缺少字段: {required - h.keys()}"

    def test_hotel_stars_in_range(self, client: Any) -> None:
        data = client.get("/api/hotels?city_id=BJ").get_json()
        for h in data["data"]:
            assert 1 <= h["stars"] <= 5

    def test_hotel_tags_is_list(self, client: Any) -> None:
        data = client.get("/api/hotels?city_id=SH").get_json()
        for h in data["data"]:
            assert isinstance(h["tags"], list)
            assert len(h["tags"]) >= 1

    def test_all_cities_have_hotels(self, client: Any) -> None:
        for city in app_module.CITIES:
            data = client.get(f"/api/hotels?city_id={city['id']}").get_json()
            assert data["code"] == 0
            assert len(data["data"]) >= 1, f"{city['name']}应至少有1个酒店推荐"

    def test_unknown_city_returns_empty(self, client: Any) -> None:
        data = client.get("/api/hotels?city_id=ZZ").get_json()
        assert data["code"] == 0
        assert len(data["data"]) == 0
