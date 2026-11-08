# Air Band Lab

Workshop TOP de Programação: um instrumento musical controlado por gestos.
Material em português para 12 e 13/11/2026; duração total planejada de 5h50.

## Primeiro ensaio no Windows

1. Instale **Python 3.12 de 64 bits**, com o Python Launcher (`py`).
2. Extraia ou copie o projeto para uma pasta local. Execute `preparar_windows.bat` antes da aula.
3. Abra um terminal nessa pasta e execute a demonstração:

```powershell
.\.venv\Scripts\python.exe app.py --version instructor --input mouse
```

Mova o mouse sobre um pad, solte o botão e clique para tocar. As teclas `1` a `5`
também testam os sons. Para usar a webcam:

```powershell
.\.venv\Scripts\python.exe app.py --version instructor --input camera
```

Aponte o indicador para um pad. Abra polegar e indicador e aproxime-os para tocar.
Segurar os dedos fechados toca uma única vez. Abra-os para tocar novamente.

Com o ambiente virtual ativo, `python app.py` abre a versão starter. Para a
demonstração completa, escolha `python app.py --version instructor`. Nos pacotes
que contêm somente uma versão, essa é selecionada automaticamente.

Também é possível usar `iniciar_windows.bat starter camera`,
`iniciar_windows.bat day1 mouse` ou `iniciar_windows.bat instructor camera`.

## As três versões

| Versão | Comando após `app.py` | O que editar |
| --- | --- | --- |
| Início | `--version starter` | `versions/starter/project.py`: duas funções para completar, um pad |
| Final da noite 1 | `--version day1` | `versions/day1/project.py`: painel completo com quatro sons |
| Referência do professor | `--version instructor` | `versions/instructor/project.py`: painel, bateria, teclado e efeitos |

**O starter executa normalmente, mas ainda não toca por gesto.** Essa é a tarefa
da turma. O cursor, os pontos da mão, o pad e o teste de áudio pela tecla `1` já
funcionam. Não é um erro de instalação. Reinicie o programa após editar o código.

Todas as versões compartilham a pasta `workshop/`. Os pacotes gerados para alunos
contêm essa infraestrutura e apenas a versão correspondente; não dependem das
outras pastas de versões.

O código das atividades usa português: `criar_areas`, `encontrar_area`,
`escolher_som` e as chaves `rotulo`, `som`, `retangulo`, `cor` e `imagem`.
Os exemplos dos guias seguem esses nomes. Consulte o [glossário](docs/GLOSSARY.md)
para os termos de Python, nomes da infraestrutura e correspondências em inglês.

## Controles da referência

- `F1` painel; `F2` bateria; `F3` teclado; `F4` efeitos. Os botões na tela também funcionam.
- `B` alterna batidas descendentes na bateria. Levante o cursor acima da borda e desça sobre o pad.
- `V` alterna volume pela altura no teclado. Notas tocadas mais acima ficam mais fortes.
- `1`–`9` tocam diretamente os pads disponíveis, para testar som ou usar sem gestos.
- `H` mostra/esconde os pontos da mão; `R` rearma o reconhecimento; `M` silencia; `Esc` sai.
- `--mute` permite abrir sem dispositivo de áudio; nesse caso `M` não ativa o som.
- `--camera 1` seleciona outra webcam. O padrão é `0`.

Para iniciar diretamente uma extensão:

```powershell
.\.venv\Scripts\python.exe app.py --version instructor --instrument drums --strike
.\.venv\Scripts\python.exe app.py --version instructor --instrument keyboard --height-volume
```

O modo mouse usa clique para simular pinça. Na bateria por batida, apenas mova o
mouse de cima para baixo pela borda do pad; não precisa clicar.

## Material para ensinar e compreender

Leia nesta ordem:

1. [Preparação do laboratório](docs/LAB_SETUP.md): instalação, operação offline e problemas comuns.
2. [Mapa do código](docs/CODE_WALKTHROUGH.md): caminho de um quadro, dos pontos da mão até o som.
3. [Guia do professor](docs/TEACHER_GUIDE.md): roteiro, respostas, demonstrações e evolução dos instrumentos.
4. [Caderno do aluno](docs/STUDENT_GUIDE.md): missões curtas e critérios de conclusão.
5. [Plano do workshop](WORKSHOP_PLAN.md): agenda e objetivos pedagógicos.
6. [Glossário](docs/GLOSSARY.md): vocabulário do código e termos em inglês.

Os 13 sons de demonstração já estão incluídos e são gerados por código original.
Troque os WAVs em `assets/sounds/` pelos seus arquivos ou altere `som` nos pads.
Para adicionar PNGs aos instrumentos, consulte [assets/images/README.md](assets/images/README.md).

## Verificação e distribuição

```powershell
.\.venv\Scripts\python.exe -m unittest discover -v
.\.venv\Scripts\python.exe scripts/package_workshop.py
```

O primeiro comando verifica regras de gestos, layouts, áudio sobreposto, desenho
das versões e inferência real em uma imagem vazia. A janela e o áudio dos testes
usam os drivers de simulação do SDL. **Isso não substitui testar a webcam e a saída
de som reais no Windows do laboratório.**

O segundo comando cria três ZIPs em `dist/`. Para incluir as dependências Windows
previamente baixadas na pasta `wheelhouse/`, acrescente `--include-wheels`.
Entregue o ZIP starter na primeira noite e o checkpoint day1 na segunda, conforme
necessário. O ZIP instructor inclui as três versões e todo o material do professor.

## Outros ambientes

O alvo do evento é Windows com Python 3.12. Para desenvolver em Linux/macOS com
Python 3.12, crie um ambiente virtual e instale `requirements-lock.txt`, depois
execute `scripts/generate_sounds.py` e `scripts/prepare_model.py`.

`requirements.txt` registra as dependências diretas; `requirements-lock.txt` fixa
também as transitivas. O modelo local tem URL de versão fixa e verificação SHA-256.
O aplicativo não acessa a rede durante sua execução.

Consulte o [registro de validação](docs/VALIDATION.md) para os resultados e os
limites das verificações feitas neste ambiente.

