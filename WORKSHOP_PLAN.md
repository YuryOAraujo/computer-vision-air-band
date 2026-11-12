# Workshop TOP de Programação — Laboratório de Música com Gestos

Plano do workshop de 12 e 13 de novembro de 2026. As versões implementadas e os
materiais de apoio estão descritos em [README.md](README.md).

## Contexto confirmado

- 20 participantes, com níveis de experiência em Python ainda desconhecidos.
- 5h50 de programação do evento no total: 175 minutos por noite, das 19h às 21h55. Os cinco minutos restantes de cada noite ficam como margem até as 22h.
- Computadores Windows, Acer Nitro V15 com GPU RTX.
- O professor fornecerá imagens e amostras de áudio.
- É necessário verificar previamente a disponibilidade e o funcionamento das webcams e da saída de áudio de cada estação.

## Proposta

**Desafio:** construir um instrumento que responde aos movimentos das mãos diante de uma webcam.

Na primeira noite, todos desenvolvem um pequeno painel de sons. Na segunda, cada dupla transforma essa base em um instrumento ou painel temático e apresenta uma demonstração curta.

A interação inicial é única e previsível: apontar para uma região e aproximar o polegar do indicador para tocar um som. Soltar os dedos permite tocar novamente. O reconhecimento de mão fica pronto no material de apoio; os participantes programam o comportamento da aplicação.

**Resultado mínimo por dupla:** uma aplicação com quatro regiões sonoras, seleção visível, acionamento por gesto, resposta visual e possibilidade de tocar novamente após soltar o gesto.

**Resultado da segunda noite:** uma aplicação personalizada, com pelo menos uma alteração de comportamento que a dupla consiga explicar.

## Escopo dos instrumentos

| Trilha | Entrega principal | Possível desafio adicional |
| --- | --- | --- |
| Bateria de pads | Quatro pads: bumbo, caixa, chimbal e palma; acionamento por pinça | Trocar a pinça por um movimento descendente que cruza a borda superior do pad |
| Teclado musical | Cinco teclas largas com notas de uma escala pentatônica, como dó, ré, mi, sol e lá | Acrescentar notas ou controlar o volume pela altura da mão |
| Efeitos de cinema ou jogos | Quatro a seis efeitos em um painel temático | Criar uma sequência guiada de efeitos ou uma pequena história sonora |

A primeira entrega de todas as trilhas usa o mesmo acionamento por pinça. A bateria com movimento de baqueta é um desafio adicional, pois exige regras de velocidade, direção e rearme diferentes.

Para quem terminar cedo, um jogo de memória sonora pode reutilizar os mesmos pads. Esse jogo não faz parte da entrega obrigatória.

## Organização das atividades

Preferir até dez duplas, conforme a quantidade de estações e webcams. Alternar quem programa e quem experimenta a cada atividade. A experiência prévia serve para distribuir desafios, sem impedir que iniciantes escrevam e expliquem código.

Cada atividade segue um ciclo curto:

1. Prever o que uma alteração fará.
2. Alterar uma pequena parte do código.
3. Executar e experimentar com as mãos.
4. Explicar o resultado à outra pessoa da dupla.

### Noite 1 — 12/11: do movimento ao primeiro painel de sons

| Horário | Atividade | Entrega observável |
| --- | --- | --- |
| 19h–19h10 | Demonstração do professor e desafio da noite | Participantes experimentam um instrumento pronto |
| 19h10–19h25 | Abrir e executar o projeto inicial | Webcam e pontos da mão aparecem na tela |
| 19h25–19h45 | Explorar coordenadas, variáveis e condições com um cursor | A dupla muda uma regra e vê o cursor interagir com uma região |
| 19h45–20h10 | Associar o início de uma pinça a um som | Primeiro som acionado por uma regra escrita pela dupla |
| 20h10–20h20 | Intervalo | — |
| 20h20–21h | Construir quatro regiões e associar os sons | Painel com quatro sons diferentes |
| 21h–21h30 | Entender estado, soltura e resposta visual | Segurar a pinça toca apenas uma vez; soltar e apertar toca novamente |
| 21h30–21h55 | Desafio criativo e salvamento | Painel personalizado e projeto salvo para a próxima noite |

