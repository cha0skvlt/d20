from __future__ import annotations

from unittest.mock import patch

from bot.utils import parse_dice_expression


def test_dice_expression() -> None:
    seq = [4, 2, 6]

    def fake_randint(a: int, b: int) -> int:
        return seq.pop(0)

    with patch("random.randint", fake_randint):
        result = parse_dice_expression("3d6 + 2")
    assert result["rolls"] == [4, 2, 6]
    assert result["modifier"] == 2
    assert result["total"] == sum([4, 2, 6]) + 2
