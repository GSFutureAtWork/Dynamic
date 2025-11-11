def insertion_sort(data):
    """
    Ordena uma lista de números usando o algoritmo Insertion Sort.
    Retorna uma nova lista ordenada.

    Complexidade de Tempo: O(n²) no pior caso e caso médio, O(n) no melhor caso.
    Complexidade de Espaço: O(1) pois pode ser feito in-place na lista original, O(n) se criar uma cópia (Que é o caso atual).
    """
    sorted_data = data[:]

    for i in range(1, len(sorted_data)):
        current_value = sorted_data[i]
        position = i - 1

        while position >= 0 and current_value < sorted_data[position]:
            sorted_data[position + 1] = sorted_data[position]
            position -= 1

        sorted_data[position + 1] = current_value

    return sorted_data


def merge_sort(data):
    """
    Ordena uma lista de números usando o algoritmo Merge Sort.
    Retorna uma nova lista ordenada.

    Complexidade de Tempo: O(n log n)
    Complexidade de Espaço: O(n)
    """
    if len(data) <= 1:
        return data[:]

    mid = len(data) // 2
    left_sorted = merge_sort(data[:mid])
    right_sorted = merge_sort(data[mid:])

    merged_list = []
    left_idx = right_idx = 0

    while left_idx < len(left_sorted) and right_idx < len(right_sorted):
        if left_sorted[left_idx] < right_sorted[right_idx]:
            merged_list.append(left_sorted[left_idx])
            left_idx += 1
        else:
            merged_list.append(right_sorted[right_idx])
            right_idx += 1

    merged_list.extend(left_sorted[left_idx:])
    merged_list.extend(right_sorted[right_idx:])
    return merged_list


def main():
    # import random
    import math
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    from utils.measure_time import medir_tempo

    # ------------------------------- Configuração ------------------------------- #
    N_ITEMS = 100
    console = Console()

    console.print(
        f"\n[yellow]Gerando uma lista REVERSA de {N_ITEMS} elementos (pior caso para o Insertion Sort)...[/yellow]"
    )
    data_to_sort = list(range(N_ITEMS, 0, -1))
    # data_to_sort = [random.randint(0, 5000) for _ in range(N_ITEMS)] # Caso médio

    console.print("\nExecutando [bold red]Insertion Sort (O(n²))...[/]")
    _, time_insert = medir_tempo(insertion_sort, data_to_sort)
    console.print(f"Tempo de execução: [bold red]{time_insert} ms[/]")

    console.print("\nExecutando [bold green]Merge Sort (O(n log n))...[/]")
    result_merge, time_merge = medir_tempo(merge_sort, data_to_sort)
    console.print(f"Tempo de execução: [bold green]{time_merge} ms[/]")

    table = Table(title="\n\nAnálise de Complexidade (Big O)", show_lines=True)
    table.add_column(
        "Algoritmo",
        style="cyan",
    )
    table.add_column("Complexidade (Pior Caso)", style="magenta")
    table.add_row("Insertion Sort", "O(n²)")
    table.add_row("Merge Sort", "O(n log n)")
    console.print(table)

    n = N_ITEMS
    log_n = math.log2(n)
    proporcao_teorica = n / log_n

    tempo_insert_float = float(time_insert.replace(",", "."))
    tempo_merge_float = float(time_merge.replace(",", "."))
    proporcao_pratica = (
        tempo_insert_float / tempo_merge_float
        if tempo_merge_float > 0
        else float("inf")
    )

    analysis_text = f"""
    [bold]Qual consome mais energia?[/]
    O consumo de energia é proporcional ao tempo de CPU.
    O [bold red]Insertion Sort[/] levou [bold]{time_insert} ms[/], enquanto o [bold green]Merge Sort[/] levou [bold]{time_merge} ms[/].
    Claramente, o [bold]Insertion Sort consumiu muito mais energia[/bold].

    [bold]Qual a proporção?[/]
    A proporção teórica de operações é (n² / n log n) = (n / log n).
    Com n={N_ITEMS} e log₂({N_ITEMS})≈{log_n:.2f}, a proporção teórica é:
    [yellow]{N_ITEMS} / {log_n:.2f} ≈ {proporcao_teorica:.2f} vezes[/yellow]

    A proporção PRÁTICA (medida pelo tempo) foi:
    [yellow]{time_insert} ms / {time_merge} ms ≈ {proporcao_pratica:.2f} vezes[/yellow]
    """

    print("\n")
    console.print(
        Panel.fit(
            analysis_text,
            title=f"[bold cyan]Análise de Consumo e Proporção (n={N_ITEMS})[/bold cyan]",
            border_style="bright_magenta",
        )
    )


if __name__ == "__main__":
    main()
