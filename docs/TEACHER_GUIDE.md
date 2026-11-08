# Guia do professor

## Seu ensaio antes de ensinar

Reserve um ensaio para fazer o percurso inteiro:

1. Execute a referência com mouse, conheça F1–F4 e experimente B e V.
2. Leia `versions/day1/project.py` e explique cada chave do primeiro pad em voz alta.
3. Abra o starter e complete as duas funções sem copiar a resposta.
4. Adicione os três pads restantes e teste os cinco casos da missão 6 do caderno.
5. Transforme os quatro pads em cinco teclas trocando somente os dados.
6. Leia o mapa do código e execute os testes.
7. Repita a demonstração com a webcam real no Espaço Maker.

Você estará pronto para conduzir o núcleo da aula quando conseguir responder:
“Como escolhemos a região?”, “Por que segurar não repete?” e “Como trocamos o
instrumento sem reescrever a câmera?”.

## Abertura: faça o resultado aparecer primeiro

Use os mesmos nomes em português do código ao explicar as atividades: `areas`,
`encontrar_area`, `escolher_som` e `pinca_iniciada`. O [glossário](GLOSSARY.md)
relaciona esses nomes ao vocabulário em inglês e às palavras reservadas do Python.

Nos primeiros dez minutos, apresente a referência já funcionando. Toque uma
sequência curta na bateria e depois algumas notas no teclado. Convide alguém a
experimentar. Mostre a mão, o cursor, a região selecionada e o som.

Uma introdução possível:

> A câmera fornece imagens. Um modelo estima pontos da mão. Hoje vamos programar
> o que fazer com esses pontos: escolher uma região e transformá-la em som.

Use a primeira noite para garantir uma conquista compartilhada. A personalização
e as extensões vêm depois de um acionamento funcionar de ponta a ponta.

## Condução da primeira noite

Siga os horários do `WORKSHOP_PLAN.md` e as missões do caderno. Alterne explicação
curta, previsão da dupla e experiência prática. Verifique uma entrega visível a
cada bloco, evitando uma apresentação longa antes do primeiro código.

### 1. Executar e personalizar

Distribua apenas o pacote starter. O arquivo editado é
`versions/starter/project.py`. Comece com título, nome e cor para todos obterem
uma mudança visível. A tecla `1` confirma que o áudio está funcionando mesmo
antes de completar o reconhecimento de região.

Explique apenas a sintaxe que será usada: variável, função, lista, dicionário,
condição, repetição e `return`. Não é necessário dar uma aula completa sobre cada
assunto antes de usar o programa.

### 2. Coordenadas e seleção

Mostre `retangulo = (0.28, 0.28, 0.44, 0.48)` do starter. Peça que prevejam a borda
direita: `0.72`. Depois mova o pad e compare. Explique que `largura` é uma medida
horizontal; a coordenada da borda direita é `esquerda + largura`.

Resposta de referência para `encontrar_area`:

```python
def encontrar_area(areas, x, y):
    for area in areas:
        esquerda, topo, largura, altura = area["retangulo"]
        if esquerda <= x < esquerda + largura and topo <= y < topo + altura:
            return area
    return None
```

Perguntas para a dupla: por que usamos `and`? O que aconteceria se `return None`
ficasse dentro do `for`? Qual pad ganha se dois retângulos se sobrepuserem?

Resultado esperado: destacar a região sem precisar tocar. Isso separa dois
problemas que poderão ser depurados individualmente: seleção e acionamento.

### 3. Primeiro som

Resposta de referência:

```python
def escolher_som(area, pinca_iniciada):
    if area is not None and pinca_iniciada:
        return area["som"]
    return None
```

Primeiro mostre a saída lógica: nome de um arquivo ou `None`. Depois explique que
o runtime usa essa resposta para tocar e desenhar a animação.

Deixe claro que `pinca_iniciada` significa **começou uma nova pinça autorizada**,
não “os dedos estão fechados”. A robustez desse evento já vem preparada para que
a primeira experiência não seja uma rajada de sons.

### 4. Do primeiro pad ao painel

Peça três dicionários adicionais: caixa, chimbal e palma. Os alunos devem decidir
posição e cor. Garanta que os IDs sejam únicos e que as regiões não se sobreponham.
O conjunto completo de recuperação está em `versions/day1/project.py`.

Não substitua imediatamente o trabalho de uma dupla pelo checkpoint. Primeiro
identifique se o problema está nos dados, na seleção ou no acionamento. Quando
usar a recuperação, salve o trabalho anterior e peça uma personalização e uma
explicação da solução.

### 5. Estado: o que a máquina precisa lembrar?

Use uma pessoa como “programa” e outra como “mão”. Faça a primeira dizer “tocou”
a cada instante em que vê os dedos fechados. Depois mude a regra: somente após
ver abertura, pode aceitar um fechamento. Essa autorização é um estado.

Abra `workshop/gestures.py` e procure `armed`:

```python
if ratio >= self.open_threshold:
    self.armed = True
# ...
if self.armed:
    self.armed = False
    # emitir evento uma única vez
```

Esse é um trecho explicativo; a implementação completa também cuida dos limiares,
do intervalo mínimo e da perda da mão. Evite reescrever o módulo inteiro com a
turma. Use os casos da missão 6 para mostrar por que essas regras existem.

Para a pergunta “Por que dois limites?”, simule medidas próximas de `0.35`: a
pinça fecha nesse valor, mas só uma abertura acima de `0.60` autoriza outra. A
faixa intermediária ajuda a preservar a decisão anterior.

## Condução da segunda noite

