import argparse
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown

from .graph import build_graph


console = Console()


def run_once(query: str) -> str:
    app = build_graph()
    state = {"query": query}
    result = app.invoke(state)
    return result.get("summary", "No answer produced.")


def interactive_loop():
    app = build_graph()
    console.print("[bold green]Local Research Agent[/bold green] — type 'exit' to quit.")
    while True:
        try:
            query = console.input("[bold cyan]> [/bold cyan]")
        except (EOFError, KeyboardInterrupt):
            console.print("\nGoodbye!")
            break
        if not query or query.lower().strip() in {"exit", "quit"}:
            console.print("Goodbye!")
            break
        state = {"query": query}
        result = app.invoke(state)
        answer = result.get("summary", "No answer produced.")
        console.print(Markdown(answer))


def main():
    parser = argparse.ArgumentParser(description="Local Research Agent CLI")
    parser.add_argument("--query", help="Single-shot question to ask", default=None)
    args = parser.parse_args()

    if args.query:
        answer = run_once(args.query)
        console.print(Markdown(answer))
    else:
        interactive_loop()


if __name__ == "__main__":
    main()

