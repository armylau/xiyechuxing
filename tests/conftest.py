"""共享 pytest fixtures"""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Generator

import pytest

import app as app_module


@pytest.fixture()
def client() -> Generator[Any, None, None]:
    """创建测试客户端，每个测试使用独立的临时数据文件（订单+积分）"""
    original_orders = list(app_module.ORDERS)
    original_orders_file = app_module.ORDERS_FILE
    original_points_file = app_module.POINTS_FILE
    original_data_dir = app_module.DATA_DIR

    tmp_dir = Path(__file__).parent / "_tmp_test_data"
    tmp_dir.mkdir(exist_ok=True)

    app_module.ORDERS.clear()
    app_module.ORDERS_FILE = tmp_dir / "orders.json"  # type: ignore[assignment]
    app_module.POINTS_FILE = tmp_dir / "points.json"  # type: ignore[assignment]
    app_module.DATA_DIR = tmp_dir  # type: ignore[assignment]

    # 重置座位数，避免测试间影响
    for t in app_module.TRAINS:
        if "seats_remaining" in t and t["seats_remaining"] < 5:
            t["seats_remaining"] = 100

    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as c:
        yield c

    # 恢复
    app_module.ORDERS.clear()
    app_module.ORDERS.extend(original_orders)
    app_module.ORDERS_FILE = original_orders_file  # type: ignore[assignment]
    app_module.POINTS_FILE = original_points_file  # type: ignore[assignment]
    app_module.DATA_DIR = original_data_dir  # type: ignore[assignment]
    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)


@pytest.fixture()
def sample_train_id() -> str:
    """返回一个确定存在的车次 ID（北京→上海，2026-02-17）"""
    for t in app_module.TRAINS:
        if (
            t["from_city_id"] == "BJ"
            and t["to_city_id"] == "SH"
            and t["date"] == "2026-02-17"
        ):
            return t["id"]
    raise RuntimeError("找不到测试用车次")
