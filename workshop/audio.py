"""Amostras carregadas uma vez; cada execução pode usar um canal diferente."""

class AudioBank:
    def __init__(self, sound_dir, filenames, muted=False):
        import pygame

        self.pygame = pygame
        self.muted = muted
        self.sounds = {}
        missing = [name for name in set(filenames) if not (sound_dir / name).is_file()]
        if missing:
            raise RuntimeError("Audios ausentes: " + ", ".join(sorted(missing))
                               + ". Execute: python scripts/generate_sounds.py")
        if not pygame.mixer.get_init():
            raise RuntimeError("Audio indisponivel. Verifique a saida de som ou execute com --mute.")
        pygame.mixer.set_num_channels(32)
        for name in set(filenames):
            try:
                self.sounds[name] = pygame.mixer.Sound(str(sound_dir / name))
            except pygame.error as error:
                raise RuntimeError(f"Nao foi possivel ler {name}: {error}") from error

    def play(self, filename, volume=1.0):
        if self.muted:
            return
        if filename not in self.sounds:
            raise RuntimeError(f"Som nao carregado: {filename}. Confira criar_areas e escolher_som.")
        channel = self.pygame.mixer.find_channel(force=True)
        channel.set_volume(max(0.0, min(1.0, volume)))
        channel.play(self.sounds[filename])

    def stop(self):
        self.pygame.mixer.stop()


class SilentAudio:
    """Permite ensaiar lógica e imagem com --mute mesmo sem dispositivo de áudio."""

    muted = True

    def play(self, filename, volume=1.0):
        pass

    def stop(self):
        pass

