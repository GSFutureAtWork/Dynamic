import statistics
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from core.dp import (
    longest_common_subsequence_iter,
    longest_common_substring_iter,
    levenshtein_distance_iter,
)

# Prompts usados para gerar respostas das LLMs. Cada prompt tem um arquivo de resposta para cada LLM na pasta data/llms/{llm}/p{num_prompt}.txt
prompts = {
    "Fatuais": [
        "Qual o rio mais longo do mundo?",
        "Quem foi a primeira pessoa a pisar na Lua?",
    ],
    "Criativos": [
        "Escreva um poema curto (quatro linhas) sobre uma xícara de café.",
        "Descreva uma cidade futurista em um único parágrafo.",
    ],
    "Código": [
        "Escreva uma função em Python que inverte uma string.",
        "Escreva a estrutura básica de um arquivo HTML5 (apenas as tags head e body).",
    ],
    "Explicações Simples": [
        "O que é um 'hash map' (ou dicionário) em programação? Explique de forma simples.",
        "Explique o que é a fotossíntese para uma criança de 10 anos.",
    ],
    "Opiniões": [
        "Qual é melhor: iOS ou Android? Liste uma vantagem de cada.",
        "O trabalho remoto é o futuro do trabalho? Justifique brevemente.",
    ],
}


def ler_arquivo(path):
    """Lê o conteúdo de um arquivo com tratamento de erro."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read(100)
    except FileNotFoundError:
        rprint(
            f"[bold red]ERRO: Arquivo não encontrado:[/bold red] [yellow]{path}[/yellow]",
            file=sys.stderr,
        )
        return None
    except Exception as e:
        rprint(f"[bold red]ERRO ao ler {path}:[/bold red] {e}", file=sys.stderr)
        return None


def calcular_distancias(
    llms, num_prompts, ler_arquivo_func, algorithm=levenshtein_distance_iter
):
    """Calcula as distâncias de Levenshtein entre pares de LLMs para cada prompt."""
    pares = [
        (llms[0], llms[1]),
        (llms[0], llms[2]),
        (llms[1], llms[2]),
    ]
    all_distances = {f"{l1}-{l2}": [] for l1, l2 in pares}
    resultados = []

    for i in range(1, num_prompts + 1):
        conteudos = {}
        llms_ok = True

        for llm in llms:
            filename = f"p{i}.txt"
            filepath = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "llms",
                llm,
                filename,
            )
            conteudos[llm] = ler_arquivo_func(filepath)

            if conteudos[llm] is None:
                llms_ok = False
                break

        if not llms_ok:
            resultados.append((i, None))
            continue

        distancias = {}
        for l1, l2 in pares:
            dist = algorithm(conteudos[l1], conteudos[l2])
            chave = f"{l1}-{l2}"
            all_distances[chave].append(dist)
            distancias[chave] = dist

        resultados.append((i, distancias))

    return pares, all_distances, resultados


def exibir_tabela_distancias(pares, resultados, algorithm=levenshtein_distance_iter):
    """Exibe a tabela de distâncias para cada prompt, usando o algoritmo especificado."""
    if algorithm == levenshtein_distance_iter:
        title = "Distâncias de Levenshtein (Primeiros 100 chars)"
    elif algorithm == longest_common_subsequence_iter:
        title = "Subsequência Comum Mais Longa (Primeiros 100 chars)"
    elif algorithm == longest_common_substring_iter:
        title = "Substring Comum Mais Longa (Primeiros 100 chars)"
    else:
        title = "Comparação de Respostas (Primeiros 100 chars)"

    table = Table(title=title, show_lines=True)
    table.add_column("Prompt", style="cyan", justify="center")
    for l1, l2 in pares:
        table.add_column(
            f"{l1.upper()} vs {l2.upper()}", justify="center", style="magenta"
        )

    for i, distancias in resultados:
        if distancias is None:
            table.add_row(
                f"P{i}",
                Text("ERRO DE ARQUIVO", style="bold red", justify="center"),
                *([""] * (len(pares) - 1)),
            )
        else:
            row_data = [f"P{i}"]
            for l1, l2 in pares:
                chave = f"{l1}-{l2}"
                row_data.append(f"{distancias[chave]}")
            table.add_row(*row_data)
    return table


def exibir_tabela_medias(all_distances):
    """Exibe a tabela de médias e medianas das distâncias."""
    avg_table = Table(show_header=True, show_lines=True, padding=(0, 2))
    avg_table.add_column("Comparação", style="cyan")
    avg_table.add_column("Média da Distância", justify="right", style="yellow")
    avg_table.add_column("Mediana da Distância", justify="right", style="yellow")

    for chave, distancias in all_distances.items():
        l1, l2 = chave.split("-")
        if distancias:
            media = sum(distancias) / len(distancias)
            mediana = statistics.median(distancias)
            avg_table.add_row(
                f"{l1.capitalize()} vs {l2.capitalize()}",
                f"{media:.2f}",
                f"{mediana:.2f}",
            )
        else:
            avg_table.add_row(
                f"{l1.capitalize()} vs {l2.capitalize()}",
                "[bold red]N/A (nenhum dado)[/bold red]",
                "",
            )
    return avg_table


def show_llm_prompts():
    rprint("\n[bold blue]Prompts utilizados:[/bold blue]\n")
    for categoria, lista_prompts in prompts.items():
        rprint(f"[bold magenta]{categoria}:[/bold magenta]")
        for i, prompt in enumerate(lista_prompts, start=1):
            rprint(f"  [green]{i}.[/green] {prompt}")
        rprint("")  # Linha em branco entre categorias


def compare_llm_responses(algorithm=levenshtein_distance_iter):
    console = Console()
    llms = ["chatgpt", "deepseek", "gemini"]
    num_prompts = 10

    if algorithm == levenshtein_distance_iter:
        text = "\n\n[bold green]📊 Tabela de Distâncias de Levenshtein Prompt a Prompt[/bold green]\n"
    elif algorithm == longest_common_subsequence_iter:
        text = "\n\n[bold green]📊 Tabela de Subsequências Comuns Mais Longas Prompt a Prompt[/bold green]\n"
    elif algorithm == longest_common_substring_iter:
        text = "\n\n[bold green]📊 Tabela de Substrings Comuns Mais Longas Prompt a Prompt[/bold green]\n"
    else:
        text = (
            "\n\n[bold yellow]📊 Tabela de Comparação Prompt a Prompt[/bold yellow]\n"
        )

    rprint(text)

    pares, all_distances, resultados = calcular_distancias(
        llms, num_prompts, ler_arquivo, algorithm
    )
    table = exibir_tabela_distancias(pares, resultados)
    console.print(table)

    if algorithm == levenshtein_distance_iter:
        rprint("\n\n[bold green]🏆 Distâncias de Levenshtein Gerais[/bold green]\n")
    elif algorithm == longest_common_subsequence_iter:
        rprint(
            "\n\n[bold green]🏆 Subsequências Comuns Mais Longas Gerais[/bold green]\n"
        )
    elif algorithm == longest_common_substring_iter:
        rprint("\n\n[bold green]🏆 Substrings Comuns Mais Longas Gerais[/bold green]\n")

    avg_table = exibir_tabela_medias(all_distances)
    console.print(avg_table)
