"""Mensagens curtas para erros comuns ao editar um layout."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate_pads(pads):
    if not pads or len(pads) > 9:
        raise ValueError("Crie entre 1 e 9 pads (teclas fisicas de 1 a 9).")
    seen = set()
    for pad in pads:
        for field in ("id", "label", "sound", "rect", "color"):
            if field not in pad:
                raise ValueError(f"Pad incompleto: falta {field!r}.")
        if pad["id"] in seen:
            raise ValueError(f"Cada pad precisa de um id diferente: {pad['id']}")
        seen.add(pad["id"])
        x, y, width, height = pad["rect"]
        if not (0 <= x < 1 and 0 <= y < 1 and width > 0 and height > 0
                and x + width <= 1.000001 and y + height <= 1.000001):
            raise ValueError(f"Confira rect do pad {pad['id']}: use limites de 0 a 1.")
        if len(pad["color"]) != 3 or any(not 0 <= value <= 255 for value in pad["color"]):
            raise ValueError(f"Confira color do pad {pad['id']}: tres valores RGB de 0 a 255.")

