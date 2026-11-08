"""Integração real em SDL dummy: não abre janela nem acessa uma webcam."""

import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
if os.name != "nt":
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/air-band-matplotlib")

from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import wave

import numpy as np
import pygame

from app import parse_args
from versions.day1 import project as day1
from workshop.audio import AudioBank
from workshop.config import ROOT
from workshop.drawing import HEIGHT, STAGE, WIDTH, View
from workshop.runtime import run
from workshop.tracking import CameraTracker


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.desktop = patch("pygame.display.get_desktop_sizes", return_value=[(1920, 1080)])
        self.desktop.start()
        self.addCleanup(self.desktop.stop)

    def tearDown(self):
        pygame.quit()

    def test_all_scenes_render_and_save(self):
        scenes = [("starter", "soundboard"), ("day1", "soundboard")] + [
            ("instructor", mode) for mode in ("soundboard", "drums", "keyboard", "effects")]
        with tempfile.TemporaryDirectory() as directory:
            for version, mode in scenes:
                output = Path(directory) / f"{version}-{mode}.png"
                run(parse_args(["--version", version, "--instrument", mode,
                                "--input", "mouse", "--mute", "--frames", "2", "--screenshot", str(output)]))
                self.assertGreater(output.stat().st_size, 2000)

    def test_small_window_preserves_cursor_and_tab_coordinates(self):
        pygame.display.init()
        pygame.font.init()
        with patch("pygame.display.get_desktop_sizes", return_value=[(1280, 720)]):
            view = View(ROOT / "assets" / "images")
        width, height = pygame.display.get_surface().get_size()
        self.assertLessEqual(height, 720 - 96)
        physical = ((STAGE.centerx * width / WIDTH), (STAGE.centery * height / HEIGHT))
        cursor = view.mouse_cursor(physical)
        self.assertAlmostEqual(cursor[0], 0.5)
        self.assertAlmostEqual(cursor[1], 0.5, places=2)
        tab = (400 * width / WIDTH, 130 * height / HEIGHT)
        self.assertEqual(view.tab_at(tab), "keyboard")

    def test_custom_image_uses_the_portuguese_area_key(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            image_dir = root / "assets" / "images"
            image_dir.mkdir(parents=True)
            image_path = image_dir / "bumbo.png"
            image = pygame.Surface((32, 32), pygame.SRCALPHA)
            image.fill((55, 220, 190, 180))
            pygame.image.save(image, str(image_path))
            areas = day1.criar_areas()
            areas[0]["imagem"] = "bumbo.png"
            with patch("workshop.runtime.ROOT", root), \
                 patch.object(day1, "criar_areas", return_value=areas), \
                 patch("pygame.image.load", wraps=pygame.image.load) as load:
                run(parse_args(["--version", "day1", "--input", "mouse", "--mute", "--frames", "1"]))
            load.assert_called_once_with(str(image_path))

    def test_mouse_pinch_path_plays_once_per_click(self):
        position = (STAGE.x + int(0.2 * STAGE.width), STAGE.y + int(0.3 * STAGE.height))
        with patch("pygame.mouse.get_pos", return_value=position), \
             patch("pygame.mouse.get_pressed", side_effect=[(False, 0, 0), (True, 0, 0), (True, 0, 0)]), \
             patch.object(AudioBank, "play", autospec=True) as play:
            run(parse_args(["--version", "day1", "--input", "mouse", "--frames", "3"]))
        self.assertEqual(play.call_count, 1)
        self.assertEqual(play.call_args.args[1], "kick.wav")

    def test_physical_key_can_test_starter_audio_before_tasks_are_done(self):
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_1)
        with patch("pygame.event.get", return_value=[event]), patch.object(AudioBank, "play", autospec=True) as play:
            run(parse_args(["--version", "starter", "--input", "mouse", "--frames", "1"]))
        self.assertEqual(play.call_args.args[1], "kick.wav")

    def test_instructor_can_switch_to_keyboard_and_enable_volume(self):
        events = [[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F3)],
                  [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_v)], []]
        with patch("pygame.event.get", side_effect=events):
            run(parse_args(["--version", "instructor", "--input", "mouse", "--mute", "--frames", "3"]))

    def test_samples_and_overlapping_audio(self):
        files = sorted((ROOT / "assets" / "sounds").glob("*.wav"))
        self.assertEqual(len(files), 13)
        for path in files:
            with wave.open(str(path)) as sound:
                self.assertEqual((sound.getnchannels(), sound.getsampwidth(), sound.getframerate()), (2, 2, 44100))
                self.assertGreater(sound.getnframes(), 1000)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        bank = AudioBank(ROOT / "assets" / "sounds", [path.name for path in files])
        bank.play("C4.wav", 0.3)
        bank.play("E4.wav", 0.8)
        self.assertEqual(sum(pygame.mixer.Channel(i).get_busy() for i in range(32)), 2)

    def test_actual_model_and_camera_pipeline_on_blank_frame(self):
        if not (ROOT / "models" / "hand_landmarker.task").is_file():
            self.skipTest("Execute scripts/prepare_model.py para validar o modelo.")
        capture = unittest.mock.Mock()
        capture.isOpened.return_value = True
        capture.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        with patch("cv2.VideoCapture", return_value=capture):
            tracker = CameraTracker(ROOT / "models" / "hand_landmarker.task")
            try:
                rgb, observation = tracker.read(1)
                self.assertEqual(rgb.shape, (360, 640, 3))
                self.assertIsNone(observation.cursor)
                # Mesmo horário de entrada ainda produz timestamps crescentes.
                tracker.read(1)
                self.assertEqual(tracker.timestamp, 1001)
            finally:
                tracker.close()
        capture.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()
