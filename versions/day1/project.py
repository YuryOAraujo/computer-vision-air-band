"""Checkpoint: painel completo da primeira noite, pronto para recuperar a aula."""

TITLE = "Meu painel de sons"
MISSION = "Aponte, feche a pinca e solte para tocar novamente."


def build_pads(instrument="soundboard"):
    return [
        {"id": "kick", "label": "BUMBO", "sound": "kick.wav",
         "rect": (0.10, 0.20, 0.37, 0.29), "color": (55, 220, 190)},
        {"id": "snare", "label": "CAIXA", "sound": "snare.wav",
         "rect": (0.53, 0.20, 0.37, 0.29), "color": (255, 116, 142)},
        {"id": "hihat", "label": "CHIMBAL", "sound": "hihat.wav",
         "rect": (0.10, 0.56, 0.37, 0.29), "color": (255, 205, 97)},
        {"id": "clap", "label": "PALMA", "sound": "clap.wav",
         "rect": (0.53, 0.56, 0.37, 0.29), "color": (148, 144, 255)},
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

