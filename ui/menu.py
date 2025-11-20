from os import system, name
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt, InvalidResponse
from rich.text import Text
from rich.theme import Theme

from ui.console import get_console


# ------------------------------- Custom Theme ------------------------------- #
custom_theme = Theme(
    {
        "red": "#ff5555",
        "green": "#50fa7b",
        "yellow": "#f1fa8c",
        "cyan": "#8be9fd",
        "purple": "#bd93f9",
        "magenta": "#ff79c6",
    }
)


def clear_console():
    """Limpa o console de forma cross-platform."""
    if name == "nt":
        _ = system("cls")
    else:
        _ = system("clear")


# ---------------------------------- Config ---------------------------------- #
console = get_console()

# ---------------------------------- Menu ----------------------------------- #


def atualizar_console():
    global console
    console = get_console(force_reload=True)


def show_main_menu(config):
    """Exibe o menu principal estilizado com grupos e cores"""
    menu_text = Text()

    for group_index, group in enumerate(config["groups"]):
        menu_text.append(f"{group['title']}\n", style=" bold " + group["color"])
        for option in group["options"]:
            is_last_group = group_index == len(config["groups"]) - 1
            is_last_option = option == group["options"][-1]
            option_line = f"  [{option['number']}] {option['description']}"
            if not (is_last_group and is_last_option):
                option_line += "\n"
            menu_text.append(option_line, style=f"{group['color']}")
        if group_index < len(config["groups"]) - 1:
            menu_text.append("\n")

    panel = Panel.fit(
        menu_text,
        title=config["panel_title"],
        border_style=config["panel_border_style"],
        padding=(1, 2),
    )
    console.print(panel, new_line_start=True)


def get_valid_menu_options(config):
    """Retorna uma lista com os números de opções válidas do menu."""
    valid_options = []
    for group in config["groups"]:
        for option in group["options"]:
            valid_options.append(option["number"])
    return valid_options


def get_menu_option_description(option_number, config):
    """Retorna a descrição de uma opção específica do menu."""
    for group in config["groups"]:
        for option in group["options"]:
            if option["number"] == option_number:
                return option["description"]
    return None


class PromptPT(Prompt):
    def process_response(self, value: str):
        try:
            return super().process_response(value)
        except InvalidResponse:
            raise InvalidResponse(
                "\n[bold red]❌ Selecione uma das opções disponíveis.[/bold red]\n"
            )


def ask_input(prompt_text="Escolha uma opção: ", choices=None, default=None):
    """Solicita uma entrada do usuário."""
    return PromptPT.ask(prompt_text, choices=choices, default=default)


class IntPromptPT(IntPrompt):
    def process_response(self, value: str):
        try:
            return int(value)
        except ValueError:
            raise InvalidResponse(
                "\n[bold red]❌ Por favor, digite um número inteiro válido.[/bold red]\n"
            )


def ask_input_int(prompt_text="Escolha uma opção: ", default=None):
    """Solicita um número inteiro do usuário."""
    return IntPromptPT.ask(prompt_text, default=default)


def show_message(message, style="bold green", new_line_start=True):
    """Exibe uma mensagem simples estilizada."""
    if new_line_start:
        console.print(f"\n[{style}]{message}[/{style}]\n")
    else:
        console.print(f"[{style}]{message}[/{style}]\n")


def show_title(title):
    """Exibe um título estilizado."""
    console.print(
        Panel.fit(
            f"[bold white]{title}[/bold white]",
            border_style="bold blue",
        ),
        new_line_start=True,
    )
    print()