Comece executando a base salva ou o checkpoint. Cada dupla escolhe uma trilha e
escreve uma mudança de comportamento que quer demonstrar. Não é necessário
implementar todos os instrumentos.

### Evolução A — teclado, apenas alterando dados

Continue no arquivo da dupla. Troque a lista de pads por cinco teclas. Um exemplo
de primeira tecla:

```python
{"id": "C4", "rotulo": "DÓ", "som": "C4.wav",
 "retangulo": (0.075, 0.25, 0.155, 0.62), "cor": (55, 220, 190)}
```

Para as próximas, avance X em `0.172` e use `D4`, `E4`, `G4`, `A4`. As funções
`encontrar_area` e `escolher_som` permanecem iguais. O programa pode continuar sendo
executado com `--version starter` ou `--version day1`: o nome da versão seleciona
o arquivo; o layout vem dos dados que a dupla editou.

Primeiro escreva as cinco teclas explicitamente. Para quem já domina repetição,
mostre como `versions/instructor/project.py` gera esses dados com `enumerate`.

Aprendizado: separar dados e comportamento permite transformar o instrumento
sem reescrever seleção, reconhecimento ou áudio.

### Evolução B — bateria e efeitos

A bateria da referência coloca os quatro pads em uma fileira. A disposição deixa
uma área livre acima de todas as bordas, útil para o gesto de descida posterior.
Comece mantendo pinça como acionamento.

O painel de efeitos é outra mudança de dados: mantenha as regiões e troque
arquivos, cores e nomes. Peça uma pequena cena sonora para dar propósito à seleção
de efeitos. Imagens são opcionais; o desenho padrão já fornece resposta visual.

### Evolução C — volume pela altura

Para esse desafio, distribua ou abra a referência instructor e compare com o
arquivo da dupla. As opções de extensão do aplicativo são disponibilizadas nessa
versão. Não basta acrescentar `--height-volume` a uma versão starter/day1.

```powershell
.\.venv\Scripts\python.exe app.py --version instructor --instrument keyboard --height-volume
```

Estude `volume_pela_altura`:

```python
def volume_pela_altura(y):
    return max(0.2, min(1.0, 1.0 - y))
```

Previsões: Y `0.2` dá volume `0.8`; Y `0.8` dá pelo menos `0.2`. O volume é
definido no ataque de cada nota. No `runtime.py`, procure `volume_pela_altura`
e mostre onde o resultado chega a `audio.play(som, volume)`.

Desafio: inverter a direção e explicar a fórmula. Outra possibilidade é estabelecer
três faixas discretas de volume usando `if`/`elif`.

### Evolução D — batida descendente

Use somente depois de concluir a bateria por pinça:

```powershell
.\.venv\Scripts\python.exe app.py --version instructor --instrument drums --strike
```

Ensine primeiro com mouse. Levante acima da borda e desça: uma batida. Mantenha
dentro: nenhuma repetição. Suba um pouco sem ultrapassar a margem: ainda não
rearmou. Suba acima da margem e desça novamente: outra batida.

Abra `StrikeGate.update` no módulo de gestos. Os passos são:

1. Guardar posição e horário anteriores.
2. Verificar se Y atravessou a borda superior descendo.
3. Calcular velocidade: `(y - old_y) / elapsed`.
4. Confirmar que a trajetória cruzou a largura do pad e que ele estava rearmado.
5. Emitir um evento e exigir subida antes de aceitar outro.

O conjunto de pads rearmados é um `set`: cada pad tem sua autorização. Uma nova
mão aparecendo dentro do pad não tem trajetória anterior e não deve bater.

Desafio: modificar um parâmetro por vez (`min_speed`, `margin` ou `cooldown`)
e explicar os efeitos observados. Não comece ajustando todos simultaneamente.

## Diferenciação por experiência

| Situação | Próxima tarefa |
| --- | --- |
| Esqueceu a sintaxe | Fazer previsões e implementar as duas funções com apoio e lembretes do caderno |
| Entregou o painel básico | Alterar dados e produzir um instrumento próprio |
| Já programa com facilidade | Explicar uma regra, experimentar uma extensão e verificar os casos de perda/rearme |
| Dupla bloqueada por ambiente | Continuar com mouse/teclado e recuperar o checkpoint sem perder o trabalho |

Não atribua apenas a edição de cores a quem tem menos experiência: todos devem
participar de pelo menos uma condição que muda comportamento. Quem já programa
pode ajudar a formular a explicação, sem tomar o teclado durante toda a atividade.

## Depuração guiada

Pergunte nesta ordem:

1. A imagem/cursor está disponível?
2. O pad é selecionado visualmente?
3. O gesto está rearmado após abertura?
4. A função devolve o arquivo correto?
5. O som funciona pela tecla numérica?

Um `print(x, y)` temporário pode ajudar nas coordenadas; explique que centenas de
mensagens por segundo deixam o terminal confuso e remova-o depois de resolver.
Um som não tocar no starter pode ser uma tarefa pendente, não um problema da webcam.

## Encerramento

Nas apresentações, cada dupla faz uma demonstração e explica uma regra em até
90 segundos. As dez duplas usam aproximadamente 15 minutos, deixando dez para
transições e pequenos imprevistos dentro do bloco de 25 minutos.

Reserve os últimos 20 minutos para a equipe apresentar o curso e esclarecer as
informações de matrícula. Conforme orientação da organização, eventual dispensa
de componentes é condicionada à análise institucional e precisa ser solicitada
antes da matrícula.

Faça a ponte com o curso a partir do que acabaram de construir: variáveis e
condições controlaram ações, funções separaram responsabilidades, dados permitiram
novos instrumentos e testes ajudaram a explicar problemas reais.

