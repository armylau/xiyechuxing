"""出行安全提醒 API 测试"""

from __future__ import annotations

from typing import Any

import app as app_module


class TestSafetyTips:
    """GET /api/safety_tips"""

    def test_returns_success(self, client: Any) -> None:
        data = client.get("/api/safety_tips").get_json()
        assert data["code"] == 0

    def test_returns_list(self, client: Any) -> None:
        data = client.get("/api/safety_tips").get_json()
        assert isinstance(data["data"], list)
        assert len(data["data"]) > 0

    def test_tip_has_required_fields(self, client: Any) -> None:
        data = client.get("/api/safety_tips").get_json()
        for tip in data["data"]:
            assert "icon" in tip
            assert "title" in tip
            assert "content" in tip

    def test_tip_count_matches_data(self, client: Any) -> None:
        data = client.get("/api/safety_tips").get_json()
        assert len(data["data"]) == len(app_module.SAFETY_TIPS)

    def test_tip_content_not_empty(self, client: Any) -> None:
        data = client.get("/api/safety_tips").get_json()
        for tip in data["data"]:
            assert len(tip["title"]) > 0
            assert len(tip["content"]) > 0

    def test_known_tips_exist(self, client: Any) -> None:
        data = client.get("/api/safety_tips").get_json()
        titles = [t["title"] for t in data["data"]]
        assert "实名制乘车" in titles
        assert "行李安检须知" in titles
        assert "提前到站" in titles


class TestSafetyTipsData:
    """直接检查 SAFETY_TIPS 数据完整性"""

    def test_at_least_5_tips(self) -> None:
        assert len(app_module.SAFETY_TIPS) >= 5

    def test_all_have_icon(self) -> None:
        for tip in app_module.SAFETY_TIPS:
            assert "icon" in tip
            assert len(tip["icon"]) > 0

    def test_all_have_title_and_content(self) -> None:
        for tip in app_module.SAFETY_TIPS:
            assert len(tip["title"]) >= 2
            assert len(tip["content"]) >= 10

    def test_titles_unique(self) -> None:
        titles = [t["title"] for t in app_module.SAFETY_TIPS]
        assert len(titles) == len(set(titles))
