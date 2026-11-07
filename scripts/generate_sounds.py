"""Cria amostras originais de demonstração; não sobrescreve os seus sons.

Somente biblioteca padrão. Use --force para recriar todos os arquivos.
"""

import argparse
from array import array
import math
from pathlib import Path
import random
import sys
import wave

ROOT = Path(__file__).resolve().parents[1]
RATE = 44100


def synthesize(kind, frequency=440.0):
    rng = random.Random(42)
    duration = {"kick": 0.4, "snare": 0.24, "hihat": 0.12, "clap": 0.23,
                "note": 0.7, "laser": 0.35, "coin": 0.32,
                "space": 0.7, "powerup": 0.55}[kind]
    samples = []
    phase = 0.0
    last_noise = 0.0
    for index in range(int(RATE * duration)):
        t = index / RATE
        noise = rng.uniform(-1, 1)
        if kind == "kick":
            phase += 2 * math.pi * (48 + 110 * math.exp(-t * 35)) / RATE
            value = math.sin(phase) * math.exp(-t * 11)
        elif kind == "snare":
            value = (0.75 * noise + 0.25 * math.sin(2 * math.pi * 180 * t)) * math.exp(-t * 20)
        elif kind == "hihat":
            value = (noise - last_noise) * 0.45 * math.exp(-t * 42)
        elif kind == "clap":
            envelope = sum(math.exp(-(t - start) * 55) for start in (0, 0.018, 0.036) if t >= start)
            value = noise * envelope * 0.55
        elif kind == "note":
            value = (math.sin(2 * math.pi * frequency * t)
                     + 0.25 * math.sin(4 * math.pi * frequency * t)
                     + 0.12 * math.sin(6 * math.pi * frequency * t)) * math.exp(-t * 4)
        elif kind == "laser":
            phase += 2 * math.pi * (140 + 1700 * math.exp(-t * 10)) / RATE
            value = math.sin(phase) * math.exp(-t * 8)
        elif kind == "coin":
            hz = 988 if t < 0.09 else 1318.5
            phase += 2 * math.pi * hz / RATE
            value = math.sin(phase) * math.exp(-t * 9)
        elif kind == "space":
            phase += 2 * math.pi * (220 + 70 * math.sin(2 * math.pi * 5 * t)) / RATE
            value = (math.sin(phase) + 0.2 * noise) * math.sin(math.pi * t / duration) * 0.7
        else:
            hz = (261.63, 329.63, 392.0, 523.25)[min(3, int(t / duration * 4))]
            phase += 2 * math.pi * hz / RATE
            value = math.sin(phase) * math.exp(-t * 2)
        # Pequeno ataque e soltura evitam cliques na borda da amostra.
        value *= min(1.0, t / 0.003, (duration - t) / 0.015)
        samples.append(value)
        last_noise = noise
    peak = max(abs(value) for value in samples) or 1
    pcm = array("h")
    for value in samples:
        sample = int(value / peak * 24500)
        pcm.extend((sample, sample))
    if sys.byteorder != "little":
        pcm.byteswap()
    return pcm.tobytes()


def generate(output, force=False):
    output.mkdir(parents=True, exist_ok=True)
    definitions = {name: (name, 440) for name in
                   ("kick", "snare", "hihat", "clap", "laser", "coin", "space", "powerup")}
    definitions.update({name: ("note", hz) for name, hz in
                        (("C4", 261.63), ("D4", 293.66), ("E4", 329.63), ("G4", 392.0), ("A4", 440.0))})
    for name, (kind, hz) in definitions.items():
        path = output / f"{name}.wav"
        if path.exists() and not force:
            continue
        with wave.open(str(path), "wb") as sound:
            sound.setnchannels(2)
            sound.setsampwidth(2)
            sound.setframerate(RATE)
            sound.writeframes(synthesize(kind, hz))
        print(f"Criado: {path.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true")
    arguments = parser.parse_args()
    generate(ROOT / "assets" / "sounds", arguments.force)

