"""Integração da janela, câmera, gestos e código editado pela turma."""

import importlib
import os
import time

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
import pygame

from workshop.audio import AudioBank, SilentAudio
from workshop.config import ROOT, validar_areas
from workshop.drawing import View
from workshop.gestures import PinchGate, StrikeGate
from workshop.tracking import CameraTracker, Observation


# A linha de comando mantém seus nomes; o código das atividades usa português.
INSTRUMENTOS = {"soundboard": "painel", "drums": "bateria",
                "keyboard": "teclado", "effects": "efeitos"}


def run(args):
    projeto = importlib.import_module(f"versions.{args.version}.project")
    pygame.display.init()
    pygame.font.init()
    camera = None
    try:
        if not args.mute:
            try:
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            except pygame.error as error:
                raise RuntimeError("Audio indisponivel. Verifique a saida de som ou use --mute.") from error
        view = View(ROOT / "assets" / "images")
        instrument = args.instrument
        areas = projeto.criar_areas(INSTRUMENTOS[instrument])
        validar_areas(areas)
        # A referência permite mudar de instrumento sem recarregar arquivos a cada toque.
        todas_as_areas = (sum((projeto.criar_areas(nome) for nome in INSTRUMENTOS.values()), [])
                          if args.version == "instructor" else areas)
        audio = (SilentAudio() if args.mute else
                 AudioBank(ROOT / "assets" / "sounds", [area["som"] for area in todas_as_areas]))
        if args.input_mode == "camera":
            camera = CameraTracker(ROOT / "models" / "hand_landmarker.task", args.camera)

        pinch = PinchGate()
        strike_gate = StrikeGate()
        strike = args.strike
        height_volume = args.height_volume
        show_hand = True
        flashes = {}
        hit_count = 0
        clock = pygame.time.Clock()
        running = True
        frame_count = 0

        while running:
            now = time.monotonic()
            keyboard_hits = []
            requested_instrument = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif pygame.K_1 <= event.key <= pygame.K_9:
                        index = event.key - pygame.K_1
                        if index < len(areas):
                            keyboard_hits.append(areas[index])
                    elif event.key == pygame.K_r:
                        pinch.reset()
                        strike_gate.reset()
                    elif event.key == pygame.K_h:
                        show_hand = not show_hand
                    elif event.key == pygame.K_m:
                        audio.muted = not audio.muted if not args.mute else True
                        audio.stop()
                    elif args.version == "instructor":
                        modes = {pygame.K_F1: "soundboard", pygame.K_F2: "drums",
                                 pygame.K_F3: "keyboard", pygame.K_F4: "effects"}
                        requested_instrument = modes.get(event.key, requested_instrument)
                        if event.key == pygame.K_b and instrument == "drums":
                            strike = not strike
                            pinch.reset()
                            strike_gate.reset()
                        elif event.key == pygame.K_v and instrument == "keyboard":
                            height_volume = not height_volume
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and args.version == "instructor":
                    requested_instrument = view.tab_at(event.pos) or requested_instrument

            if not running:
                break
            if requested_instrument and requested_instrument != instrument:
                instrument = requested_instrument
                areas = projeto.criar_areas(INSTRUMENTOS[instrument])
                validar_areas(areas)
                strike = False
                height_volume = False
                flashes.clear()
                view.trail.clear()
                pinch.reset()
                strike_gate.reset()
                audio.stop()
                keyboard_hits.clear()

            if camera:
                rgb, observation = camera.read(now)
            else:
                rgb = None
                cursor = view.mouse_cursor(pygame.mouse.get_pos())
                down = pygame.mouse.get_pressed()[0]
                observation = Observation(cursor, (0.1 if down else 1.0) if cursor else None)

            # As duas funções abaixo são a ponte direta para o arquivo dos alunos.
            cursor = observation.cursor
            area_selecionada = projeto.encontrar_area(areas, *cursor) if cursor is not None else None
            pinca_iniciada = pinch.update(observation.pinch_ratio, now)
            volume = (projeto.volume_pela_altura(cursor[1])
                      if height_volume and cursor is not None else 0.8)
            if strike:
                area_batida = strike_gate.update(cursor, areas, now)
                som = projeto.escolher_som(area_batida, area_batida is not None)
                area_acionada = area_batida
            else:
                som = projeto.escolher_som(area_selecionada, pinca_iniciada)
                area_acionada = area_selecionada

            if som is not None:
                audio.play(som, volume)
                hit_count += 1
                if area_acionada is not None:
                    flashes[area_acionada["id"]] = now + 0.18
            for area in keyboard_hits:
                audio.play(area["som"], volume)
                flashes[area["id"]] = now + 0.18
                hit_count += 1

            status = ("BATIDA ATIVA" if cursor else "SEM CURSOR") if strike else pinch.status
            if args.input_mode == "mouse" and not strike:
                status = "CLIQUE PARA TOCAR" if pinch.armed else "SOLTE O BOTAO" if cursor else "APONTE PARA O PAINEL"
            view.render(project=projeto, version=args.version, instrument=instrument,
                        pads=areas, selected=area_selecionada, cursor=cursor, observation=observation,
                        rgb=rgb, flashes=flashes, now=now, status=status,
                        hit_count=hit_count, fps=clock.get_fps(), input_mode=args.input_mode,
                        strike=strike, height_volume=height_volume, muted=audio.muted,
                        show_hand=show_hand)
            frame_count += 1
            if args.frames and frame_count >= args.frames:
                break
            clock.tick(30)

        if args.screenshot:
            view.save(args.screenshot)
    finally:
        if camera:
            camera.close()
        pygame.quit()

