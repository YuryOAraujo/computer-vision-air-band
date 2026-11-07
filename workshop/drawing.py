"""Uma janela Pygame: vídeo, regiões, imagens opcionais e instruções."""

import math
from pathlib import Path

import pygame

WIDTH, HEIGHT = 1120, 820
STAGE = pygame.Rect(24, 166, 1072, 603)
BACKGROUND = (11, 16, 30)
TEXT = (235, 242, 255)
MUTED = (143, 160, 187)
ACCENT = (55, 220, 190)
TABS = [("soundboard", "F1  PAINEL"), ("drums", "F2  BATERIA"),
        ("keyboard", "F3  TECLADO"), ("effects", "F4  EFEITOS")]
CONNECTIONS = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7),
               (7, 8), (5, 9), (9, 10), (10, 11), (11, 12), (9, 13),
               (13, 14), (14, 15), (15, 16), (13, 17), (0, 17),
               (17, 18), (18, 19), (19, 20))


class View:
    def __init__(self, image_dir):
        desktop_width, desktop_height = pygame.display.get_desktop_sizes()[0]
        scale = min(1.0, max(0.35, (desktop_width - 64) / WIDTH),
                    max(0.35, (desktop_height - 96) / HEIGHT))
        pygame.display.set_mode((round(WIDTH * scale), round(HEIGHT * scale)), pygame.RESIZABLE)
        # Canvas lógico fixo: a janela pode caber em notebooks com escala do Windows.
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        pygame.display.set_caption("Air Band Lab | Workshop TOP de Programacao")
        self.fonts = {size: pygame.font.SysFont("segoeui,dejavusans,arial", size)
                      for size in (13, 15, 17, 20, 26, 36)}
        self.image_dir = image_dir
        self.images = {}
        self.trail = []

    def text(self, value, position, size=17, color=TEXT, center=False):
        rendered = self.fonts[size].render(str(value), True, color)
        rectangle = rendered.get_rect(center=position) if center else rendered.get_rect(topleft=position)
        self.screen.blit(rendered, rectangle)

    def tab_at(self, position):
        position = self.logical_position(position)
        for index, (instrument, _) in enumerate(TABS):
            if pygame.Rect(24 + index * 180, 112, 170, 36).collidepoint(position):
                return instrument
        return None

    def mouse_cursor(self, position):
        position = self.logical_position(position)
        if not STAGE.collidepoint(position):
            return None
        return ((position[0] - STAGE.x) / STAGE.width,
                (position[1] - STAGE.y) / STAGE.height)

    def logical_position(self, position):
        width, height = pygame.display.get_surface().get_size()
        return (position[0] * WIDTH / width, position[1] * HEIGHT / height)

    def image(self, filename, size):
        key = (filename, size)
        if key not in self.images:
            path = self.image_dir / filename
            try:
                image = pygame.image.load(str(path)).convert_alpha()
                self.images[key] = pygame.transform.smoothscale(image, size)
            except (pygame.error, FileNotFoundError) as error:
                raise RuntimeError(f"Imagem nao encontrada ou invalida: {path}") from error
        return self.images[key]

    def render(self, *, project, version, instrument, pads, selected, cursor,
               observation, rgb, flashes, now, status, hit_count, fps,
               input_mode, strike, height_volume, muted, show_hand):
        screen = self.screen
        screen.fill(BACKGROUND)
        self.text("AIR BAND", (24, 12), 36)
        self.text("LAB / TOP DE PROGRAMACAO", (236, 30), 15, ACCENT)
        self.text(project.TITLE, (24, 62), 20)
        self.text(project.MISSION, (24, 89), 15, MUTED)
        self.text(f"{hit_count:03d}  TOQUES", (903, 19), 20, ACCENT)
        self.text(f"{fps:02.0f} FPS  |  {'MUDO' if muted else 'SOM ATIVO'}", (903, 51), 13, MUTED)

        if version == "instructor":
            for index, (name, label) in enumerate(TABS):
                rectangle = pygame.Rect(24 + index * 180, 112, 170, 36)
                pygame.draw.rect(screen, (31, 65, 70) if instrument == name else (24, 33, 51), rectangle, border_radius=9)
                self.text(label, rectangle.center, 15, ACCENT if instrument == name else MUTED, center=True)
        else:
            self.text("INICIO / EXPLORAR" if version == "starter" else "DIA 1 / PAINEL COMPLETO", (24, 122), 15, ACCENT)
        self.text(status, (800, 122), 15, ACCENT)

        if rgb is not None:
            camera_surface = pygame.image.frombuffer(rgb.tobytes(), (640, 360), "RGB")
            screen.blit(pygame.transform.smoothscale(camera_surface, STAGE.size), STAGE)
            shade = pygame.Surface(STAGE.size, pygame.SRCALPHA)
            shade.fill((5, 10, 22, 92))
            screen.blit(shade, STAGE)
        else:
            pygame.draw.rect(screen, (16, 25, 43), STAGE, border_radius=14)
            for x in range(STAGE.left, STAGE.right, 40):
                pygame.draw.line(screen, (23, 35, 54), (x, STAGE.top), (x, STAGE.bottom))
            for y in range(STAGE.top, STAGE.bottom, 40):
                pygame.draw.line(screen, (23, 35, 54), (STAGE.left, y), (STAGE.right, y))

        # Todo desenho de mão e pads é recortado na área do vídeo.
        screen.set_clip(STAGE)
        for index, pad in enumerate(pads):
            x, y, width, height = pad["rect"]
            rectangle = pygame.Rect(STAGE.x + round(x * STAGE.width), STAGE.y + round(y * STAGE.height),
                                    round(width * STAGE.width), round(height * STAGE.height))
            active = flashes.get(pad["id"], -1) > now
            hovering = selected is not None and selected["id"] == pad["id"]
            color = pad["color"]
            fill = pygame.Surface(rectangle.size, pygame.SRCALPHA)
            pygame.draw.rect(fill, (*color, 155 if active else 55 if hovering else 24), fill.get_rect(), border_radius=18)
            screen.blit(fill, rectangle)
            pygame.draw.rect(screen, color, rectangle, 4 if active else 3 if hovering else 1, border_radius=18)
            if "image" in pad:
                side = max(24, min(rectangle.width // 3, rectangle.height // 3, 90))
                screen.blit(self.image(pad["image"], (side, side)),
                            (rectangle.centerx - side // 2, rectangle.centery - side - 6))
            else:
                # Pequena forma de onda desenhada por código: nenhum asset necessário.
                for bar in range(11):
                    amplitude = 5 + abs(math.sin(bar * 1.4 + index)) * (23 if active else 13)
                    bx = rectangle.centerx - 35 + bar * 7
                    by = rectangle.centery - 35
                    pygame.draw.line(screen, color, (bx, by - amplitude), (bx, by + amplitude), 3)
            self.text(pad["label"], (rectangle.centerx, rectangle.centery + 13),
                      26 if rectangle.width > 200 else 20, center=True)
            self.text(f"[ {index + 1} ]", (rectangle.centerx, rectangle.bottom - 25), 15, color, center=True)
            if strike:
                pygame.draw.line(screen, color, (rectangle.left + 15, rectangle.top + 6),
                                 (rectangle.right - 15, rectangle.top + 6), 4)

        if show_hand and observation.landmarks:
            points = [(STAGE.x + int(x * STAGE.width), STAGE.y + int(y * STAGE.height))
                      for x, y in observation.landmarks]
            for a, b in CONNECTIONS:
                pygame.draw.line(screen, (106, 193, 202), points[a], points[b], 2)
            for point in points:
                pygame.draw.circle(screen, (207, 252, 242), point, 3)
        if cursor is not None:
            point = (STAGE.x + int(cursor[0] * STAGE.width), STAGE.y + int(cursor[1] * STAGE.height))
            self.trail.append(point)
            self.trail = self.trail[-7:]
            for index, old_point in enumerate(self.trail[:-1]):
                pygame.draw.circle(screen, (49, 100 + index * 12, 117), old_point, 2 + index)
            pygame.draw.circle(screen, TEXT, point, 14, 2)
            pygame.draw.circle(screen, ACCENT, point, 5)
        else:
            self.trail.clear()
        screen.set_clip(None)

        action = "Desca pela borda do pad" if strike else "Aponte e feche a pinca" if input_mode == "camera" else "Aponte e clique"
        modifiers = ("  |  B: batida" + (" ON" if strike else " OFF")) if instrument == "drums" and version == "instructor" else ""
        modifiers += ("  |  V: volume" + (" ON" if height_volume else " OFF")) if instrument == "keyboard" and version == "instructor" else ""
        self.text(action + modifiers, (24, 781), 15, ACCENT)
        self.text("1-9: sons  |  R: rearmar  |  H: mao  |  M: som  |  ESC: sair", (594, 784), 13, MUTED)
        window = pygame.display.get_surface()
        window.blit(pygame.transform.smoothscale(screen, window.get_size()), (0, 0))
        pygame.display.flip()

    def save(self, filename):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        pygame.image.save(self.screen, str(path))

