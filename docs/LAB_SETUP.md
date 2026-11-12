# Preparação do laboratório

## Antes de instalar

Use Windows de 64 bits e o Python 3.8.2 de 64 bits já instalado nas estações.
Não é necessário acessar a Microsoft Store nem reinstalar o Python. Versões
posteriores da série 3.8 também são aceitas. Confira:

```powershell
py -3.8 --version
py -3.8 -c "import struct; print(struct.calcsize('P') * 8)"
```

A segunda linha deve mostrar `64`. O Python do sistema pode ser outro; o comando
`py -3.8` seleciona explicitamente a versão do workshop. Se `py` não estiver
disponível, use o caminho do interpretador existente, por exemplo no PowerShell:

```powershell
& "C:\caminho\para\python.exe" --version
& "C:\caminho\para\python.exe" -c "import struct; print(struct.calcsize('P') * 8)"
```

Se mostrar `32`, essa instalação não pode executar o MediaPipe usado aqui; será
necessário obter Python de 64 bits com a equipe de TI. A série 3.8
[não recebe atualizações desde outubro de 2024](https://www.python.org/downloads/release/python-382/);
esta configuração aproveita a instalação existente na escola.

O projeto executa o reconhecimento em CPU. Não exige instalação de CUDA nem
configuração da RTX. Use uma pasta local com permissão de escrita, fora de pastas
de sincronização que possam interferir nos arquivos durante a aula.

## Preparação com internet

Execute `preparar_windows.bat`. Equivalente manual:

```powershell
py -3.8 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: pip==25.0.1
.\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r requirements-lock.txt
.\.venv\Scripts\python.exe scripts/generate_sounds.py
.\.venv\Scripts\python.exe scripts/prepare_model.py
.\.venv\Scripts\python.exe app.py --version instructor --input mouse
```

O preparador procura `py -3.8` e depois uma instalação compatível no `PATH`,
ignorando o atalho da Microsoft Store. Para informar o caminho diretamente:

```powershell
.\preparar_windows.bat "C:\caminho\para\python.exe"
```

No procedimento manual, também é possível substituir `py -3.8` por
`& "C:\caminho\para\python.exe"`. Se já existir uma `.venv` criada com Python
3.12, mova essa pasta para fora do projeto e execute a preparação novamente;
o script recusa um ambiente de outra versão e não o apaga automaticamente.

Não é necessário ativar o ambiente virtual ou alterar a política do PowerShell.
Abra o projeto no VS Code e selecione `.\.venv\Scripts\python.exe` como interpretador.

O preparador instala pip **25.0.1** dentro da `.venv`: ele ainda suporta Python
3.8 e reconhece os wheels de OpenCV no Windows. O pip original do Python 3.8.2
pode recusar esses arquivos. A instalação do Python do sistema não é alterada.

As dependências diretas são MediaPipe Tasks, OpenCV contrib, NumPy e Pygame.
Use somente a distribuição OpenCV fixada no arquivo; instalar outra distribuição
que também fornece `cv2` no mesmo ambiente pode causar conflitos.

## Preparação offline

Em **uma estação Windows de 64 bits com Python 3.8.2**, após preparar o ambiente:
use o projeto completo ou o pacote instructor para esta etapa de distribuição.

```powershell
.\.venv\Scripts\python.exe -m pip download --only-binary=:all: pip==25.0.1 -r requirements-lock.txt -d wheelhouse
.\.venv\Scripts\python.exe scripts/package_workshop.py --include-wheels
```

Os ZIPs incluirão os 24 wheels das dependências, o wheel do pip 25.0.1, o modelo,
os sons e o código. Nas outras estações,
extraia o pacote e execute `preparar_windows.bat`; a presença de `wheelhouse/` faz
a instalação usar `--no-index`. O script do modelo apenas verifica o arquivo já
presente. O Python 3.8 de 64 bits já instalado será usado para criar a `.venv`.

Ao migrar da configuração anterior com Python 3.12, gere uma nova pasta
`wheelhouse/` vazia e baixe novamente as dependências: os wheels e o lock antigos
não servem para esta configuração. Inclua também `pip==25.0.1` no download;
o preparador usa esse wheel antes de instalar as dependências, sem precisar de rede.

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
| `py` não foi encontrado | Execute `preparar_windows.bat "C:\caminho\para\python.exe"` usando o Python 3.8 de 64 bits existente |
| `python` abre a Microsoft Store | Informe o caminho real de `python.exe` ao preparador; ele também ignora esse atalho na busca automática |
| Ambiente `.venv` de outra versão | Mova a `.venv` antiga para fora do projeto e execute a preparação com Python 3.8 de 64 bits |
| `No matching distribution` | Confira Python 3.8.2 ou posterior da série 3.8, de 64 bits, o lock e wheels correspondentes; não tente compilar dependências durante o workshop |
| Câmera não abre | Feche Teams, navegador e outros consumidores de câmera; confira permissões de câmera para aplicativos de desktop no Windows; tente `--camera 1` |
| Precisa continuar sem webcam | Use `--input mouse` |
| O programa mostra apenas um pad e tarefas para completar | Está na versão starter; use `--version instructor` para a demonstração completa |
| O starter não toca por gesto | Complete `encontrar_area` e `escolher_som`; use `1` para confirmar o áudio |
| Rastreamento mostra mão, mas não toca | Abra polegar e indicador primeiro; verifique se o cursor está dentro do pad; ajuste iluminação e distância |
| Dedos fechados repetem sons | Confira se `escolher_som` usa `pinca_iniciada`; não use a condição de dedos fechados em todos os quadros |
| Áudio não inicializa | Confira o dispositivo padrão do Windows e a conexão dos fones; `--mute` permite continuar a lógica |
| Som perceptivelmente atrasado | Retire silêncio do início dos WAVs e teste saída com fio; ensaie eventual ajuste de buffer no `runtime.py` |
| `Som nao carregado` | Faça `escolher_som` devolver um `som` declarado nos pads; reinicie depois de alterar os arquivos |
| `Imagem nao encontrada` | Confira `assets/images/` e a grafia de `imagem` no pad |
| Modelo ausente ou corrompido | Antes da aula, execute `scripts/prepare_model.py` com internet; a verificação SHA-256 confirma o arquivo |
| `M` não ativa áudio | Se iniciou com `--mute`, reinicie sem essa opção |

Os limiares da pinça ficam em `workshop/gestures.py`: `0.35` para fechar e `0.60`
para abrir, relativos à largura da palma. Ajuste somente após experimentar na
posição e iluminação previstas. Os valores são pontos de partida, não uma
calibração universal.

