"""Câmera e MediaPipe isolados do código das atividades."""

from dataclasses import dataclass
import math
import os
from typing import Optional


@dataclass
class Observation:
    cursor: Optional[tuple]
    pinch_ratio: Optional[float]
    landmarks: tuple = ()


def observation_from_landmarks(landmarks, width, height):
    """Distâncias em pixels preservam a proporção da imagem."""
    if len(landmarks) != 21:
        return Observation(None, None)

    def distance(a, b):
        return math.hypot((landmarks[a].x - landmarks[b].x) * width,
                          (landmarks[a].y - landmarks[b].y) * height)

    palm_width = distance(5, 17)
    if palm_width < 1:
        return Observation(None, None)
    tip = landmarks[8]
    return Observation(
        (tip.x, tip.y), distance(4, 8) / palm_width,
        tuple((point.x, point.y) for point in landmarks),
    )


class CameraTracker:
    def __init__(self, model_path, camera_index=0):
        import cv2
        import mediapipe as mp

        if not model_path.is_file():
            raise RuntimeError("Modelo ausente. Execute: python scripts/prepare_model.py")

        self.cv2 = cv2
        self.mp = mp
        self.camera = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW) if os.name == "nt" else cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            self.camera.release()
            raise RuntimeError("Nao foi possivel abrir a webcam. Feche outros aplicativos ou use --input mouse.")
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=mp.tasks.BaseOptions(model_asset_path=str(model_path)),
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.55,
            min_hand_presence_confidence=0.55,
            min_tracking_confidence=0.55,
        )
        try:
            self.detector = mp.tasks.vision.HandLandmarker.create_from_options(options)
        except Exception:
            self.camera.release()
            raise
        self.timestamp = -1

    def read(self, now):
        cv2 = self.cv2
        ok, frame = self.camera.read()
        if not ok:
            raise RuntimeError("A webcam parou de enviar imagens. Verifique a conexao ou use --input mouse.")
        # Um único espelhamento, antes da inferência e da exibição.
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        target_ratio = 16 / 9
        if width / height > target_ratio:
            cropped_width = int(height * target_ratio)
            left = (width - cropped_width) // 2
            frame = frame[:, left:left + cropped_width]
        else:
            cropped_height = int(width / target_ratio)
            top = (height - cropped_height) // 2
            frame = frame[top:top + cropped_height, :]
        rgb = cv2.cvtColor(cv2.resize(frame, (640, 360)), cv2.COLOR_BGR2RGB)
        timestamp = max(self.timestamp + 1, int(now * 1000))
        self.timestamp = timestamp
        result = self.detector.detect_for_video(
            self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=rgb), timestamp)
        observation = (observation_from_landmarks(result.hand_landmarks[0], 640, 360)
                       if result.hand_landmarks else Observation(None, None))
        return rgb, observation

    def close(self):
        self.detector.close()
        self.camera.release()

