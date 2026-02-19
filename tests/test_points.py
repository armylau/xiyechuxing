"""积分系统 API 测试"""

from __future__ import annotations

from typing import Any

import app as app_module


def _create_order(
    client: Any, train_id: str, phone: str = "13900000001",
    seat_class: str = "second", meal: str = "none", quantity: int = 1,
) -> dict[str, Any]:
    return client.post("/api/orders", json={
        "train_id": train_id, "passenger_name": "测试用户",
        "phone": phone, "quantity": quantity,
        "seat_class": seat_class, "meal": meal,
    }).get_json()


class TestOrderPointsEarning:
    """下单获取积分"""

    def test_order_returns_points_earned(self, client: Any, sample_train_id: str) -> None:
        data = _create_order(client, sample_train_id)
        assert data["code"] == 0
        assert "points_earned" in data
        assert data["points_earned"] > 0

    def test_order_returns_level(self, client: Any, sample_train_id: str) -> None:
        data = _create_order(client, sample_train_id)
        assert "level" in data
        assert "points_total" in data

    def test_points_earned_equals_total_price(self, client: Any, sample_train_id: str) -> None:
        """积分 = int(总金额) * 1"""
        data = _create_order(client, sample_train_id)
        order = data["data"]
        assert data["points_earned"] == int(order["total_price"]) * app_module.POINTS_PER_YUAN

    def test_order_data_includes_points(self, client: Any, sample_train_id: str) -> None:
        """订单数据中包含 points_earned 字段"""
        data = _create_order(client, sample_train_id)
        assert "points_earned" in data["data"]
        assert data["data"]["points_earned"] > 0

    def test_points_accumulate(self, client: Any, sample_train_id: str) -> None:
        phone = "13900000099"
        d1 = _create_order(client, sample_train_id, phone=phone)
        d2 = _create_order(client, sample_train_id, phone=phone)
        assert d2["points_total"] == d1["points_earned"] + d2["points_earned"]


class TestQueryPoints:
    """GET /api/points"""

    def test_missing_phone_returns_400(self, client: Any) -> None:
        data = client.get("/api/points").get_json()
        assert data["code"] == 400

    def test_new_user_returns_zero(self, client: Any) -> None:
        data = client.get("/api/points?phone=19900000000").get_json()
        assert data["code"] == 0
        assert data["data"]["points"] == 0
        assert data["data"]["level"] == "普通会员"

    def test_returns_points_after_order(self, client: Any, sample_train_id: str) -> None:
        phone = "13900000002"
        order_data = _create_order(client, sample_train_id, phone=phone)
        earned = order_data["points_earned"]

        data = client.get(f"/api/points?phone={phone}").get_json()
        assert data["code"] == 0
        assert data["data"]["points"] == earned
        assert data["data"]["total_earned"] == earned

    def test_has_history(self, client: Any, sample_train_id: str) -> None:
        phone = "13900000003"
        _create_order(client, sample_train_id, phone=phone)
        data = client.get(f"/api/points?phone={phone}").get_json()
        assert len(data["data"]["history"]) == 1
        assert data["data"]["history"][0]["earned"] > 0

    def test_points_has_level_fields(self, client: Any, sample_train_id: str) -> None:
        phone = "13900000004"
        _create_order(client, sample_train_id, phone=phone)
        data = client.get(f"/api/points?phone={phone}").get_json()
        p = data["data"]
        assert "level" in p
        assert "level_icon" in p
        assert "discount" in p


class TestPointsLevels:
    """GET /api/points/levels"""

    def test_returns_levels(self, client: Any) -> None:
        data = client.get("/api/points/levels").get_json()
        assert data["code"] == 0
        assert len(data["data"]) == len(app_module.LEVEL_THRESHOLDS)

    def test_level_fields(self, client: Any) -> None:
        data = client.get("/api/points/levels").get_json()
        for lv in data["data"]:
            assert "threshold" in lv
            assert "level" in lv
            assert "icon" in lv
            assert "discount" in lv
            assert "discount_label" in lv

    def test_first_level_is_free(self, client: Any) -> None:
        data = client.get("/api/points/levels").get_json()
        first = data["data"][0]
        assert first["threshold"] == 0
        assert first["discount"] == 0.0


class TestCalcLevel:
    """_calc_level 等级计算"""

    def test_zero_points(self) -> None:
        name, icon, discount = app_module._calc_level(0)
        assert name == "普通会员"
        assert discount == 0.0

    def test_silver_level(self) -> None:
        name, _, discount = app_module._calc_level(500)
        assert name == "白银会员"
        assert discount == 0.02

    def test_gold_level(self) -> None:
        name, _, discount = app_module._calc_level(2000)
        assert name == "黄金会员"

    def test_diamond_level(self) -> None:
        name, _, discount = app_module._calc_level(10000)
        assert name == "钻石会员"
        assert discount == 0.10