A regra de acionamento único já deve existir no exemplo do primeiro som. O bloco posterior aprofunda o motivo dessa regra e permite modificá-la, sem deixar o problema de repetição atrapalhar a primeira experiência.

### Noite 2 — 13/11: transformar a base em um instrumento

| Horário | Atividade | Entrega observável |
| --- | --- | --- |
| 19h–19h15 | Retomada e execução da base da noite anterior | Todas as duplas partem de um painel funcionando |
| 19h15–19h30 | Escolher trilha, desenhar regiões e definir uma mudança de comportamento | Pequeno esboço do instrumento e tarefa da dupla |
| 19h30–20h30 | Construir o instrumento com imagens e sons fornecidos | Instrumento principal funcionando |
| 20h30–20h40 | Intervalo | — |
| 20h40–21h10 | Experimentar, corrigir e acrescentar um desafio opcional | Outra dupla consegue usar o instrumento sem instruções longas |
| 21h10–21h35 | Apresentações: cerca de 90 segundos por dupla, com margem para trocas | Demonstração e explicação de uma decisão de programação |
| 21h35–21h55 | Apresentação do curso e orientações da equipe institucional | Dúvidas sobre continuidade dos estudos e matrícula esclarecidas |

Nos dois dias, 21h55–22h fica como margem de encerramento. Os intervalos e a apresentação do curso estão incluídos nos 350 minutos planejados.

Na apresentação do curso, a equipe institucional deve reforçar a orientação informada pela organização: eventuais dispensas de componentes dependem de análise e critérios institucionais, e a solicitação deve ocorrer antes da matrícula.

## O que o professor prepara e o que os alunos programam

| Preparado pelo professor | Construído ou modificado pelos participantes |
| --- | --- |
| Abertura e encerramento da câmera | Posição, tamanho e quantidade de regiões |
| Execução do modelo de rastreamento | Associação entre regiões e sons |
| Extração dos pontos e cálculo básico da pinça | Condições que autorizam o acionamento |
| Carregamento e reprodução de áudio | Estado anterior e regra de tocar novamente |
| Funções para desenhar regiões e imagens | Cores, nomes, imagens e resposta visual |
| Tratamento de falhas de câmera e arquivos | Uma mudança de comportamento na segunda noite |

Iniciantes recebem trechos pequenos com tarefas em português e exemplos completos de sintaxe. Participantes experientes podem acrescentar uma segunda mão, controle de volume ou detecção de batida descendente, após concluir a base.

Não é necessário ensinar treinamento de modelos, orientação a objetos ou programação assíncrona para concluir o projeto. A explicação conceitual distingue o modelo, que estima pontos da mão, das regras escritas pela turma, que decidem o que esses pontos fazem.

## Direção técnica proposta

- **Python 3.8.2 de 64 bits:** aproveitar a instalação existente no laboratório, com dependências compatíveis fixadas e instalação offline por wheels; ensaiar no Windows antes da aula.
- **OpenCV:** captura da webcam, recorte e espelhamento do vídeo.
- **MediaPipe Tasks / Hand Landmarker:** estimativa dos pontos da mão a partir do modelo pré-treinado, salvo localmente.
- **Pygame:** janela, texto, desenho dos instrumentos e mixer com sons carregados no início da aplicação e reprodução sem bloquear o processamento da câmera.
- **Execução local em CPU:** sem uma etapa de configuração de CUDA no workshop.

Começar com uma mão e uma janela de vídeo. Manter câmera, desenho e reconhecimento encapsulados em funções de apoio. O trecho editado pelos alunos deve mostrar claramente a sequência: obter posição, escolher região, verificar gesto, tocar som e atualizar estado.

### Regras de interação

1. Espelhar a imagem antes de calcular e desenhar as interações, mantendo uma única convenção de coordenadas.
2. Usar coordenadas normalizadas para os layouts, com conversão para pixels nas funções de desenho.
3. Exibir um cursor e destacar a região selecionada antes do acionamento.
4. Comparar a distância entre polegar e indicador com uma medida da palma; evitar depender apenas de uma distância fixa em pixels.
5. Usar limiares diferentes para fechar e abrir a pinça, reduzindo alternâncias na borda do limiar.
6. Tocar no início do gesto, e não em todos os quadros em que ele permanece fechado. A soltura rearma o próximo acionamento.
7. Uma mão recém-detectada precisa ser vista com a pinça aberta antes de poder tocar. A perda de rastreamento não deve criar um novo acionamento.
8. Manter uma forma de acionar os sons pelo teclado físico para verificar áudio e continuar uma atividade enquanto se resolve um problema de câmera.

