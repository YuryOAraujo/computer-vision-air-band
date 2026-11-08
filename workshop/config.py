"""Mensagens curtas para erros comuns ao editar um layout."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validar_areas(areas):
    if not areas or len(areas) > 9:
        raise ValueError("Crie entre 1 e 9 áreas (teclas físicas de 1 a 9).")
    identificadores = set()
    for area in areas:
        for campo in ("id", "rotulo", "som", "retangulo", "cor"):
            if campo not in area:
                raise ValueError(f"Área incompleta: falta {campo!r}.")
        if area["id"] in identificadores:
            raise ValueError(f"Cada área precisa de um id diferente: {area['id']}")
        identificadores.add(area["id"])
        x, y, largura, altura = area["retangulo"]
        if not (0 <= x < 1 and 0 <= y < 1 and largura > 0 and altura > 0
                and x + largura <= 1.000001 and y + altura <= 1.000001):
            raise ValueError(f"Confira retangulo da área {area['id']}: use limites de 0 a 1.")
        if len(area["cor"]) != 3 or any(not 0 <= valor <= 255 for valor in area["cor"]):
            raise ValueError(f"Confira cor da área {area['id']}: três valores RGB de 0 a 255.")

