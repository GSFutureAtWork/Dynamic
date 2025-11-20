from rich.table import Table
from rich import box
from rich.prompt import Prompt, Confirm
from ui.menu import atualizar_console, show_message
from utils.config.config_manager import TerminalTheme


def config_menu(config_manager):
    """Exibe as configurações como uma tabela interativa e permite edição"""
    show_message("⚙️  Configurações do Sistema", "bright_blue")

    config = config_manager.config

    tabela = Table(title="🔧 Configurações Atuais", box=box.SIMPLE_HEAVY)
    tabela.add_column("Opção", style="cyan", justify="right")
    tabela.add_column("Parâmetro", style="magenta")
    tabela.add_column("Valor Atual", style="green")

    tabela.add_row(
        "1",
        "Tema do terminal",
        "Sem cor (no_color)" if config.theme == "no_color" else "Padrão (colorido)",
    )
    # Removido: Tempo de delay entre ações
    tabela.add_row(
        "2",
        "Modo de depuração",
        "Ativado" if getattr(config, "debug", False) else "Desativado",
    )
    tabela.add_row(
        "3",
        "[yellow]Desfazer última alteração[/yellow]",
        (
            f"Disponível ({config_manager.get_undo_count()} ações)"
            if config_manager.has_undo_history()
            else "Indisponível"
        ),
    )
    tabela.add_row(
        "4",
        "[yellow]Redefinir configurações para padrão[/yellow]",
        "",
    )
    tabela.add_row(
        "0",
        "[red]Voltar ao menu principal[/red]",
        "",
    )

    print()
    from ui.console import get_console

    console = get_console()
    console.print(tabela)

    while True:
        escolha = Prompt.ask(
            "[magenta]Digite o número da configuração que deseja alterar[/magenta]",
            default="0",
            show_default=False,
            console=console,
        ).strip()
        if escolha == "0":
            show_message("Retornando ao menu...", "cyan")
            return
        elif escolha == "1":
            novo_tema = (
                TerminalTheme.NO_COLOR
                if config_manager.config.theme == TerminalTheme.DEFAULT
                else TerminalTheme.DEFAULT
            )
            config_manager.update_config(theme=novo_tema)
            atualizar_console()
            show_message(f"Tema atualizado para: {novo_tema.value}", "green")
            break
        elif escolha == "2":
            novo_debug = not getattr(config, "debug", False)
            config_manager.update_config(debug=novo_debug)
            if not novo_debug:
                show_message(
                    "Modo de depuração desativado",
                    "red",
                )
            else:
                show_message(
                    "Modo de depuração ativado",
                    "green",
                )
            break
        elif escolha == "3":
            if config_manager.undo_last_config_change():
                atualizar_console()
                show_message("Última alteração de configuração desfeita com sucesso!")
            else:
                show_message("Não há alterações de configuração para desfazer.", "red")
            break
        elif escolha == "4":
            confirmar = Confirm.ask(
                "[red]Tem certeza que deseja redefinir as configurações para o padrão?[/red]",
                default=False,
                choices=["s", "n"],
            )
            if confirmar:
                config_manager.reset_config()
                show_message("Configurações redefinidas para o padrão.", "green")
                atualizar_console()
                break
        else:
            show_message("Opção inválida.", "red")
    input("Pressione Enter para continuar...")
