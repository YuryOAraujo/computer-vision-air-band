"""Referência da segunda noite. Comece estudando a versão day1.

F1: painel; F2: bateria; F3: teclado; F4: efeitos.
Para imagens opcionais, acrescente "image": "arquivo.png" a um pad.
"""

TITLE = "Air Band Lab"
MISSION = "Crie um instrumento. Experimente. Apresente sua ideia."


def build_pads(instrument="soundboard"):
    if instrument == "keyboard":
        notes = [("C4", "DO"), ("D4", "RE"), ("E4", "MI"), ("G4", "SOL"), ("A4", "LA")]
        return [
            {"id": note, "label": label, "sound": f"{note}.wav",
             "rect": (0.075 + index * 0.172, 0.25, 0.155, 0.62),
             "color": [(55, 220, 190), (97, 190, 255), (148, 144, 255),
                       (255, 116, 142), (255, 205, 97)][index]}
            for index, (note, label) in enumerate(notes)
        ]

    if instrument == "effects":
        sounds = [("laser", "LASER"), ("coin", "MOEDA"),
                  ("space", "ESPACO"), ("powerup", "POWER UP")]
    else:
        sounds = [("kick", "BUMBO"), ("snare", "CAIXA"),
                  ("hihat", "CHIMBAL"), ("clap", "PALMA")]

    colors = [(55, 220, 190), (255, 116, 142), (255, 205, 97), (148, 144, 255)]
    # A bateria tem uma só fileira: a mão pode subir acima de todos os pads.
    if instrument == "drums":
        rectangles = [(0.055 + index * 0.235, 0.43, 0.21, 0.43) for index in range(4)]
    else:
        rectangles = [(0.10, 0.20, 0.37, 0.29), (0.53, 0.20, 0.37, 0.29),
                      (0.10, 0.56, 0.37, 0.29), (0.53, 0.56, 0.37, 0.29)]

    return [
        {"id": sound, "label": label, "sound": f"{sound}.wav",
         "rect": rectangle, "color": color}
        for (sound, label), rectangle, color in zip(sounds, rectangles, colors)
    ]


def find_pad(pads, x, y):
    for pad in pads:
        left, top, width, height = pad["rect"]
        if left <= x < left + width and top <= y < top + height:
            return pad
    return None


def choose_sound(pad, pinch_started):
    if pad is not None and pinch_started:
        return pad["sound"]
    return None


def volume_from_height(y):
    """Mais alto na imagem = mais volume, limitado ao intervalo 0.2 a 1."""
    return max(0.2, min(1.0, 1.0 - y))

