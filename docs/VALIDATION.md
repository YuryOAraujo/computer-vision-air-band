# Registro de validação — atualizado em 08/11/2026

## Ambiente usado

Linux x86_64, Python 3.12.16 em ambiente virtual isolado. Dependências diretas e
transitivas fixadas em `requirements-lock.txt`. GPU e webcam físicas não foram
utilizadas nos testes deste ambiente.

## Verificações

- **26 testes automatizados**: condições de seleção, layouts, pinça sustentada,
  histerese, cooldown, perda e retorno de mão, batidas descendentes, volume,
  desenho das seis combinações de versão/cena, redimensionamento, fluxo de mouse,
  teclas físicas, áudio simultâneo, imagem opcional com a chave `imagem` e pipeline
  real de câmera/modelo sobre quadro vazio. Executados novamente após a tradução
  das funções e dos dados das atividades em 08/11/2026.
- As funções de resposta do guia do professor foram executadas com os dados do
  starter: seleção da área, acionamento único e volume retornam os resultados esperados.
- A reprodução foi verificada com o driver de áudio simulado do SDL, incluindo
  dois canais simultâneos. Isso verifica a integração, sem comprovar latência ou
  qualidade de uma saída de áudio física.
- **Inferência positiva real (07/11)**: o pipeline detectou 21 pontos da mão na foto usada
  pelo [exemplo oficial do MediaPipe](https://github.com/google-ai-edge/mediapipe-samples/blob/main/examples/hand_landmarker/python/hand_landmarker.ipynb).
  A imagem foi usada temporariamente para verificação e não está nos pacotes.
  Essa verificação confirma detecção de mão, sem substituir um ensaio de gestos ao vivo.
- **Windows x86_64 / CPython 3.12 (07/11)**: resolução com `--only-binary :all:` e `--dry-run`
  confirmou disponibilidade de wheels compatíveis para as 20 dependências fixadas.
  Os binários Windows não foram executados neste ambiente Linux.
- Modelo oficial de 7.819.105 bytes, versão float16/1, verificado por SHA-256
  `fbc2a30080c3c557093b5ddfc334698132eb341044ccee322ccf8bcf3607cde1`.
- Três ZIPs extraídos em uma pasta temporária: integridade do arquivo, execução de
  cada versão com a infraestrutura incluída e verificação local do modelo sem download.
  Os pacotes starter/day1 não incluem a versão instructor nem o guia de respostas.
  Os três pacotes incluem o glossário com a interface em português.
  A execução sem `--version` seleciona starter no projeto completo e a versão
  disponível nos pacotes individuais.
- Prévia do teclado inspecionada visualmente, sem cortes de texto ou sobreposição
  dos controles na resolução lógica de 1120 × 820.

## Como repetir

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
.\.venv\Scripts\python.exe scripts/prepare_model.py
.\.venv\Scripts\python.exe scripts/package_workshop.py
```

Os testes usam SDL em modo simulado. Para confirmar a experiência física, execute
o [ensaio de cada estação](LAB_SETUP.md#ensaio-de-cada-estação) no Windows do laboratório,
com webcam, iluminação, fones e conta de usuário que serão usados no evento.

Os ZIPs atuais contêm código, modelo, sons e documentação. As dependências são
instaladas na preparação. Para uma instalação inteiramente offline, gere a pasta
`wheelhouse` em Windows e refaça os pacotes com `--include-wheels`, conforme o guia.

