"""Ponto de recuperação: painel completo da primeira noite."""

TITULO = "Meu painel de sons"
MISSAO = "Aponte, feche a pinça e solte para tocar novamente."


def criar_areas(instrumento="painel"):
    return [
        {"id": "bumbo", "rotulo": "BUMBO", "som": "kick.wav",
         "retangulo": (0.10, 0.20, 0.37, 0.29), "cor": (55, 220, 190)},
        {"id": "caixa", "rotulo": "CAIXA", "som": "snare.wav",
         "retangulo": (0.53, 0.20, 0.37, 0.29), "cor": (255, 116, 142)},
        {"id": "chimbal", "rotulo": "CHIMBAL", "som": "hihat.wav",
         "retangulo": (0.10, 0.56, 0.37, 0.29), "cor": (255, 205, 97)},
        {"id": "palma", "rotulo": "PALMA", "som": "clap.wav",
         "retangulo": (0.53, 0.56, 0.37, 0.29), "cor": (148, 144, 255)},
    ]


def encontrar_area(areas, x, y):
    for area in areas:
        esquerda, topo, largura, altura = area["retangulo"]
        if esquerda <= x < esquerda + largura and topo <= y < topo + altura:
            return area
    return None


def escolher_som(area, pinca_iniciada):
    if area is not None and pinca_iniciada:
        return area["som"]
    return None

