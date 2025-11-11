import random
import string


def levenshtein_distance_iter(s1, s2):
    """
    Calcula a distância de Levenshtein entre duas strings de forma iterativa (bottom-up).

    Complexidade de tempo: O(m * n)
    """
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # remoção
                dp[i][j - 1] + 1,  # inserção
                dp[i - 1][j - 1] + cost,  # substituição
            )
    return dp[m][n]


def levenshtein_distance_rec(s1, s2):
    """
    Calcula a distância de Levenshtein entre duas strings usando recursão e cache manual.

    Complexidade de tempo: O(m * n)
    Complexidade de tempo sem cache: O(3^(m+n))
    """
    cache = {}

    def rec(i, j):
        if (i, j) in cache:
            return cache[(i, j)]
        if i == 0:
            result = j
        elif j == 0:
            result = i
        else:
            cost = 0 if s1[i - 1].lower() == s2[j - 1].lower() else 1
            result = min(
                rec(i - 1, j) + 1,  # remoção
                rec(i, j - 1) + 1,  # inserção
                rec(i - 1, j - 1) + cost,  # substituição
            )
        cache[(i, j)] = result
        return result

    return rec(len(s1), len(s2))


def main():
    from rich.console import Console
    from rich.table import Table
    from rich import box

    from utils.measure_time import medir_tempo
    from rich.panel import Panel

    console = Console()

    def teste_basico():
        s1 = "Augusto"
        s2 = "Arnaldo"

        # Teste Bottom-Up
        iter_distance, iter_time = medir_tempo(levenshtein_distance_iter, s1, s2)

        # Teste Top-Down
        rec_distance, rec_time = medir_tempo(levenshtein_distance_rec, s1, s2)

        table = Table(box=box.SIMPLE)
        table.add_column("Método", style="cyan", no_wrap=True)
        table.add_column("Distância", style="magenta")
        table.add_column("Tempo (ms)", style="green")

        table.add_row("Iterativo (Bottom-Up)", str(iter_distance), f"{iter_time}")
        table.add_row("Recursivo (Top-Down)", str(rec_distance), f"{rec_time}")

        panel = Panel.fit(
            table,
            title=f"Teste Básico com '{s1}' e '{s2}'",
            border_style="blue",
            subtitle=f"[bold yellow]Resultados iguais:[/] {iter_distance == rec_distance}",
        )
        console.print(panel)

    def teste_desempenho():
        random.seed(42)
        s1 = "".join(random.choices(string.ascii_letters, k=100))
        s2 = "".join(random.choices(string.ascii_letters, k=100))

        iter_distance, iter_time = medir_tempo(levenshtein_distance_iter, s1, s2)
        rec_distance, rec_time = medir_tempo(levenshtein_distance_rec, s1, s2)

        table = Table(box=box.SIMPLE)
        table.add_column("Método", style="cyan", no_wrap=True)
        table.add_column("Distância", style="magenta")
        table.add_column("Tempo (ms)", style="green")

        table.add_row("Iterativo (Bottom-Up)", str(iter_distance), f"{iter_time}")
        table.add_row("Recursivo (Top-Down)", str(rec_distance), f"{rec_time}")

        panel = Panel.fit(
            table,
            title="Teste de Desempenho com 100 caracteres",
            border_style="blue",
            subtitle=f"[bold yellow]Resultados iguais:[/] {iter_distance == rec_distance}",
        )
        console.print(panel)

    teste_basico()
    print("\n")
    teste_desempenho()


if __name__ == "__main__":
    main()
