# Registro de validação — atualizado em 12/11/2026

## Ambiente usado

Linux x86_64, Python **3.8.2** em ambiente virtual isolado. Dependências diretas e
transitivas fixadas em `requirements-lock.txt`. GPU e webcam físicas não foram
utilizadas nos testes deste ambiente.

## Verificações

- **26 testes automatizados**: condições de seleção, layouts, pinça sustentada,
  histerese, cooldown, perda e retorno de mão, batidas descendentes, volume,
  desenho das seis combinações de versão/cena, redimensionamento, fluxo de mouse,
  teclas físicas, áudio simultâneo, imagem opcional com a chave `imagem` e pipeline
  real de câmera/modelo sobre quadro vazio. Todos passaram em Python 3.8.2 com
  MediaPipe 0.10.9, OpenCV contrib 4.9.0.80, NumPy 1.24.4 e Pygame 2.6.1 em 12/11/2026.
- Todos os arquivos Python do aplicativo, atividades, scripts e testes foram
  compilados com Python 3.8.2, sem erros de sintaxe.
- A reprodução foi verificada com o driver de áudio simulado do SDL, incluindo
  dois canais simultâneos. Isso verifica a integração, sem comprovar latência ou
  qualidade de uma saída de áudio física.
- **Inferência positiva real (12/11)**: o pipeline completo de câmera detectou 21 pontos
  da mão e calculou cursor e razão de pinça na foto usada
  pelo [exemplo oficial do MediaPipe](https://github.com/google-ai-edge/mediapipe-samples/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb).
  A imagem foi usada temporariamente para verificação e não está nos pacotes.
  Essa verificação confirma detecção de mão, sem substituir um ensaio de gestos ao vivo.
- **Windows x86_64 / CPython 3.8.2 (12/11)**: as **24 dependências** fixadas foram
  resolvidas e baixadas como wheels, com `--only-binary=:all:`. A resolução usou
  Python 3.8.2 para avaliar corretamente os marcadores de versão, com plataforma
  `win_amd64` e ABI `cp38`; não depende de compilar pacotes nos computadores da escola.
- **Preparação do pip**: o pip 19.2.3 original do Python 3.8.2 pode recusar o
  wheel `cp37-abi3` de OpenCV no Windows. O preparador instala primeiro pip 25.0.1
  na `.venv`, usando o wheel local quando presente. Essa atualização foi verificada
  sem rede, partindo de pip 19.2.3 em Python 3.8.2; a instalação do sistema é preservada.
- Os binários Windows e os arquivos `.bat` não foram executados neste ambiente
  Linux. Ainda é necessário ensaiar instalação, webcam e áudio no Windows da escola.
- Modelo oficial de 7.819.105 bytes, versão float16/1, verificado por SHA-256
  `fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1`.
- Três ZIPs extraídos em uma pasta temporária: integridade do arquivo, execução de
  cada versão com a infraestrutura incluída e verificação local do modelo sem download.
  Os pacotes starter/day1 não incluem a versão instructor nem o guia de respostas.
  Os três pacotes incluem o glossário com a interface em português.
  A distribuição local em `dist/` foi refeita com `--include-wheels` para Python
  3.8.2: cada ZIP também contém as 24 dependências Windows e pip 25.0.1 em `wheelhouse/`.
  A execução sem `--version` seleciona starter no projeto completo e a versão
  disponível nos pacotes individuais.
- A inspeção visual do teclado e a execução das respostas do guia do professor
  foram feitas na validação anterior (Python 3.12, 08/11). Nesta migração, o
  desenho das seis cenas foi verificado novamente pelos testes automatizados.

## Como repetir

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
.\.venv\Scripts\python.exe scripts/prepare_model.py
.\.venv\Scripts\python.exe scripts/package_workshop.py
```

Os testes usam SDL em modo simulado. Para confirmar a experiência física, execute
o [ensaio de cada estação](LAB_SETUP.md#ensaio-de-cada-estação) no Windows do laboratório,
com webcam, iluminação, fones e conta de usuário que serão usados no evento.

Os ZIPs locais atuais contêm código, modelo, sons, documentação e wheels Windows
para Python 3.8.2 de 64 bits. Extraia e execute `preparar_windows.bat` usando o
Python existente na escola; as dependências são instaladas sem rede na `.venv`.
Ao gerar novos pacotes, use `--include-wheels` para manter essa instalação offline,
conforme o [guia do laboratório](LAB_SETUP.md#preparação-offline).

