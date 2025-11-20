from ui import config
import core.dp as dp
import core.llm_analysis as llm
import core.o_notation as o_notation

from . import menu


def execute_algorithm(algorithm):
    """Opção 1: Longest Common Subsequence (LCS)"""
    menu.show_title(f"Algoritmo: {algorithm}")
    dp.algorithm_tests(algorithm)


def show_llm_prompts():
    """Opção 8: Ver prompts"""
    llm.show_llm_prompts()


def compare_llm_responses():
    # Solicita ao usuário que escolha o algoritmo
    menu.show_message("🤖 Comparando [bold]LLMs[/bold]...", "yellow")

    chave_menu = {
        "1": (
            dp.longest_common_subsequence_iter,
            "🔗 Longest Common Subsequence",
        ),
        "2": (dp.longest_common_substring_iter, "🔗 Longest Common Substring"),
        "3": (dp.levenshtein_distance_iter, "🔗 Levenshtein"),
    }

    opcoes_texto = "\n".join([f"[{k}] {v[1]}" for k, v in chave_menu.items()])
    menu.show_message(
        f"[bold]Escolha o algoritmo a ser utilizado:[/bold]\n{opcoes_texto}",
        "white",
        new_line_start=False,
    )

    chave_algoritmo = menu.ask_input(
        "Digite o número da opção desejada",
        choices=list(chave_menu.keys()),
        default="3",
    )

    algorithm, _ = chave_menu.get(
        chave_algoritmo,  # type: ignore
        (dp.levenshtein_distance_iter, "🔗 Levenshtein"),
    )
    menu.clear_console()
    llm.compare_llm_responses(algorithm)


def big_o_analysis():
    """Opção 6: Análise de Notação Big O"""
    o_notation.big_o_analysis()


def system_settings(config_manager):
    """Opção 9: Configurações do Sistema"""
    config.config_menu(config_manager)


def exit_system():
    """Opção 10: Sair"""
    menu.show_message("👋 Saindo do sistema. Até logo!", "bold magenta")
