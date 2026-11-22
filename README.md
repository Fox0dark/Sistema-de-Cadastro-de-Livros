# Cadastro de Livros — Atividade N3

**Disciplina:** Estrutura de Dados e Organização de Arquivos
**Aluno(a):** _(Mikael Cenedese Arévalo)_
**Linguagem:** Python 

## 1. Descrição

Sistema de cadastro de livros executado no terminal. Permite incluir, alterar e
excluir registros, pesquisar por campos de texto e imprimir listas ordenadas.
Os dados são salvos em um arquivo JSON, então continuam disponíveis quando o
programa é fechado e aberto novamente.

## 2. Requisitos atendidos

| Requisito da atividade | Como foi atendido |
|---|---|
| Incluir, alterar, excluir | Funções `incluir()`, `alterar()` e `excluir()` |
| Persistência em JSON | Funções `carregar()` e `salvar()` usando o módulo `json` (arquivo `livros.json`) |
| Pesquisa por campos de texto | Função `pesquisar()`: busca parcial por **título**, **autor** ou **gênero**, sem diferenciar maiúsculas de minúsculas |
| Listas ordenadas por 2 campos | Opção 5 ordena por **título** (texto) e opção 6 ordena por **ano** (numérico) |

## 3. Como executar


```bash
git clone <link-do-repositorio>
cd <pasta-do-repositorio>
python main.py
```

Na primeira execução o arquivo `livros.json` é criado automaticamente quando o
primeiro livro é cadastrado.

## 4. Estrutura do projeto

```
.
├── main.py        # código-fonte do sistema
├── livros.json    # base de dados (gerada pelo programa)
└── README.md      # documentação
```

## 5. Estrutura dos dados

Cada livro é um dicionário e a base é uma lista de dicionários, gravada em JSON:

```json
[
    {
        "id": 1,
        "titulo": "Dom Casmurro",
        "autor": "Machado de Assis",
        "ano": 1899,
        "genero": "Romance"
    }
]
```

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | inteiro | Código único gerado automaticamente (maior id + 1) |
| `titulo` | texto | Título do livro |
| `autor` | texto | Nome do autor |
| `ano` | inteiro | Ano de publicação |
| `genero` | texto | Gênero literário |

## 6. Funcionamento

### Menu principal

```
1 - Incluir
2 - Alterar
3 - Excluir
4 - Pesquisar (título / autor / gênero)
5 - Listar ordenado por TÍTULO
6 - Listar ordenado por ANO
7 - Listar todos (ordem de cadastro)
0 - Sair
```

### Principais funções

- **`carregar()`**: lê o `livros.json` ao iniciar. Se o arquivo não existir ou estiver corrompido, começa com uma lista vazia.
- **`salvar(livros)`**: grava a lista no arquivo com `ensure_ascii=False` (preserva acentos) e `indent=4` (arquivo legível). É chamada após cada inclusão, alteração ou exclusão.
- **`incluir(livros)`**: lê os campos, gera o `id` e adiciona o livro à lista.
- **`alterar(livros)`**: localiza o livro pelo `id`; campos deixados em branco mantêm o valor atual.
- **`excluir(livros)`**: localiza o livro pelo `id` e remove após confirmação do usuário.
- **`pesquisar(livros)`**: o usuário escolhe o campo de texto e digita o termo. Retorna todos os livros cujo campo contém o termo.
- **`ordenar(livros, campo)`**: implementa o algoritmo **Insertion Sort** e devolve uma nova lista ordenada, sem alterar a ordem original salva no arquivo.
- **`imprimir(livros)`**: exibe a lista em formato de tabela.

### Algoritmo de ordenação

Foi usado o **Insertion Sort**, que percorre a lista e insere cada elemento na
posição correta dentro da parte já ordenada. Ele é estável (registros com valores
iguais mantêm a ordem relativa) e tem complexidade O(n²) no pior caso, o que é
adequado para o volume de dados do sistema. Para textos, a comparação ignora
maiúsculas e minúsculas, então "abacaxi" e "Zebra" ficam na ordem alfabética correta.

### Validações

- Campos de texto obrigatórios não aceitam valor vazio.
- O ano deve ser um número inteiro.
- Exclusão exige confirmação.
- Buscas por `id` inexistente mostram mensagem de erro, sem interromper o programa.

## 7. Exemplo de uso

```
===== CADASTRO DE LIVROS =====
Escolha: 1

--- Incluir livro ---
Título: Dom Casmurro
Autor: Machado de Assis
Ano de publicação: 1899
Gênero: Romance
Livro incluído com sucesso (ID 1).
```

Listagem por título:

```
ID   Título                         Autor                  Ano    Gênero
--------------------------------------------------------------------------------
2    A Hora da Estrela              Clarice Lispector      1977   Romance
1    Dom Casmurro                   Machado de Assis       1899   Romance

Total: 2 registro(s)
```
