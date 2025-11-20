from ui import menu, menu_logic
from utils.config.config_manager import ConfigManager

MENU_CONFIG = {
    "panel_title": "[bold magenta]📚  Análise de Similaridade Textual[/bold magenta]",
    "panel_border_style": "bold cyan",
    "groups": [
        {
            "title": "🔢 ALGORITMOS",
            "color": "green",
            "options": [
                {"number": 1, "description": "Subsequência Comum Mais Longa"},
                {"number": 2, "description": "Substring Comum Mais Longa"},
                {"number": 3, "description": "Distância de Edição - Levenshtein"},
            ],
        },
        {
            "title": "🤖 ANÁLISE LLMS",
            "color": "purple",
            "options": [
                {"number": 4, "description": "Ver prompts"},
                {"number": 5, "description": "Comparar respostas"},
            ],
        },
        {
            "title": "⭕ O GRANDE",
            "color": "yellow",
            "options": [
                {"number": 6, "description": "Análise de Notação Big O"},
            ],
        },
        {
            "title": "🔧 GERENCIAMENTO",
            "color": "cyan",
            "options": [
                {"number": 7, "description": "Configurações do Sistema"},
            ],
        },
        {
            "title": "🚪 SISTEMA",
            "color": "red",
            "options": [
                {"number": 8, "description": "Sair"},
            ],
        },
    ],
}


def main():
    """Função principal que executa o loop da aplicação."""
    config = ConfigManager()

    menu_actions = {
        1: lambda: menu_logic.execute_algorithm("Longest Common Subsequence"),
        2: lambda: menu_logic.execute_algorithm("Longest Common Substring"),
        3: lambda: menu_logic.execute_algorithm("Levenshtein"),
        4: lambda: menu_logic.show_llm_prompts(),
        5: lambda: menu_logic.compare_llm_responses(),
        6: lambda: menu_logic.big_o_analysis(),
        7: lambda: menu_logic.system_settings(config),
        8: lambda: menu_logic.exit_system(),
    }

    menu.clear_console()

    while True:
        menu.show_main_menu(MENU_CONFIG)
        min_option = min(menu.get_valid_menu_options(MENU_CONFIG))
        max_option = max(menu.get_valid_menu_options(MENU_CONFIG))
        opcao_input_str = f"[bold green]>[/bold green] Digite o número da sua opção [bold magenta][{min_option}-{max_option}][/bold magenta]"
        opcao = menu.ask_input_int("\n" + opcao_input_str)
        valid_options = menu.get_valid_menu_options(MENU_CONFIG)

        while opcao not in valid_options:
            menu.show_message("❌ Opção inválida. Tente novamente.", "bold red")
            opcao = menu.ask_input_int(opcao_input_str)

        if opcao != menu.get_valid_menu_options(MENU_CONFIG)[-1]:
            menu.clear_console()

        action = menu_actions.get(opcao)  # type: ignore
        if action:
            if opcao == menu.get_valid_menu_options(MENU_CONFIG)[-1]:
                action()
                break
            else:
                action()
        else:
            menu.show_message("❌ Opção não implementada.", "bold red")

        if opcao != menu.get_valid_menu_options(MENU_CONFIG)[-1]:
            menu.console.print(
                "[cyan]\nPressione [bold]Enter[/bold] para voltar ao menu...[/cyan]"
            )
            menu.ask_input("")
            menu.clear_console()


if __name__ == "__main__":
    menu.clear_console()
    try:
        main()
    except KeyboardInterrupt:
        menu.show_message("\n👋 Saindo do sistema. Até logo!", "bold magenta")
