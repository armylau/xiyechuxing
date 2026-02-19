"""折扣车票推荐 API 测试"""

from __future__ import annotations

from typing import Any


class TestDiscountTrains:
    """GET /api/trains/discount"""

    def test_missing_params_returns_400(self, client: Any) -> None:
        data = client.get("/api/trains/discount").get_json()
        assert data["code"] == 400

    def test_missing_date_returns_400(self, client: Any) -> None:
        data = client.get("/api/trains/discount?from=BJ&to=SH").get_json()
        assert data["code"] == 400

    def test_valid_request_returns_data(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        assert data["code"] == 0
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_discount_fields(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        if data["data"]:
            item = data["data"][0]
            assert "original_price" in item
            assert "discounted_price" in item
            assert "discount_rate" in item
            assert "discount_label" in item
            assert "discount_reasons" in item

    def test_discounted_price_less_than_original(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        for item in data["data"]:
            assert item["discounted_price"] < item["original_price"]

    def test_discount_rate_range(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        for item in data["data"]:
            assert 0 < item["discount_rate"] <= 0.20

    def test_discount_reasons_not_empty(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        for item in data["data"]:
            assert len(item["discount_reasons"]) > 0

    def test_max_10_results(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        assert len(data["data"]) <= 10

    def test_sorted_by_discount_rate(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        rates = [d["discount_rate"] for d in data["data"]]
        assert rates == sorted(rates, reverse=True)

    def test_no_discount_for_nonexistent_route(self, client: Any) -> None:
        data = client.get(
            "/api/trains/discount?from=BJ&to=KM&date=2026-02-17"
        ).get_json()
        assert data["code"] == 0
        assert data["data"] == []

    def test_discount_has_train_fields(self, client: Any) -> None:
        """折扣数据同时包含基本车次字段"""
        data = client.get(
            "/api/trains/discount?from=BJ&to=SH&date=2026-02-17"
        ).get_json()
        if data["data"]:
            item = data["data"][0]
            assert "train_no" in item
            assert "from_city" in item
            assert "to_city" in item
            assert "depart_time" in item
