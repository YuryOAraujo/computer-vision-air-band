"""Entrada do workshop. Execute `python app.py --help` para ver as opções."""

import argparse
from pathlib import Path


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Air Band Lab — instrumentos com gestos")
    available = [name for name in ("starter", "day1", "instructor")
                 if (Path(__file__).parent / "versions" / name / "project.py").is_file()]
    default_version = available[0]
    parser.add_argument("--version", choices=available, default=default_version,
                        help=f"versao a executar; padrao: {default_version}")
    parser.add_argument("--input", choices=("camera", "mouse"), default="camera", dest="input_mode")
    parser.add_argument("--instrument", choices=("soundboard", "drums", "keyboard", "effects"), default="soundboard")
    parser.add_argument("--camera", type=int, default=0, help="indice da webcam, normalmente 0 ou 1")
    parser.add_argument("--strike", action="store_true", help="bateria por batidas descendentes")
    parser.add_argument("--height-volume", action="store_true", help="volume do teclado pela altura da mao")
    parser.add_argument("--mute", action="store_true", help="executar sem dispositivo de audio")
    parser.add_argument("--frames", type=int, default=0, help="encerrar apos N quadros; 0 = sem limite")
    parser.add_argument("--screenshot", help="salvar o ultimo quadro em um arquivo PNG")
    args = parser.parse_args(argv)
    if args.version != "instructor" and (args.instrument != "soundboard" or args.strike or args.height_volume):
        parser.error("instrumentos e extensoes usam --version instructor")
    if args.strike and args.instrument != "drums":
        parser.error("--strike requer --instrument drums")
    if args.height_volume and args.instrument != "keyboard":
        parser.error("--height-volume requer --instrument keyboard")
    if args.frames < 0:
        parser.error("--frames deve ser maior ou igual a zero")
    return args


def main():
    args = parse_args()
    try:
        from workshop.runtime import run
        run(args)
    except ModuleNotFoundError as error:
        print(f"Dependencia ausente: {error.name}. Instale com: python -m pip install -r requirements-lock.txt")
        return 1
    except (RuntimeError, ValueError) as error:
        print(f"Nao foi possivel continuar: {error}")
        return 1
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

