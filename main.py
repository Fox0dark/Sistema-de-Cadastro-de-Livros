"""
Atividade N3 - Estrutura de Dados e Organização de Arquivos
Sistema de Cadastro de Livros

Funcionalidades:
  1. Incluir, alterar e excluir registros
  2. Persistência em arquivo JSON
  3. Pesquisa por campos de texto (título, autor, gênero)
  4. Listagens ordenadas por 2 campos diferentes (título e ano)
"""

import json
import os

ARQUIVO = "livros.json"


# ---------------------------------------------------------------
# Persistência (JSON)
# ---------------------------------------------------------------
def carregar():
    """Lê a lista de livros do arquivo JSON. Se não existir, retorna lista vazia."""
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível ler o arquivo. Iniciando lista vazia.")
        return []


def salvar(livros):
    """Grava a lista de livros no arquivo JSON."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(livros, f, ensure_ascii=False, indent=4)


# ---------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------
def proximo_id(livros):
    """Gera o próximo código único (maior id existente + 1)."""
    if not livros:
        return 1
    return max(l["id"] for l in livros) + 1


def buscar_por_id(livros, id_livro):
    """Retorna o livro com o id informado, ou None."""
    for livro in livros:
        if livro["id"] == id_livro:
            return livro
    return None


def ler_inteiro(mensagem, permitir_vazio=False):
    """Lê um número inteiro do teclado, repetindo até ser válido."""
    while True:
        texto = input(mensagem).strip()
        if permitir_vazio and texto == "":
            return None
        try:
            return int(texto)
        except ValueError:
            print("Valor inválido. Digite um número inteiro.")


def ler_texto(mensagem):
    """Lê um texto não vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Este campo não pode ficar vazio.")


def imprimir(livros):
    """Imprime uma lista de livros em formato de tabela."""
    if not livros:
        print("\nNenhum registro encontrado.")
        return
    print()
    print(f"{'ID':<4} {'Título':<30} {'Autor':<22} {'Ano':<6} {'Gênero':<15}")
    print("-" * 80)
    for l in livros:
        print(f"{l['id']:<4} {l['titulo'][:29]:<30} {l['autor'][:21]:<22} "
              f"{l['ano']:<6} {l['genero'][:14]:<15}")
    print(f"\nTotal: {len(livros)} registro(s)")


# ---------------------------------------------------------------
# CRUD
# ---------------------------------------------------------------
def incluir(livros):
    print("\n--- Incluir livro ---")
    livro = {
        "id": proximo_id(livros),
        "titulo": ler_texto("Título: "),
        "autor": ler_texto("Autor: "),
        "ano": ler_inteiro("Ano de publicação: "),
        "genero": ler_texto("Gênero: "),
    }
    livros.append(livro)
    salvar(livros)
    print(f"Livro incluído com sucesso (ID {livro['id']}).")


def alterar(livros):
    print("\n--- Alterar livro ---")
    livro = buscar_por_id(livros, ler_inteiro("ID do livro: "))
    if livro is None:
        print("Livro não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")
    novo = input(f"Título [{livro['titulo']}]: ").strip()
    if novo:
        livro["titulo"] = novo
    novo = input(f"Autor [{livro['autor']}]: ").strip()
    if novo:
        livro["autor"] = novo
    novo = ler_inteiro(f"Ano [{livro['ano']}]: ", permitir_vazio=True)
    if novo is not None:
        livro["ano"] = novo
    novo = input(f"Gênero [{livro['genero']}]: ").strip()
    if novo:
        livro["genero"] = novo

    salvar(livros)
    print("Livro alterado com sucesso.")


def excluir(livros):
    print("\n--- Excluir livro ---")
    livro = buscar_por_id(livros, ler_inteiro("ID do livro: "))
    if livro is None:
        print("Livro não encontrado.")
        return

    confirma = input(f"Excluir '{livro['titulo']}'? (s/n): ").strip().lower()
    if confirma == "s":
        livros.remove(livro)
        salvar(livros)
        print("Livro excluído com sucesso.")
    else:
        print("Exclusão cancelada.")


# ---------------------------------------------------------------
# Pesquisa por campo de texto
# ---------------------------------------------------------------
def pesquisar(livros):
    print("\n--- Pesquisar ---")
    print("1 - Título\n2 - Autor\n3 - Gênero")
    opcao = input("Pesquisar por: ").strip()
    campos = {"1": "titulo", "2": "autor", "3": "genero"}
    if opcao not in campos:
        print("Opção inválida.")
        return

    campo = campos[opcao]
    termo = ler_texto("Texto a buscar: ").lower()
    # Busca parcial, sem diferenciar maiúsculas de minúsculas
    resultado = [l for l in livros if termo in l[campo].lower()]
    imprimir(resultado)


# ---------------------------------------------------------------
# Ordenação (Insertion Sort implementado manualmente)
# ---------------------------------------------------------------
def ordenar(livros, campo):
    """
    Retorna uma NOVA lista ordenada pelo campo informado,
    usando o algoritmo Insertion Sort (estável).
    Textos são comparados sem diferenciar maiúsculas/minúsculas.
    """
    def chave(livro):
        valor = livro[campo]
        return valor.lower() if isinstance(valor, str) else valor

    lista = livros[:]
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0 and chave(lista[j]) > chave(atual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = atual
    return lista


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------
def menu():
    print("\n===== CADASTRO DE LIVROS =====")
    print("1 - Incluir")
    print("2 - Alterar")
    print("3 - Excluir")
    print("4 - Pesquisar (título / autor / gênero)")
    print("5 - Listar ordenado por TÍTULO")
    print("6 - Listar ordenado por ANO")
    print("7 - Listar todos (ordem de cadastro)")
    print("0 - Sair")
    return input("Escolha: ").strip()


def main():
    livros = carregar()
    while True:
        opcao = menu()
        if opcao == "1":
            incluir(livros)
        elif opcao == "2":
            alterar(livros)
        elif opcao == "3":
            excluir(livros)
        elif opcao == "4":
            pesquisar(livros)
        elif opcao == "5":
            imprimir(ordenar(livros, "titulo"))
        elif opcao == "6":
            imprimir(ordenar(livros, "ano"))
        elif opcao == "7":
            imprimir(livros)
        elif opcao == "0":
            print("Encerrando. Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
