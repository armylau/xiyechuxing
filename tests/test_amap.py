"""高德地图跳转链接测试"""

from __future__ import annotations

from typing import Any

import app as app_module


class TestAmapUrlGeneration:
    """_amap_url 和 _inject_amap_url 工具函数"""

    def test_amap_url_format(self) -> None:
        url = app_module._amap_url("故宫博物院", "景山前街4号", "北京")
        assert url.startswith("https://uri.amap.com/search?keyword=")
        assert "src=" in url

    def test_amap_url_contains_keyword(self) -> None:
        url = app_module._amap_url("故宫博物院", "景山前街4号", "北京")
        assert "keyword=" in url

    def test_amap_url_contains_city(self) -> None:
        url = app_module._amap_url("西湖", "龙井路1号", "杭州")
        assert "city=" in url

    def test_inject_amap_url_adds_field(self) -> None:
        item = {"name": "测试地点", "address": "测试地址1号"}
        result = app_module._inject_amap_url(item, "北京")
        assert "amap_url" in result
        assert result["amap_url"].startswith("https://uri.amap.com/")

    def test_inject_amap_url_preserves_fields(self) -> None:
        item = {"name": "A", "address": "B", "rating": "4.5"}
        result = app_module._inject_amap_url(item, "上海")
        assert result["name"] == "A"
        assert result["address"] == "B"
        assert result["rating"] == "4.5"

    def test_inject_amap_url_no_address_no_url(self) -> None:
        item = {"name": "仅名称无地址"}
        result = app_module._inject_amap_url(item, "北京")
        assert "amap_url" not in result

    def test_inject_does_not_mutate_original(self) -> None:
        item = {"name": "A", "address": "B"}
        result = app_module._inject_amap_url(item, "成都")
        assert "amap_url" not in item
        assert "amap_url" in result


class TestAttractionAmapUrl:
    """景点 API 返回 amap_url"""

    def test_attraction_list_has_amap_url(self, client: Any) -> None:
        data = client.get("/api/attractions?city_id=BJ").get_json()
        for a in data["data"]:
            assert "amap_url" in a
            assert a["amap_url"].startswith("https://uri.amap.com/")

    def test_attraction_detail_has_amap_url(self, client: Any) -> None:
        data = client.get("/api/attractions/bj_gugong").get_json()
        assert data["code"] == 0
        assert "amap_url" in data["data"]
        assert "amap.com" in data["data"]["amap_url"]

    def test_all_city_attractions_have_amap_url(self, client: Any) -> None:
        for city in app_module.CITIES:
            data = client.get(
                f"/api/attractions?city_id={city['id']}"
            ).get_json()
            for a in data["data"]:
                assert "amap_url" in a, f"Missing amap_url for {a['name']}"


class TestFoodAmapUrl:
    """美食 API 返回 amap_url"""

    def test_food_has_amap_url(self, client: Any) -> None:
        data = client.get("/api/foods?city_id=BJ").get_json()
        for f in data["data"]:
            assert "amap_url" in f
            assert f["amap_url"].startswith("https://uri.amap.com/")

    def test_all_city_foods_have_amap_url(self, client: Any) -> None:
        for city in app_module.CITIES:
            data = client.get(
                f"/api/foods?city_id={city['id']}"
            ).get_json()
            for f in data["data"]:
                assert "amap_url" in f, f"Missing amap_url for {f['name']}"


class TestHotelAmapUrl:
    """酒店 API 返回 amap_url"""

    def test_hotel_has_amap_url(self, client: Any) -> None:
        data = client.get("/api/hotels?city_id=BJ").get_json()
        for h in data["data"]:
            assert "amap_url" in h
            assert h["amap_url"].startswith("https://uri.amap.com/")

    def test_all_city_hotels_have_amap_url(self, client: Any) -> None:
        for city in app_module.CITIES:
            data = client.get(
                f"/api/hotels?city_id={city['id']}"
            ).get_json()
            for h in data["data"]:
                assert "amap_url" in h, f"Missing amap_url for {h['name']}"
