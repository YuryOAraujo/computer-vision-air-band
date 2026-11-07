# Seu instrumento com gestos

Você vai construir um painel de sons e transformá-lo em um instrumento.
Uma pessoa da dupla programa; a outra testa e explica o resultado. Troquem de papel
a cada missão. Reiniciem o programa depois de salvar alterações.

## Iniciar

No terminal da pasta do projeto:

```powershell
.\.venv\Scripts\python.exe app.py --version starter
```

Para experimentar com mouse, acrescente `--input mouse`. O clique simula a pinça.
A tecla `1` testa o primeiro som sem depender das suas funções.

Abra `versions/starter/project.py`. O programa já mostra câmera, cursor e um pad.
**O som por gesto ainda será programado por você.**

## Missão 1 — Dê sua identidade ao projeto

Altere `TITLE`, `label` e `color`. Os três números da cor são vermelho, verde e
azul, de `0` a `255`. Faça uma previsão antes de executar.

Conclusão: a dupla consegue apontar na tela o que mudou e no código onde mudou.

## Missão 2 — Explore as coordenadas

`rect` contém `(esquerda, topo, largura, altura)`. As medidas vão de `0` a `1`.
X cresce para a direita e Y cresce para baixo. A origem é o canto superior
esquerdo da área do vídeo, sem o cabeçalho.

No pad inicial, a borda esquerda é `0.28` e a direita é `0.28 + 0.44 = 0.72`.
O que precisa acontecer com `rect` para mover o pad à direita sem mudar seu tamanho?

Teste uma alteração de cada vez. Mantenha o retângulo dentro do vídeo.

## Missão 3 — Encontre o pad

Complete `find_pad(pads, x, y)`:

1. Percorra os pads: `for pad in pads:`.
2. Separe as medidas: `left, top, width, height = pad["rect"]`.
3. Verifique se X está entre esquerda e direita **e** Y entre topo e base.
4. Se estiver dentro, devolva o pad com `return pad`.
5. Se nenhum pad for encontrado, devolva `None` ao final da função.

Lembretes de Python:

```python
# Uma condição pode combinar duas comparações:
if minimo <= valor < maximo:
    print("Esta dentro do intervalo")

# `and` exige que duas condições sejam verdadeiras.
```

Conclusão: o pad destaca sua borda quando o cursor entra e volta ao normal quando sai.
Se só o primeiro pad funcionar mais tarde, confira onde está a indentação de
`return None`: ele deve ficar depois do `for`.

## Missão 4 — Toque um som

Complete `choose_sound(pad, pinch_started)`.

- `pad` pode ser um dicionário ou `None`.
- `pinch_started` vale `True` somente no quadro em que uma nova pinça é aceita.
- Se houver pad e uma nova pinça, devolva `pad["sound"]`.
- Nos demais casos, devolva `None`.

O nome do arquivo é suficiente: a infraestrutura reproduz o som e acende o pad.
Você não precisa abrir o arquivo de áudio dentro dessa função.

Conclusão: aponte, abra os dedos e faça a pinça. Deve tocar uma vez. Segure os
dedos fechados: não deve repetir. Abra e feche novamente: outro toque.

## Missão 5 — Crie quatro escolhas

Adicione três dicionários à lista de pads. Cada um precisa ter `id` diferente.
Experimente `snare.wav`, `hihat.wav` e `clap.wav`, além de `kick.wav`.
Planeje quatro regiões sem sobreposição. Deixe uma margem entre elas.

O programa associa automaticamente as teclas `1`, `2`, `3` e `4` à ordem dos pads.
Um dicionário tem chaves e valores; vários dicionários ficam dentro de uma lista.
Use vírgula entre os elementos e confira colchetes e chaves.

Conclusão: quatro regiões, quatro sons e quatro seleções visuais funcionando.

## Missão 6 — Teste o comportamento

Façam uma previsão e depois experimentem:

| Experimento | Resultado esperado |
| --- | --- |
| Segurar a pinça no pad | Um único som |
| Soltar e fazer outra pinça | Outro som |
| Manter a pinça e mudar de pad | Nenhum novo som até soltar e fazer outra pinça |
| Fechar fora do pad e entrar nele | Nenhum som até outra pinça |
| Retirar a mão e recolocá-la fechada | Aguardar a abertura dos dedos |

Por que o programa precisa lembrar se a mão já estava fechada? Explique à sua dupla.
Salve uma cópia do seu `project.py` antes de encerrar a primeira noite.

## Segunda noite — Escolha seu instrumento

Continue no arquivo que você construiu. Se precisar recuperar a base, o professor
fornecerá o pacote `day1`; nesse caso use `--version day1` e edite
`versions/day1/project.py`.

Escolha uma trilha e faça um esboço das regiões:

- **Bateria:** bumbo, caixa, chimbal e palma. Comece com pinça, com pads em uma fileira.
- **Teclado:** cinco teclas verticais usando `C4.wav`, `D4.wav`, `E4.wav`, `G4.wav`, `A4.wav`.
- **Efeitos:** `laser.wav`, `coin.wav`, `space.wav`, `powerup.wav` em um painel temático.

Primeiro altere os dados dos pads. Confirme que as mesmas funções continuam
selecionando regiões e tocando os novos sons. Depois escolha **uma** melhoria:
uma nova disposição, uma regra que limita uma região da tela, novas imagens ou,
com apoio do professor, volume pela altura ou batidas descendentes.

Se receber imagens, copie os PNGs para `assets/images/` e adicione
`"image": "nome.png"` ao pad. Use imagens quadradas. Reinicie após alterar os arquivos.

## Desafio para quem terminar cedo

Escreva primeiro a regra em português: o que autoriza a ação, o que bloqueia e o
que permite repetir? Depois transforme-a em condições de Python.

Possibilidades: instrumento com uma região silenciosa, uma sequência de três
efeitos para contar uma história ou intensidade pela posição vertical.

O professor possui uma referência com extensões. Entenda uma mudança antes de
copiá-la: quais dados entram, qual estado precisa ser lembrado e o que sai?

## Apresentação final — até 90 segundos

1. Apresente o nome do instrumento e faça uma pequena demonstração.
2. Mostre uma regra que a dupla escreveu e explique seu efeito.
3. Conte uma ideia que gostaria de desenvolver com mais tempo.

Concluído: outra dupla consegue usar seu instrumento e vocês conseguem explicar
por que ele responde daquele jeito.

