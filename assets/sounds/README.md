# Sons

As 13 amostras WAV incluídas são sintetizadas pelo código original de
`scripts/generate_sounds.py`; não são gravações nem amostras de terceiros.

Substitua os arquivos pelos seus sons, preservando os nomes, ou altere `som`
nos pads. O programa deve ser reiniciado depois de trocar os arquivos.

Formato recomendado: WAV PCM de 16 bits, 44.100 Hz, estéreo. Remova silêncio
inicial e ajuste o volume dos arquivos para um conjunto equilibrado.

- Bateria: `kick.wav`, `snare.wav`, `hihat.wav`, `clap.wav`.
- Notas: `C4.wav`, `D4.wav`, `E4.wav`, `G4.wav`, `A4.wav`.
- Efeitos: `laser.wav`, `coin.wav`, `space.wav`, `powerup.wav`.

`python scripts/generate_sounds.py` cria somente arquivos ausentes.
`--force` recria todos e sobrescreve personalizações; use-o somente quando desejar.

