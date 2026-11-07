"""Gera três pacotes independentes; o starter não inclui respostas do professor."""

import argparse
import hashlib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from prepare_model import MODEL_SHA256

ROOT = Path(__file__).resolve().parents[1]


def selected_files(stage, include_wheels):
    direct = ["app.py", "requirements.txt", "requirements-lock.txt",
              "preparar_windows.bat", "iniciar_windows.bat"]
    paths = [ROOT / name for name in direct]
    directories = ["workshop", "assets", "models"]
    if stage == "instructor":
        paths += [ROOT / "README.md", ROOT / "WORKSHOP_PLAN.md"]
        directories += ["versions", "docs", "scripts", "tests"]
    else:
        paths += [ROOT / "versions" / "__init__.py",
                  ROOT / "docs" / "STUDENT_GUIDE.md", ROOT / "docs" / "LAB_SETUP.md",
                  ROOT / "scripts" / "prepare_model.py", ROOT / "scripts" / "generate_sounds.py"]
        directories += [f"versions/{stage}"]
    if include_wheels:
        if not (ROOT / "wheelhouse").is_dir() or not list((ROOT / "wheelhouse").glob("*.whl")):
            raise RuntimeError("wheelhouse ausente/vazio. Baixe as dependencias no Windows primeiro.")
        directories += ["wheelhouse"]
    for name in directories:
        paths.extend(path for path in (ROOT / name).rglob("*")
                     if path.is_file() and "__pycache__" not in path.parts
                     and path.suffix not in (".pyc", ".download"))
    return sorted(set(paths))


def package(include_wheels=False):
    model = ROOT / "models" / "hand_landmarker.task"
    if not model.is_file() or hashlib.sha256(model.read_bytes()).hexdigest() != MODEL_SHA256:
        raise RuntimeError("Prepare e verifique o modelo antes: python scripts/prepare_model.py")
    if len(list((ROOT / "assets" / "sounds").glob("*.wav"))) < 13:
        raise RuntimeError("Prepare os audios antes: python scripts/generate_sounds.py")
    destination = ROOT / "dist"
    destination.mkdir(exist_ok=True)
    for stage in ("starter", "day1", "instructor"):
        filename = destination / f"air-band-{stage}.zip"
        with ZipFile(filename, "w", ZIP_DEFLATED) as archive:
            prefix = f"air-band-{stage}"
            for path in selected_files(stage, include_wheels):
                archive.write(path, f"{prefix}/{path.relative_to(ROOT).as_posix()}")
            if stage != "instructor":
                archive.writestr(f"{prefix}/README.md", (ROOT / "versions" / stage / "README.md").read_bytes())
        print(f"Criado: {filename.name} ({filename.stat().st_size / 1_000_000:.1f} MB)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-wheels", action="store_true")
    arguments = parser.parse_args()
    try:
        package(arguments.include_wheels)
    except RuntimeError as error:
        raise SystemExit(str(error))

