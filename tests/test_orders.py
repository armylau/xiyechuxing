"""订单创建、查询与持久化测试"""

from __future__ import annotations

import json
from typing import Any

import app as app_module


def _create_order(
    client: Any,
    train_id: str,
    seat_class: str = "second",
    meal: str = "none",
    quantity: int = 1,
    name: str = "张三",
    phone: str = "13800000001",
) -> dict[str, Any]:
    """辅助方法：创建订单并返回响应 JSON"""
    resp = client.post("/api/orders", json={
        "train_id": train_id,
        "passenger_name": name,
        "phone": phone,
        "quantity": quantity,
        "seat_class": seat_class,
        "meal": meal,
    })
    return resp.get_json()


class TestCreateOrder:
    """POST /api/orders"""

    def test_missing_params_returns_400(self, client: Any) -> None:
        data = client.post("/api/orders", json={}).get_json()
        assert data["code"] == 400

    def test_missing_name_returns_400(self, client: Any, sample_train_id: str) -> None:
        data = client.post("/api/orders", json={
            "train_id": sample_train_id, "phone": "13800000001",
        }).get_json()
        assert data["code"] == 400

    def test_nonexistent_train_returns_404(self, client: Any) -> None:
        data = _create_order(client, "FAKE_TRAIN_ID")
        assert data["code"] == 404

    def test_create_order_success(self, client: Any, sample_train_id: str) -> None:
        data = _create_order(client, sample_train_id)
        assert data["code"] == 0
        assert data["msg"] == "购票成功"
        order = data["data"]
        assert "order_id" in order
        assert order["status"] == "已出票"

    def test_order_has_seat_class(self, client: Any, sample_train_id: str) -> None:
        data = _create_order(client, sample_train_id, seat_class="first")
        order = data["data"]
        assert order["seat_class"]["id"] == "first"
        assert order["seat_class"]["name"] == "一等座"

    def test_order_has_meal(self, client: Any, sample_train_id: str) -> None:
        data = _create_order(client, sample_train_id, meal="meal_a")
        order = data["data"]
        assert order["meal"]["id"] == "meal_a"
        assert order["meal"]["price"] == 45

    def test_order_price_calculation_second(self, client: Any, sample_train_id: str) -> None:
        """二等座 ×1.0，无餐食"""
        data = _create_order(client, sample_train_id, seat_class="second", meal="none", quantity=2)
        order = data["data"]
        train_price = order["train"]["duration"]  # just to check calculation
        expected_ticket = round(
            next(t["price"] for t in app_module.TRAINS if t["id"] == sample_train_id) * 1.0, 1
        )
        assert order["ticket_price"] == expected_ticket
        assert order["meal_total"] == 0
        assert order["total_price"] == round(expected_ticket * 2, 1)

    def test_order_price_calculation_business_with_meal(
        self, client: Any, sample_train_id: str,
    ) -> None:
        """商务座 ×2.8 + 餐食"""
        base_price = next(
            t["price"] for t in app_module.TRAINS if t["id"] == sample_train_id
        )
        data = _create_order(
            client, sample_train_id,
            seat_class="business", meal="meal_b", quantity=3,
        )
        order = data["data"]
        expected_ticket = round(base_price * 2.8, 1)
        assert order["ticket_price"] == expected_ticket
        assert order["meal_total"] == 40 * 3  # meal_b = ¥40
        assert order["total_price"] == round(expected_ticket * 3 + 120, 1)

    def test_default_seat_and_meal(self, client: Any, sample_train_id: str) -> None:
        """不传 seat_class / meal 时使用默认值"""
        resp = client.post("/api/orders", json={
            "train_id": sample_train_id,
            "passenger_name": "王五",
            "phone": "13900000001",
        }).get_json()
        assert resp["code"] == 0
        assert resp["data"]["seat_class"]["id"] == "second"
        assert resp["data"]["meal"]["id"] == "none"

    def test_seats_decrease_after_order(self, client: Any, sample_train_id: str) -> None:
        train = next(t for t in app_module.TRAINS if t["id"] == sample_train_id)
        before = train["seats_remaining"]
        _create_order(client, sample_train_id, quantity=3)
        assert train["seats_remaining"] == before - 3

    def test_insufficient_seats(self, client: Any, sample_train_id: str) -> None:
        data = _create_order(client, sample_train_id, quantity=9999)
        assert data["code"] == 409


class TestQueryOrders:
    """GET /api/orders"""

    def test_empty_orders(self, client: Any) -> None:
        data = client.get("/api/orders").get_json()
        assert data["code"] == 0
        assert data["total"] == 0

    def test_query_all_orders(self, client: Any, sample_train_id: str) -> None:
        _create_order(client, sample_train_id, phone="13800000001")
        _create_order(client, sample_train_id, phone="13800000002")
        data = client.get("/api/orders").get_json()
        assert data["total"] == 2

    def test_query_by_phone(self, client: Any, sample_train_id: str) -> None:
        _create_order(client, sample_train_id, phone="13811111111")
        _create_order(client, sample_train_id, phone="13822222222")
        data = client.get("/api/orders?phone=13811111111").get_json()
        assert data["total"] == 1
        assert data["data"][0]["phone"] == "13811111111"

    def test_query_nonexistent_phone(self, client: Any) -> None:
        data = client.get("/api/orders?phone=19999999999").get_json()
        assert data["code"] == 0
        assert data["total"] == 0


class TestOrderPersistence:
    """订单持久化测试"""

    def test_order_saved_to_file(self, client: Any, sample_train_id: str) -> None:
        _create_order(client, sample_train_id)
        assert app_module.ORDERS_FILE.exists()
        saved = json.loads(app_module.ORDERS_FILE.read_text(encoding="utf-8"))
        assert len(saved) == 1
        assert saved[0]["passenger_name"] == "张三"

    def test_multiple_orders_accumulated(self, client: Any, sample_train_id: str) -> None:
        _create_order(client, sample_train_id, name="甲", phone="13800000001")
        _create_order(client, sample_train_id, name="乙", phone="13800000002")
        saved = json.loads(app_module.ORDERS_FILE.read_text(encoding="utf-8"))
        assert len(saved) == 2

    def test_load_orders_from_file(self, client: Any, sample_train_id: str) -> None:
        """模拟写入文件后用 _load_orders 读取"""
        _create_order(client, sample_train_id)
        loaded = app_module._load_orders()
        assert len(loaded) == 1
        assert loaded[0]["status"] == "已出票"

    def test_order_train_snapshot(self, client: Any, sample_train_id: str) -> None:
        """订单中保存的车次信息应为快照"""
        data = _create_order(client, sample_train_id)
        train_snap = data["data"]["train"]
        required = {"id", "train_no", "from_city", "to_city", "train_type",
                     "depart_time", "arrive_time", "duration", "date"}
        assert required.issubset(train_snap.keys())
