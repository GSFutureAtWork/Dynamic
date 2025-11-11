import statistics
import sys
import os
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import print as rprint

from dp import levenshtein_distance_iter


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


def calcular_distancias(llms, num_prompts, ler_arquivo_func):
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
            dist = levenshtein_distance_iter(conteudos[l1], conteudos[l2])
            chave = f"{l1}-{l2}"
            all_distances[chave].append(dist)
            distancias[chave] = dist

        resultados.append((i, distancias))

    return pares, all_distances, resultados


def exibir_tabela_distancias(pares, resultados):
    """Exibe a tabela de distâncias de Levenshtein para cada prompt."""
    table = Table(
        title="Distâncias de Levenshtein (Primeiros 100 chars)", show_lines=True
    )
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
                "",
                "",
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


def main():
    """Análise das distâncias de Levenshtein entre respostas de diferentes LLMs."""
    console = Console()
    llms = ["chatgpt", "deepseek", "gemini"]
    num_prompts = 10

    rprint(
        "\n[bold green]📊 Tabela de Distâncias de Levenshtein Prompt a Prompt[/bold green]\n"
    )

    pares, all_distances, resultados = calcular_distancias(
        llms, num_prompts, ler_arquivo
    )
    table = exibir_tabela_distancias(pares, resultados)
    console.print(table)

    rprint("\n\n[bold green]🏆 Distância Geral (Média | Mediana)[/bold green]\n")
    rprint("Calculada como a [bold]média[/bold] das distâncias dos 10 prompts.")

    avg_table = exibir_tabela_medias(all_distances)
    console.print(avg_table)


if __name__ == "__main__":
    main()
