"""EDITE AQUI: primeiro um pad; depois, um painel com quatro sons.

Execute: python app.py --version starter --input mouse
O rastreamento, o áudio e o desenho já estão preparados pelo professor.
"""

TITLE = "Meu primeiro som"
MISSION = "Complete as funcoes para tocar por gesto. Tecla 1: testar audio."


def build_pads(instrument="soundboard"):
    # Coordenadas de 0 a 1: esquerda, topo, largura, altura.
    # Cor em RGB (vermelho, verde, azul). Tecla física para testar: 1.
    return [
        {"id": "kick", "label": "BUMBO", "sound": "kick.wav",
         "rect": (0.28, 0.28, 0.44, 0.48), "color": (55, 220, 190)},
    ]


def find_pad(pads, x, y):
    """Devolva o pad que contém o cursor, ou None se estiver fora."""
    # TODO 1: percorra os pads com `for pad in pads:`.
    # TODO 2: leia `left, top, width, height = pad["rect"]`.
    # TODO 3: verifique os limites de x e y e devolva `pad`.
    return None


def choose_sound(pad, pinch_started):
    """Devolva o nome do áudio somente no INÍCIO da pinça."""
    # TODO 4: se existir pad e pinch_started for True, devolva pad["sound"].
    return None