Um pequeno intervalo mínimo entre acionamentos pode complementar essas regras. Ele não substitui o reconhecimento de soltura e rearme.

Na extensão de bateria por movimento, exigir descida através da borda de acionamento e retorno acima dela antes da próxima batida. Apenas permanecer dentro do pad não deve gerar uma sequência de sons.

### Organização sugerida do código

```text
app.py                  # Entrada e opções de execução
versions/*/project.py   # Regiões, sons e regras modificadas pelos alunos
workshop/runtime.py     # Laço principal e integração
workshop/tracking.py    # Câmera, pontos e apoio para gestos
workshop/gestures.py    # Estado da pinça e batidas descendentes
workshop/audio.py       # Carregamento e reprodução dos sons
workshop/drawing.py     # Cursor, regiões, imagens e feedback visual
assets/sounds/          # Amostras fornecidas pelo professor
assets/images/          # Imagens fornecidas pelo professor
models/                 # Modelo local de detecção das mãos
```

Evitar criar sistemas de plugins, telas de configuração ou abstrações adicionais antes de validar uma interação completa.

## Materiais a preparar

- Um projeto inicial que já abre a câmera e desenha os pontos da mão.
- Uma versão de recuperação com o painel da primeira noite concluído.
- Uma versão de referência para o professor, com os instrumentos funcionando.
- Um roteiro curto em português, organizado por pequenos desafios e resultados esperados.
- Quatro amostras de bateria, cinco notas musicais e, opcionalmente, um conjunto de efeitos.
- Áudios WAV PCM de 16 bits, preferencialmente com a mesma taxa de amostragem e quantidade de canais. Cortar silêncio no início e equilibrar volumes antes do evento.
- Imagens PNG com transparência, já dimensionadas ou processadas pelas funções de apoio.
- Modelo e dependências disponíveis localmente antes da aula; o caminho principal da atividade não deve depender de downloads durante o evento.
- Fones para as duplas; caixas de som para as demonstrações coletivas.

## Verificação antes do evento

Executar a referência completa em um computador do laboratório e depois verificar cada estação:

- Abrir a câmera com a conta de usuário que será utilizada na aula.
- Rastrear uma mão e tocar sons usando a iluminação e a posição previstas no Espaço Maker.
- Confirmar que segurar uma pinça gera apenas um acionamento e que soltá-la permite outro.
- Retirar a mão e recolocá-la com os dedos fechados: o som deve aguardar a abertura e uma nova pinça.
- Passar por regiões sem fazer a pinça: não deve haver som.
- Executar dois sons em sequência rápida e verificar resposta e sobreposição.
- Abrir o projeto inicial e a versão de recuperação usando apenas as instruções entregues aos alunos.
- Executar sem acesso à internet, com todos os arquivos necessários já disponíveis.

Essa verificação determina as versões fixadas das dependências e os ajustes de câmera e áudio. A disponibilidade da GPU não substitui esse ensaio.

## Critério de sucesso do workshop

Cada dupla termina com um programa que consegue executar, demonstrar e explicar. Durante a apresentação, deve apontar ao menos uma regra que escreveu e uma alteração que mudou o comportamento do instrumento.

O foco é proporcionar autoria e uma experiência musical divertida. Gravação de faixas, edição de áudio, sincronização precisa de ritmo e treinamento de modelos ficam fora da entrega principal.

## Referências técnicas consultadas

- [MediaPipe Hand Landmarker](https://developers.google.com/edge/mediapipe/solutions/vision/hand_landmarker?tab=Python)
- [Configuração do MediaPipe Tasks em Python](https://developers.google.com/edge/mediapipe/solutions/setup_python)
- [Pygame mixer](https://www.pygame.org/docs/ref/mixer.html)
