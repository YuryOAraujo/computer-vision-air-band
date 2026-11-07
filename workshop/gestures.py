"""Regras puras: nenhum acesso à câmera, à janela ou ao áudio.

Leia este módulo depois de concluir as tarefas de versions/day1/project.py.
"""

import math


class PinchGate:
    """Uma pinça gera um evento; outra exige soltura e nova aproximação.

    A primeira observação e cada perda de rastreamento exigem mão aberta.
    Dois limiares evitam oscilação quando os dedos estão quase fechados.
    """

    def __init__(self, close_threshold=0.35, open_threshold=0.60, cooldown=0.12):
        self.close_threshold = close_threshold
        self.open_threshold = open_threshold
        self.cooldown = cooldown
        self.last_trigger = -math.inf
        self.reset()

    def reset(self):
        self.armed = False
        self.closed = False
        self.present = False

    def update(self, ratio, now):
        if ratio is None or not math.isfinite(ratio):
            self.reset()
            return False

        self.present = True
        if ratio >= self.open_threshold:
            self.armed = True
            self.closed = False
        elif ratio <= self.close_threshold:
            self.closed = True
            if self.armed:
                # Consumir a pinça, mesmo que o intervalo mínimo ainda não passou.
                self.armed = False
                if now - self.last_trigger >= self.cooldown:
                    self.last_trigger = now
                    return True
        return False

    @property
    def status(self):
        if not self.present:
            return "SEM MAO"
        if self.armed:
            return "PRONTO PARA TOCAR"
        return "ABRA OS DEDOS"


class StrikeGate:
    """Extensão: cruzar a borda de um pad descendo dispara uma batida.

    Velocidade em alturas de tela/segundo. Rearme acima da borda com margem.
    A detecção não dispara ao aparecer dentro de um pad ou em uma perda de mão.
    """

    def __init__(self, min_speed=0.45, cooldown=0.12, margin=0.045):
        self.min_speed = min_speed
        self.cooldown = cooldown
        self.margin = margin
        self.reset()

    def reset(self):
        self.previous = None
        self.armed = set()
        self.last_trigger = {}

    def update(self, cursor, pads, now):
        if cursor is None:
            self.reset()
            return None

        x, y = cursor
        previous = self.previous
        self.previous = (x, y, now)
        if previous is None:
            for pad in pads:
                if y < pad["rect"][1] - self.margin:
                    self.armed.add(pad["id"])
            return None

        old_x, old_y, old_time = previous
        elapsed = now - old_time
        if elapsed <= 0 or elapsed > 0.25:
            # Um salto de tempo não conta como movimento contínuo.
            self.armed.clear()
            return None

        for pad in pads:
            left, top, width, height = pad["rect"]
            pad_id = pad["id"]
            if y < top - self.margin:
                self.armed.add(pad_id)

            if old_y < top <= y:
                # Interpolar o ponto em que a trajetória cruzou a borda.
                fraction = (top - old_y) / (y - old_y)
                crossing_x = old_x + fraction * (x - old_x)
                if left <= crossing_x < left + width:
                    was_armed = pad_id in self.armed
                    self.armed.discard(pad_id)
                    speed = (y - old_y) / elapsed
                    last = self.last_trigger.get(pad_id, -math.inf)
                    if was_armed and speed >= self.min_speed and now - last >= self.cooldown:
                        self.last_trigger[pad_id] = now
                        return pad
        return None

