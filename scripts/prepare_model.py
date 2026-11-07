"""Baixa uma versão fixa do modelo oficial antes da aula."""

import hashlib
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_SHA256 = "fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1"


def prepare():
    destination = ROOT / "models" / "hand_landmarker.task"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and hashlib.sha256(destination.read_bytes()).hexdigest() == MODEL_SHA256:
        print("Modelo local verificado; nenhum download necessario.")
        return
    print("Baixando modelo oficial do Google...")
    with urllib.request.urlopen(MODEL_URL, timeout=45) as response:
        data = response.read(20_000_001)
    if len(data) > 20_000_000:
        raise RuntimeError("Modelo maior que o esperado.")
    digest = hashlib.sha256(data).hexdigest()
    if digest != MODEL_SHA256:
        raise RuntimeError("O modelo recebido nao corresponde ao SHA-256 esperado.")
    temporary = destination.with_suffix(".download")
    temporary.write_bytes(data)
    temporary.replace(destination)
    print(f"Modelo salvo: {len(data):,} bytes; SHA-256: {digest}")


if __name__ == "__main__":
    try:
        prepare()
    except (OSError, urllib.error.URLError, RuntimeError) as error:
        raise SystemExit(f"Falha ao preparar modelo: {error}. Verifique a conexao antes da aula.")

