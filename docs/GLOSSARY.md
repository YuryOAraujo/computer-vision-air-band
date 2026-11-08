# Glossário de programação e do projeto

As funções, variáveis e chaves editadas nas atividades usam português. Uma **área
sonora** é uma região interativa: pode representar um pad de bateria, uma tecla ou
um efeito. No código, usamos `area` e `areas`.

Os identificadores usam nomes sem acentos, como `pinca_iniciada` e `retangulo`.
Textos exibidos, comentários e explicações usam português com acentos normalmente.

## Nomes das atividades

Esta tabela também ajuda a reconhecer exemplos anteriores em inglês. O código
atual e os roteiros usam os nomes da coluna em português.

| Inglês | Português no código | Responsabilidade |
| --- | --- | --- |
| `TITLE` | `TITULO` | Nome do projeto na janela |
| `MISSION` | `MISSAO` | Orientação exibida na janela |
| `build_pads` | `criar_areas` | Devolver a lista de regiões e seus dados |
| `find_pad` | `encontrar_area` | Selecionar a região que contém o cursor |
| `choose_sound` | `escolher_som` | Devolver o arquivo quando um gesto autoriza tocar |
| `volume_from_height` | `volume_pela_altura` | Transformar altura em volume |
| `pad` / `pads` | `area` / `areas` | Uma região ou uma lista de regiões |
| `pinch_started` | `pinca_iniciada` | Evento de uma nova pinça, em um único quadro |
| `label` | `rotulo` | Texto de uma região |
| `sound` | `som` | Nome do arquivo WAV |
| `rect` | `retangulo` | Esquerda, topo, largura e altura |
| `color` | `cor` | Três valores RGB |
| `image` | `imagem` | Nome de um PNG opcional |
| `left`, `top`, `width`, `height` | `esquerda`, `topo`, `largura`, `altura` | Medidas de um retângulo |

`id` é a abreviação de identificador. Cada área precisa de um identificador único.
Por exemplo, a área `"bumbo"` pode reproduzir `"kick.wav"`: o identificador e o nome
do arquivo são dados diferentes. Os nomes dos arquivos fornecidos permanecem os
mesmos para facilitar a substituição dos sons.

## O que continua sendo Python

Estas palavras fazem parte da linguagem e devem ser escritas como aparecem abaixo.
A tradução descreve o significado; não é uma instrução para substituir o código.

| Python | Como ler |
| --- | --- |
| `def` | Definir uma função |
| `return` | Devolver um resultado e encerrar a função |
| `for ... in ...` | Repetir para cada elemento de uma coleção |
| `if` / `elif` / `else` | Se / senão, se / senão |
| `and` / `or` / `not` | E / ou / não |
| `is not None` | Não é ausência de valor |
| `True` / `False` | Verdadeiro / falso |
| `None` | Ausência de valor; não é um texto entre aspas |
| `enumerate` | Percorrer elementos junto com seus índices |
| `zip` | Percorrer coleções em conjunto |
| `min` / `max` | Menor / maior valor |
| `print` | Mostrar uma mensagem no terminal |

Nomes definidos pelas bibliotecas também seguem sua API, como
`pygame.mixer.Sound`, `pygame.Rect` e `HandLandmarker`.

## Comandos e instrumentos

Os caminhos dos arquivos e os comandos existentes são os mesmos. O runtime
converte o nome escolhido na linha de comando para o nome recebido pela função
`criar_areas(instrumento)`:

| Opção de `--instrument` | Valor de `instrumento` no código |
| --- | --- |
| `soundboard` | `"painel"` |
| `drums` | `"bateria"` |
| `keyboard` | `"teclado"` |
| `effects` | `"efeitos"` |

Por exemplo, `--instrument keyboard` faz a referência executar
`criar_areas("teclado")`. `--version starter` escolhe o projeto inicial;
`--version day1`, a recuperação da primeira noite; e `--version instructor`,
a referência completa.

## Ao explorar a infraestrutura

Os módulos de apoio conservam alguns nomes internos em inglês. Eles fornecem
os dados usados pelas funções das atividades.

| Nome na infraestrutura | Significado |
| --- | --- |
| `PinchGate` | Regra que autoriza uma nova pinça após abertura |
| `armed` | A abertura já autorizou o próximo fechamento |
| `closed` | Condição de dedos fechados |
| `pinch_ratio` | Distância entre as pontas dos dedos dividida pela largura da palma |
| `cooldown` | Intervalo mínimo entre acionamentos |
| `StrikeGate` | Regra de batida descendente com rearme |
| `AudioBank.play` | Reproduzir um som já carregado |
| `View` | Janela e desenho da aplicação |

