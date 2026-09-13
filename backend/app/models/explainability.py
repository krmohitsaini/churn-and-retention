from typing import Any


def format_drivers(score_row: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"driver": score_row.get("top_driver_1"), "weight": score_row.get("top_driver_1_weight")},
        {"driver": score_row.get("top_driver_2"), "weight": score_row.get("top_driver_2_weight")},
        {"driver": score_row.get("top_driver_3"), "weight": score_row.get("top_driver_3_weight")},
    ]

