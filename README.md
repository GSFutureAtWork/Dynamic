## 🚀 Tecnologias Utilizadas

- **[Python 3.13+](https://www.python.org/)**: Linguagem principal do projeto.
- **[Rich](https://github.com/Textualize/rich)**: Para criar uma interface de linha de comando rica e colorida, com tabelas, painéis e texto estilizado.

## 🛠️ Instalação e Execução

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.
Você pode usar **pip** (tradicional) ou **uv** (recomendado, mais rápido e simples).

1. **Clone o repositório:**

   ```sh
   git clone https://github.com/Asteriuz/challenge3-dynamic_programming.git
   cd gerenciador-insumos
   ```

### 🔹 Opção 1 — Usando `pip` (tradicional)

2. **Crie e ative um ambiente virtual:**

   ```sh
   python -m venv .venv

   # Windows
   .\.venv\Scripts\activate

   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Instale as dependências:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**

   ```sh
   python main.py
   ```

   _Na primeira execução, se o arquivo `data/consumo.json` não existir, o programa perguntará se você deseja gerar dados simulados._

### 🔹 Opção 2 — Usando `uv` (recomendado 🚀)

2. **Instale o `uv` (se ainda não tiver):**

   ```sh
   pip install uv
   ```

3. **Sincronize as dependências automaticamente (Opcional | _uv run realiza o sync antes_):**

   ```sh
   uv sync
   ```

   > Isso cria e gerencia o ambiente virtual automaticamente, sem precisar rodar `venv` manualmente.

4. **Execute a aplicação dentro do ambiente:**

   ```sh
   uv run main.py
   ```

## 📂 Estrutura do Projeto

```
.
├── core/                       # Módulos com a lógica principal (Respostas das 3 questões)
│   ├── dp.py                   # Algoritmos de programação dinâmica (Levenshtein, Longest Common Subsequence, Longest Common Substring)
│   ├── llm_analysis.py         # Análise de similaridade usando LLMs
│   └── o_notation.py           # Implementação da notação O grande
├── data/
│   ├── llms/                   # Respostas geradas por LLMs (em formato p[num].txt)
│   │   ├── chatgpt/
│   │   ├── deepseek/
│   │   └── gemini/
│   └── config.json
├── ui/                         # Módulos responsáveis pela interface
│   ├── config.py
│   ├── console.py
│   ├── menu.py
│   └── menu_logic.py
├── utils/                      # Módulos de utilidades
│   ├── config/
│   │   └── config_manager.py
│   └── measure_time.py
├── .gitignore
├── main.py                     # Arquivo principal para executar a aplicação
├── pyproject.toml
├── README.md
├── relatorio.pdf                # Relatório do desafio
└── requirements.txt
```
