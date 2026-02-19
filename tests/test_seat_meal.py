"""舱位等级与餐食选项 API 测试"""

from __future__ import annotations

from typing import Any


class TestSeatClasses:
    """GET /api/seat_classes"""

    def test_returns_success(self, client: Any) -> None:
        data = client.get("/api/seat_classes").get_json()
        assert data["code"] == 0

    def test_has_three_classes(self, client: Any) -> None:
        data = client.get("/api/seat_classes").get_json()
        assert len(data["data"]) == 3

    def test_seat_class_fields(self, client: Any) -> None:
        data = client.get("/api/seat_classes").get_json()
        for seat in data["data"]:
            assert "id" in seat
            assert "name" in seat
            assert "multiplier" in seat
            assert "desc" in seat
            assert "icon" in seat

    def test_known_classes_exist(self, client: Any) -> None:
        data = client.get("/api/seat_classes").get_json()
        ids = {s["id"] for s in data["data"]}
        assert "business" in ids
        assert "first" in ids
        assert "second" in ids

    def test_multiplier_order(self, client: Any) -> None:
        """商务座 > 一等座 > 二等座"""
        data = client.get("/api/seat_classes").get_json()
        seat_map = {s["id"]: s["multiplier"] for s in data["data"]}
        assert seat_map["business"] > seat_map["first"] > seat_map["second"]

    def test_second_class_multiplier_is_one(self, client: Any) -> None:
        data = client.get("/api/seat_classes").get_json()
        second = next(s for s in data["data"] if s["id"] == "second")
        assert second["multiplier"] == 1.0


class TestMealOptions:
    """GET /api/meals"""

    def test_returns_success(self, client: Any) -> None:
        data = client.get("/api/meals").get_json()
        assert data["code"] == 0

    def test_has_multiple_options(self, client: Any) -> None:
        data = client.get("/api/meals").get_json()
        assert len(data["data"]) >= 2

    def test_meal_fields(self, client: Any) -> None:
        data = client.get("/api/meals").get_json()
        for meal in data["data"]:
            assert "id" in meal
            assert "name" in meal
            assert "price" in meal
            assert "icon" in meal

    def test_none_meal_is_free(self, client: Any) -> None:
        data = client.get("/api/meals").get_json()
        none_meal = next(m for m in data["data"] if m["id"] == "none")
        assert none_meal["price"] == 0

    def test_paid_meals_have_positive_price(self, client: Any) -> None:
        data = client.get("/api/meals").get_json()
        for meal in data["data"]:
            if meal["id"] != "none":
                assert meal["price"] > 0

    def test_meal_ids_unique(self, client: Any) -> None:
        data = client.get("/api/meals").get_json()
        ids = [m["id"] for m in data["data"]]
        assert len(ids) == len(set(ids))
