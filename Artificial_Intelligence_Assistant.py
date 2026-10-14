"""Simple terminal AI assistant powered by Ollama.

Install and run:
    pip install ollama
    ollama pull llama3.2
    ollama serve
    python Artificial_Intelligence_Assistant.py

You can also choose a different installed model:
    python Artificial_Intelligence_Assistant.py --model llama3.1
"""

from __future__ import annotations

import argparse

try:
    import ollama  # type: ignore[reportMissingImports]
except ImportError:
    ollama = None


def ask_question(question: str, model: str = "llama3.2") -> str:
    """Send a single question to the local Ollama model."""
    if not question.strip():
        return "Please ask me a question."

    if ollama is None:
        return (
            "The Ollama Python package is not installed.\n"
            "Run: pip install ollama\n"
            "Then start Ollama with: ollama serve\n"
            "And pull a model such as: ollama pull llama3.2"
        )

    try:
        response = ollama.chat(
            model=model,
            messages=[{"role": "user", "content": question}],
        )
        content = response.get("message", {}).get("content", "")
        return content.strip() or "I did not get a response from the model."
    except Exception as error:
        return (
            "I could not connect to the local AI model.\n\n"
            "Make sure Ollama is installed and running, and that the model exists.\n\n"
            f"Error: {error}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simple terminal-based AI assistant using Ollama."
    )
    parser.add_argument(
        "--model",
        default="llama3.2",
        help="Installed Ollama model name (for example: llama3.2 or llama3.1).",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("        SIMPLE TERMINAL AI ASSISTANT")
    print("=" * 60)
    print(f"Model: {args.model}")
    print("Ask any basic question. Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            question = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if question.strip().lower() in {"exit", "quit"}:
            print("Assistant: Goodbye!")
            break

        answer = ask_question(question, args.model)
        print(f"\nAssistant:\n{answer}\n")


if __name__ == "__main__":
    main()