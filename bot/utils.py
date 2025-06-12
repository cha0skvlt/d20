from __future__ import annotations

import random
import re
from typing import Dict, List

DICE_SIDES = {4, 6, 8, 10, 12, 20, 100}


def parse_dice_expression(expr: str) -> Dict[str, int | List[int]]:
    expr = expr.replace(" ", "")
    if not expr:
        raise ValueError("Empty expression")
    token_re = re.compile(r"([+-]?)(\d*d(?:4|6|8|10|12|20|100)|\d+)")
    pos = 0
    rolls: List[int] = []
    modifier = 0
    total = 0
    while pos < len(expr):
        m = token_re.match(expr, pos)
        if not m:
            raise ValueError(f"Invalid token at: {expr[pos:]}")
        sign = -1 if m.group(1) == "-" else 1
        token = m.group(2)
        if "d" in token:
            num_str, sides_str = token.split("d")
            num = int(num_str) if num_str else 1
            sides = int(sides_str)
            if sides not in DICE_SIDES or num < 1:
                raise ValueError("Invalid dice: " + token)
            group_rolls = [random.randint(1, sides) for _ in range(num)]
            rolls.extend(group_rolls)
            total += sign * sum(group_rolls)
        else:
            value = int(token)
            modifier += sign * value
            total += sign * value
        pos = m.end()
    return {"rolls": rolls, "modifier": modifier, "total": total}
