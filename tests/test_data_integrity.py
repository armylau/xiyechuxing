"""数据完整性检查 — 确保模拟数据结构正确"""

from __future__ import annotations

import app as app_module


class TestCitiesData:
    """城市基础数据"""

    def test_at_least_10_cities(self) -> None:
        assert len(app_module.CITIES) >= 10

    def test_city_ids_all_uppercase(self) -> None:
        for c in app_module.CITIES:
            assert c["id"] == c["id"].upper()

    def test_coordinates_valid(self) -> None:
        for c in app_module.CITIES:
            assert -90 <= c["lat"] <= 90
            assert -180 <= c["lng"] <= 180


class TestTrainsData:
    """车次数据"""

    def test_trains_generated(self) -> None:
        assert len(app_module.TRAINS) > 100

    def test_train_ids_unique(self) -> None:
        ids = [t["id"] for t in app_module.TRAINS]
        assert len(ids) == len(set(ids))

    def test_train_types_valid(self) -> None:
        valid_types = {"高铁", "动车"}
        for t in app_module.TRAINS:
            assert t["train_type"] in valid_types

    def test_train_prices_positive(self) -> None:
        for t in app_module.TRAINS:
            assert t["price"] > 0
            assert t["duration"] > 0
            assert t["seats_remaining"] >= 0


class TestAttractionsData:
    """景点数据"""

    def test_all_cities_covered(self) -> None:
        for c in app_module.CITIES:
            assert c["id"] in app_module.ATTRACTIONS, f"城市{c['name']}缺少景点数据"

    def test_attraction_ids_unique(self) -> None:
        all_ids: list[str] = []
        for attractions in app_module.ATTRACTIONS.values():
            for a in attractions:
                all_ids.append(a["id"])
        assert len(all_ids) == len(set(all_ids))

    def test_attraction_required_fields(self) -> None:
        required = {"id", "name", "image", "gallery", "desc", "detail",
                     "rating", "ticket_price", "open_time", "address", "tips"}
        for city_id, attractions in app_module.ATTRACTIONS.items():
            for a in attractions:
                missing = required - a.keys()
                assert not missing, f"景点 {a.get('name', '?')} 缺少字段: {missing}"

    def test_image_urls_valid(self) -> None:
        for attractions in app_module.ATTRACTIONS.values():
            for a in attractions:
                assert a["image"].startswith("http")
                for url in a["gallery"]:
                    assert url.startswith("http")


class TestSeatClassesData:
    """舱位数据"""

    def test_three_classes(self) -> None:
        assert len(app_module.SEAT_CLASSES) == 3

    def test_multipliers_positive(self) -> None:
        for s in app_module.SEAT_CLASSES:
            assert s["multiplier"] > 0


class TestMealOptionsData:
    """餐食数据"""

    def test_has_none_option(self) -> None:
        ids = {m["id"] for m in app_module.MEAL_OPTIONS}
        assert "none" in ids

    def test_prices_non_negative(self) -> None:
        for m in app_module.MEAL_OPTIONS:
            assert m["price"] >= 0


class TestFoodsData:
    """美食数据"""

    def test_all_cities_covered(self) -> None:
        for c in app_module.CITIES:
            assert c["id"] in app_module.FOODS, f"城市{c['name']}缺少美食数据"
            assert len(app_module.FOODS[c["id"]]) >= 1


class TestHotelsData:
    """酒店数据"""

    def test_all_cities_covered(self) -> None:
        for c in app_module.CITIES:
            assert c["id"] in app_module.HOTELS, f"城市{c['name']}缺少酒店数据"
            assert len(app_module.HOTELS[c["id"]]) >= 1

    def test_hotel_stars_valid(self) -> None:
        for city_hotels in app_module.HOTELS.values():
            for h in city_hotels:
                assert 1 <= h["stars"] <= 5
