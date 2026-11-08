"""EDITE AQUI: primeiro uma área sonora; depois, um painel com quatro sons.

Execute: python app.py --version starter --input mouse
O rastreamento, o áudio e o desenho já estão preparados pelo professor.
"""

TITULO = "Meu primeiro som"
MISSAO = "Complete as funções para tocar por gesto. Tecla 1: testar áudio."


def criar_areas(instrumento="painel"):
    # Coordenadas de 0 a 1: esquerda, topo, largura, altura.
    # Cor em RGB (vermelho, verde, azul). Tecla física para testar: 1.
    return [
        {"id": "bumbo", "rotulo": "BUMBO", "som": "kick.wav",
         "retangulo": (0.28, 0.28, 0.44, 0.48), "cor": (55, 220, 190)},
    ]


def encontrar_area(areas, x, y):
    """Devolva a área que contém o cursor, ou None se estiver fora."""
    # TAREFA 1: percorra as áreas com `for area in areas:`.
    # TAREFA 2: leia `esquerda, topo, largura, altura = area["retangulo"]`.
    # TAREFA 3: verifique os limites de x e y e devolva `area`.
    return None


def escolher_som(area, pinca_iniciada):
    """Devolva o nome do áudio somente no INÍCIO da pinça."""
    # TAREFA 4: se existir área e pinca_iniciada for True, devolva area["som"].
    return None

