"""Referência da segunda noite. Comece estudando a versão day1.

F1: painel; F2: bateria; F3: teclado; F4: efeitos.
Para imagens opcionais, acrescente "imagem": "arquivo.png" a uma área.
"""

TITULO = "Air Band Lab"
MISSAO = "Crie um instrumento. Experimente. Apresente sua ideia."


def criar_areas(instrumento="painel"):
    if instrumento == "teclado":
        notas = [("C4", "DÓ"), ("D4", "RÉ"), ("E4", "MI"), ("G4", "SOL"), ("A4", "LÁ")]
        return [
            {"id": nota, "rotulo": rotulo, "som": f"{nota}.wav",
             "retangulo": (0.075 + indice * 0.172, 0.25, 0.155, 0.62),
             "cor": [(55, 220, 190), (97, 190, 255), (148, 144, 255),
                     (255, 116, 142), (255, 205, 97)][indice]}
            for indice, (nota, rotulo) in enumerate(notas)
        ]

    if instrumento == "efeitos":
        sons = [("laser", "LASER", "laser.wav"), ("moeda", "MOEDA", "coin.wav"),
                ("espaco", "ESPAÇO", "space.wav"), ("energia", "ENERGIA", "powerup.wav")]
    else:
        sons = [("bumbo", "BUMBO", "kick.wav"), ("caixa", "CAIXA", "snare.wav"),
                ("chimbal", "CHIMBAL", "hihat.wav"), ("palma", "PALMA", "clap.wav")]

    cores = [(55, 220, 190), (255, 116, 142), (255, 205, 97), (148, 144, 255)]
    # A bateria tem uma só fileira: a mão pode subir acima de todas as áreas.
    if instrumento == "bateria":
        retangulos = [(0.055 + indice * 0.235, 0.43, 0.21, 0.43) for indice in range(4)]
    else:
        retangulos = [(0.10, 0.20, 0.37, 0.29), (0.53, 0.20, 0.37, 0.29),
                      (0.10, 0.56, 0.37, 0.29), (0.53, 0.56, 0.37, 0.29)]

    return [
        {"id": identificador, "rotulo": rotulo, "som": arquivo,
         "retangulo": retangulo, "cor": cor}
        for (identificador, rotulo, arquivo), retangulo, cor in zip(sons, retangulos, cores)
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


def volume_pela_altura(y):
    """Mais alto na imagem = mais volume, limitado ao intervalo 0.2 a 1."""
    return max(0.2, min(1.0, 1.0 - y))

