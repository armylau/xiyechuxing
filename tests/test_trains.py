"""车次搜索与智能推荐 API 测试"""

from __future__ import annotations

from typing import Any


class TestSearchTrains:
    """GET /api/trains/search"""

    def test_missing_params_returns_400(self, client: Any) -> None:
        data = client.get("/api/trains/search").get_json()
        assert data["code"] == 400

    def test_missing_date_returns_400(self, client: Any) -> None:
        data = client.get("/api/trains/search?from=BJ&to=SH").get_json()
        assert data["code"] == 400

    def test_valid_search_returns_results(self, client: Any) -> None:
        data = client.get(
            "/api/trains/search?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        assert data["code"] == 0
        assert data["total"] > 0

    def test_train_has_required_fields(self, client: Any) -> None:
        data = client.get(
            "/api/trains/search?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        required = {
            "id", "train_no", "from_city_id", "to_city_id",
            "from_city", "to_city", "train_type", "depart_time",
            "arrive_time", "duration", "price", "seats_remaining", "date",
        }
        for train in data["data"]:
            assert required.issubset(train.keys()), f"缺少字段: {required - train.keys()}"

    def test_results_sorted_by_depart_time(self, client: Any) -> None:
        data = client.get(
            "/api/trains/search?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        times = [t["depart_time"] for t in data["data"]]
        assert times == sorted(times)

    def test_no_results_for_invalid_route(self, client: Any) -> None:
        data = client.get(
            "/api/trains/search?from=BJ&to=BJ&date=2026-02-17"
        ).get_json()
        assert data["code"] == 0
        assert data["total"] == 0

    def test_no_results_for_missing_route(self, client: Any) -> None:
        data = client.get(
            "/api/trains/search?from=BJ&to=CQ&date=2026-02-17"
        ).get_json()
        assert data["code"] == 0
        assert data["total"] == 0

    def test_results_match_query_cities(self, client: Any) -> None:
        data = client.get(
            "/api/trains/search?from=SH&to=HZ&date=2026-02-17"
        ).get_json()
        for t in data["data"]:
            assert t["from_city_id"] == "SH"
            assert t["to_city_id"] == "HZ"
            assert t["date"] == "2026-02-17"


class TestRecommendTrains:
    """GET /api/trains/recommend"""

    def test_missing_params_returns_400(self, client: Any) -> None:
        data = client.get("/api/trains/recommend").get_json()
        assert data["code"] == 400

    def test_fastest_preference(self, client: Any) -> None:
        data = client.get(
            "/api/trains/recommend?from=BJ&to=SH&date=2026-02-17&preference=fastest"
        ).get_json()
        assert data["code"] == 0
        assert data["total"] <= 5
        if data["total"] > 1:
            durations = [t["duration"] for t in data["data"]]
            assert durations == sorted(durations)

    def test_cheapest_preference(self, client: Any) -> None:
        data = client.get(
            "/api/trains/recommend?from=BJ&to=SH&date=2026-02-17&preference=cheapest"
        ).get_json()
        assert data["code"] == 0
        if data["total"] > 1:
            prices = [t["price"] for t in data["data"]]
            assert prices == sorted(prices)

    def test_recommend_has_reasons(self, client: Any) -> None:
        data = client.get(
            "/api/trains/recommend?from=BJ&to=SH&date=2026-02-17&preference=fastest"
        ).get_json()
        for t in data["data"]:
            assert "recommend_reasons" in t
            assert isinstance(t["recommend_reasons"], list)

    def test_max_five_results(self, client: Any) -> None:
        data = client.get(
            "/api/trains/recommend?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        assert len(data["data"]) <= 5
