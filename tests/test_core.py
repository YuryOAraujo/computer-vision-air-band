"""Regras que podem ser verificadas sem webcam nem dependências externas."""

import math
from types import SimpleNamespace
import unittest

from app import parse_args
from versions.day1 import project
from versions.instructor import project as instructor
from versions.starter import project as starter
from workshop.config import validate_pads
from workshop.gestures import PinchGate, StrikeGate
from workshop.tracking import observation_from_landmarks


class PinchTests(unittest.TestCase):
    def test_hold_release_and_tracking_loss(self):
        gate = PinchGate()
        ratios = [0.1, 0.1, 1.0, 0.1, 0.1, 0.45, 0.1, None, 0.1, 1.0, 0.1]
        events = [gate.update(ratio, index * 0.2) for index, ratio in enumerate(ratios)]
        self.assertEqual([index for index, event in enumerate(events) if event], [3, 10])

    def test_hysteresis_and_new_pinch(self):
        gate = PinchGate()
        ratios = [0.8, 0.34, 0.4, 0.36, 0.33, 0.5, 0.61, 0.34]
        self.assertEqual(sum(gate.update(ratio, i * 0.2) for i, ratio in enumerate(ratios)), 2)

    def test_cooldown_consumes_closed_gesture(self):
        gate = PinchGate(cooldown=0.2)
        gate.update(1, 0)
        self.assertTrue(gate.update(0.1, 0.1))
        gate.update(1, 0.12)
        self.assertFalse(gate.update(0.1, 0.15))
        self.assertFalse(gate.update(0.1, 0.8))
        gate.update(1, 0.9)
        self.assertTrue(gate.update(0.1, 1))

    def test_invalid_observation_disarms(self):
        gate = PinchGate()
        gate.update(1, 0)
        gate.update(float("nan"), 0.2)
        self.assertFalse(gate.update(0.1, 0.4))

    def test_a_pinch_cannot_play_again_by_moving_between_pads(self):
        gate = PinchGate()
        pads = project.build_pads()
        sequence = [(0.2, 0.3, 1), (0.2, 0.3, 0.1), (0.6, 0.3, 0.1),
                    (0.6, 0.3, 1), (0.6, 0.3, 0.1)]
        sounds = []
        for index, (x, y, ratio) in enumerate(sequence):
            sound = project.choose_sound(project.find_pad(pads, x, y), gate.update(ratio, index * 0.2))
            if sound:
                sounds.append(sound)
        self.assertEqual(sounds, ["kick.wav", "snare.wav"])

    def test_pinch_outside_a_pad_is_consumed(self):
        gate = PinchGate()
        gate.update(1, 0)
        self.assertIsNone(project.choose_sound(None, gate.update(0.1, 0.2)))
        self.assertFalse(gate.update(0.1, 0.4))


class StrikeTests(unittest.TestCase):
    def setUp(self):
        self.gate = StrikeGate()
        self.pads = instructor.build_pads("drums")

    def test_strike_requires_crossing_and_rearming(self):
        self.assertIsNone(self.gate.update((0.15, 0.3), self.pads, 0))
        self.assertEqual(self.gate.update((0.15, 0.5), self.pads, 0.1)["id"], "kick")
        self.assertIsNone(self.gate.update((0.15, 0.6), self.pads, 0.2))
        self.assertIsNone(self.gate.update((0.15, 0.42), self.pads, 0.3))
        self.assertIsNone(self.gate.update((0.15, 0.5), self.pads, 0.4))
        self.gate.update((0.15, 0.3), self.pads, 0.5)
        self.assertEqual(self.gate.update((0.15, 0.5), self.pads, 0.6)["id"], "kick")

    def test_reappearing_inside_pad_does_not_strike(self):
        self.gate.update((0.15, 0.3), self.pads, 0)
        self.gate.update(None, self.pads, 0.1)
        self.assertIsNone(self.gate.update((0.15, 0.6), self.pads, 0.2))

    def test_slow_crossing_is_not_a_strike(self):
        self.gate.update((0.15, 0.35), self.pads, 0)
        self.gate.update((0.15, 0.42), self.pads, 0.2)
        self.assertIsNone(self.gate.update((0.15, 0.44), self.pads, 0.4))

    def test_long_gap_does_not_create_a_strike(self):
        self.gate.update((0.15, 0.3), self.pads, 0)
        self.assertIsNone(self.gate.update((0.15, 0.6), self.pads, 1))

    def test_diagonal_trajectory_uses_crossing_position(self):
        self.gate.update((0.1, 0.3), self.pads, 0)
        pad = self.gate.update((0.39, 0.6), self.pads, 0.1)
        self.assertEqual(pad["id"], "kick")


class ProjectTests(unittest.TestCase):
    def test_all_completed_layouts_have_working_centers_and_sounds(self):
        for module, name in [(project, "soundboard")] + [(instructor, name) for name in
                                                      ("soundboard", "drums", "keyboard", "effects")]:
            pads = module.build_pads(name)
            validate_pads(pads)
            for pad in pads:
                x, y, width, height = pad["rect"]
                selected = module.find_pad(pads, x + width / 2, y + height / 2)
                self.assertIs(selected, pad)
                self.assertEqual(module.choose_sound(selected, True), pad["sound"])
                self.assertIsNone(module.choose_sound(selected, False))
            self.assertIsNone(module.find_pad(pads, 0, 0))

    def test_starter_runs_with_intentionally_incomplete_tasks(self):
        pads = starter.build_pads()
        validate_pads(pads)
        self.assertIsNone(starter.find_pad(pads, 0.5, 0.5))
        self.assertIsNone(starter.choose_sound(pads[0], True))

    def test_bad_layout_gives_an_actionable_error(self):
        pad = dict(project.build_pads()[0], rect=(0.8, 0, 0.5, 0.5))
        with self.assertRaisesRegex(ValueError, "rect"):
            validate_pads([pad])

    def test_volume_is_bounded(self):
        self.assertEqual(instructor.volume_from_height(-1), 1)
        self.assertEqual(instructor.volume_from_height(2), 0.2)
        self.assertAlmostEqual(instructor.volume_from_height(0.5), 0.5)

    def test_ratio_uses_both_image_dimensions(self):
        landmarks = [SimpleNamespace(x=0.5, y=0.5) for _ in range(21)]
        landmarks[17] = SimpleNamespace(x=0.6, y=0.5)
        landmarks[8] = SimpleNamespace(x=0.52, y=0.52)
        observed = observation_from_landmarks(landmarks, 640, 360)
        self.assertAlmostEqual(observed.pinch_ratio, math.hypot(12.8, 7.2) / 64)
        self.assertEqual(observed.cursor, (0.52, 0.52))

    def test_degenerate_hand_is_absent(self):
        landmarks = [SimpleNamespace(x=0.5, y=0.5) for _ in range(21)]
        self.assertIsNone(observation_from_landmarks(landmarks, 640, 360).cursor)

    def test_cli_defaults_and_extension_options(self):
        self.assertEqual(parse_args([]).version, "starter")
        self.assertEqual(parse_args(["--version", "instructor"]).version, "instructor")
        self.assertTrue(parse_args(["--version", "instructor", "--instrument", "drums", "--strike"]).strike)


if __name__ == "__main__":
    unittest.main()

