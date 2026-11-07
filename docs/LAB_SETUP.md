# Preparação do laboratório

## Antes de instalar

Use Windows de 64 bits e Python 3.12 de 64 bits em todas as estações. Confira:

```powershell
py -3.12 --version
py -3.12 -c "import struct; print(struct.calcsize('P') * 8)"
```

A segunda linha deve mostrar `64`. O Python do sistema pode ser outro; o comando
`py -3.12` seleciona explicitamente a versão do workshop.

O projeto executa o reconhecimento em CPU. Não exige instalação de CUDA nem
configuração da RTX. Use uma pasta local com permissão de escrita, fora de pastas
de sincronização que possam interferir nos arquivos durante a aula.

## Preparação com internet

Execute `preparar_windows.bat`. Equivalente manual:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements-lock.txt
.\.venv\Scripts\python.exe scripts/generate_sounds.py
.\.venv\Scripts\python.exe scripts/prepare_model.py
.\.venv\Scripts\python.exe app.py --version instructor --input mouse
```

Não é necessário ativar o ambiente virtual ou alterar a política do PowerShell.
Abra o projeto no VS Code e selecione `.\.venv\Scripts\python.exe` como interpretador.

As dependências diretas são MediaPipe Tasks, OpenCV contrib, NumPy e Pygame.
Use somente a distribuição OpenCV fixada no arquivo; instalar outra distribuição
que também fornece `cv2` no mesmo ambiente pode causar conflitos.

## Preparação offline

Em **uma estação Windows de 64 bits com Python 3.12**, após preparar o ambiente:
use o projeto completo ou o pacote instructor para esta etapa de distribuição.

```powershell
.\.venv\Scripts\python.exe -m pip download --only-binary=:all: -r requirements-lock.txt -d wheelhouse
.\.venv\Scripts\python.exe scripts/package_workshop.py --include-wheels
```

Os ZIPs incluirão os wheels, o modelo, os sons e o código. Nas outras estações,
extraia o pacote e execute `preparar_windows.bat`; a presença de `wheelhouse/` faz
a instalação usar `--no-index`. O script do modelo apenas verifica o arquivo já
presente. O Python 3.12 precisa estar instalado previamente em cada estação.

**Não copie a pasta `.venv` entre computadores.** Os caminhos e binários do
ambiente são específicos da instalação. Gere os wheels no Windows para o
workshop Windows; o pacote de um sistema diferente pode não servir.

## Ensaio de cada estação

1. Execute a referência com `--input mouse`; teste todos os instrumentos e as teclas numéricas.
2. Execute com `--input camera`; confirme alinhamento do cursor com a imagem espelhada.
3. Abra a mão, selecione um pad e faça a pinça. Segure: apenas um toque. Solte e repita.
4. Feche a pinça fora dos pads e entre em um deles: não deve tocar até abrir e fazer outra pinça.
5. Retire a mão. Recoloque-a fechada: deve aguardar abertura antes de aceitar um toque.
6. Faça uma sequência de sons e ouça a sobreposição, sem uma chamada bloquear a próxima.
7. Na bateria com `B`, suba acima da borda do pad e desça. Permanecer dentro não repete a batida.
8. Desconecte a internet e repita o teste principal.
9. Abra o starter, edite uma cor, salve e reinicie. Confira o interpretador usado pelo editor.

Mantenha o checkpoint pronto para recuperar uma dupla. Use fones nas atividades
e caixas apenas nas demonstrações coletivas.

## Resolução de problemas

| Sintoma | Ação |
| --- | --- |
| `py` não foi encontrado | Reinstale Python 3.12 com o Python Launcher; confirme a instalação antes da aula |
| `No matching distribution` | Confira Python 3.12 de 64 bits e o lock; não tente compilar dependências durante o workshop |
| Câmera não abre | Feche Teams, navegador e outros consumidores de câmera; confira permissões de câmera para aplicativos de desktop no Windows; tente `--camera 1` |
| Precisa continuar sem webcam | Use `--input mouse` |
| O programa mostra apenas um pad e tarefas para completar | Está na versão starter; use `--version instructor` para a demonstração completa |
| O starter não toca por gesto | Complete `find_pad` e `choose_sound`; use `1` para confirmar o áudio |
| Rastreamento mostra mão, mas não toca | Abra polegar e indicador primeiro; verifique se o cursor está dentro do pad; ajuste iluminação e distância |
| Dedos fechados repetem sons | Confira se `choose_sound` usa `pinch_started`; não use a condição de dedos fechados em todos os quadros |
| Áudio não inicializa | Confira o dispositivo padrão do Windows e a conexão dos fones; `--mute` permite continuar a lógica |
| Som perceptivelmente atrasado | Retire silêncio do início dos WAVs e teste saída com fio; ensaie eventual ajuste de buffer no `runtime.py` |
| `Som nao carregado` | Faça `choose_sound` devolver um `sound` declarado nos pads; reinicie depois de alterar os arquivos |
| `Imagem nao encontrada` | Confira `assets/images/` e a grafia de `image` no pad |
| Modelo ausente ou corrompido | Antes da aula, execute `scripts/prepare_model.py` com internet; a verificação SHA-256 confirma o arquivo |
| `M` não ativa áudio | Se iniciou com `--mute`, reinicie sem essa opção |

Os limiares da pinça ficam em `workshop/gestures.py`: `0.35` para fechar e `0.60`
para abrir, relativos à largura da palma. Ajuste somente após experimentar na
posição e iluminação previstas. Os valores são pontos de partida, não uma
calibração universal.

