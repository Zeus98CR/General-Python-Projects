"""Local AI assistant for technical questions and fictional Excel data analysis.

Install dependencies with:
    pip install pandas openpyxl ollama

Run with:
    python Local_AI_Data_Incident_Assistant.py
    python Local_AI_Data_Incident_Assistant.py --workbook path\\to\\workbook.xlsx
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

try:
    import pandas as pd  # type: ignore[reportMissingImports]
except ImportError:
    pd = None

if TYPE_CHECKING:
    DataFrame = pd.DataFrame
else:
    DataFrame = Any

try:
    import ollama  # type: ignore
except ImportError:
    ollama = None


DEFAULT_WORKBOOK_NAME = "Excel Data Training (Fictional Data).xlsx"
STOP_WORDS = {
    "about", "after", "all", "and", "are", "can", "data", "does", "for",
    "from", "how", "into", "that", "the", "their", "this", "what", "when",
    "where", "which", "with", "would", "you", "your",
}


class WorkbookData:
    """Load every workbook sheet and provide evidence for assistant answers."""

    def __init__(self, workbook_path: Path) -> None:
        self.workbook_path = workbook_path
        self.sheets: dict[str, DataFrame] = {}
        self.load()

    def load(self) -> None:
        if not self.workbook_path.exists():
            raise FileNotFoundError(f"Workbook not found: {self.workbook_path}")
        if pd is None:
            raise RuntimeError(
                "pandas is not installed. Run 'pip install pandas openpyxl'."
            )

        workbook = pd.ExcelFile(self.workbook_path)
        for sheet_name in workbook.sheet_names:
            frame = pd.read_excel(self.workbook_path, sheet_name=sheet_name)
            frame.columns = [str(column).strip() for column in frame.columns]
            self.sheets[sheet_name] = frame.dropna(how="all").reset_index(drop=True)

    @property
    def row_count(self) -> int:
        return sum(len(frame) for frame in self.sheets.values())

    def overview(self) -> str:
        lines = [
            f"Workbook: {self.workbook_path.name}",
            f"Sheets: {len(self.sheets)} | Total rows: {self.row_count}",
        ]
        for name, frame in self.sheets.items():
            lines.append(
                f"- {name}: {len(frame)} rows; columns: "
                f"{', '.join(map(str, frame.columns)) or '(none)'}"
            )
        return "\n".join(lines)

    def search(self, question: str, limit: int = 30) -> list[dict[str, Any]]:
        terms = [
            term for term in re.findall(r"[a-z0-9_-]+", question.lower())
            if len(term) > 2 and term not in STOP_WORDS
        ]
        matches: list[tuple[int, str, int, dict[str, Any]]] = []

        for sheet_name, frame in self.sheets.items():
            for row_number, row in frame.iterrows():
                values = {
                    str(key): self._clean_value(value)
                    for key, value in row.items()
                }
                searchable = json.dumps(values, default=str).lower()
                score = sum(searchable.count(term) for term in terms)
                if score:
                    matches.append((score, sheet_name, row_number, values))

        matches.sort(key=lambda item: item[0], reverse=True)
        return [
            {"sheet": sheet, "row": row_number + 2, "data": values}
            for _, sheet, row_number, values in matches[:limit]
        ]

    def trends(self) -> str:
        lines: list[str] = []
        for sheet_name, frame in self.sheets.items():
            date_columns = self._date_columns(frame)
            numeric_columns = frame.select_dtypes(include="number").columns.tolist()
            if not date_columns or not numeric_columns:
                continue

            date_column = date_columns[0]
            dates = pd.to_datetime(frame[date_column], errors="coerce")
            valid = frame.loc[dates.notna()].copy()
            valid[date_column] = dates[dates.notna()]
            if valid.empty:
                continue

            lines.append(f"Sheet '{sheet_name}' grouped by {date_column}:")
            for numeric_column in numeric_columns[:5]:
                values = pd.to_numeric(
                    valid[numeric_column], errors="coerce"
                ).dropna()
                if values.empty:
                    continue
                first = float(values.iloc[0])
                last = float(values.iloc[-1])
                change = last - first
                direction = (
                    "increased" if change > 0
                    else "decreased" if change < 0
                    else "did not change"
                )
                lines.append(
                    f"- {numeric_column}: {direction} from {first:.2f} to "
                    f"{last:.2f}; average {values.mean():.2f}, minimum "
                    f"{values.min():.2f}, maximum {values.max():.2f}."
                )
        return "\n".join(lines) or "No clear date-and-numeric trend columns were detected."

    @staticmethod
    def _date_columns(frame: DataFrame) -> list[str]:
        columns: list[str] = []
        for column in frame.columns:
            converted = pd.to_datetime(frame[column], errors="coerce")
            if converted.notna().mean() >= 0.7:
                columns.append(str(column))
        return columns

    @staticmethod
    def _clean_value(value: Any) -> Any:
        if pd.isna(value):
            return None
        if isinstance(value, pd.Timestamp):
            return value.isoformat()
        if hasattr(value, "item"):
            return value.item()
        return value


class IncidentAI:
    def __init__(self, workbook: WorkbookData, model: str = "llama3.2") -> None:
        self.workbook = workbook
        self.model = model
        self.conversation: list[dict[str, str]] = []
        self.system_instructions = """
You are a helpful local AI assistant specialising in Python, cybersecurity,
IT systems, software incidents, troubleshooting, programming concepts, and
incident response. You also answer questions about the supplied fictional
Excel workbook.

Use workbook evidence and calculated trend summaries when relevant. Do not
invent workbook values, incidents, or conclusions. If the workbook evidence
does not answer a question, say so clearly. For cybersecurity questions,
stay defensive, educational, and responsible. Explain technical concepts
simply unless the user asks for advanced detail.
"""

    def ask(self, question: str) -> str:
        if not question.strip():
            return "Please ask me a question."
        if ollama is None:
            return (
                "The workbook assistant is ready, but Ollama is not installed. "
                "Run 'pip install ollama' and make sure Ollama is running."
            )

        evidence = self.workbook.search(question)
        trend_summary = (
            self.workbook.trends()
            if self._requests_trends(question.lower())
            else ""
        )
        evidence_text = json.dumps(evidence, indent=2, default=str)
        if not evidence:
            evidence_text = "No matching workbook rows were found."

        user_prompt = (
            f"Workbook overview:\n{self.workbook.overview()}\n\n"
            f"Matching workbook rows:\n{evidence_text}\n\n"
            f"Calculated trend summary:\n{trend_summary or 'Not requested.'}\n\n"
            f"User question:\n{question}"
        )
        messages = [{"role": "system", "content": self.system_instructions}]
        messages.extend(self.conversation)
        messages.append({"role": "user", "content": user_prompt})

        try:
            response = ollama.chat(model=self.model, messages=messages)
            answer = response["message"]["content"]
        except Exception as error:
            return (
                "I could not connect to the local AI model.\n\n"
                f"Error: {error}\n\n"
                "Make sure Ollama is installed, running, and that the model is available."
            )

        self.conversation.extend([
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer},
        ])
        self.conversation = self.conversation[-10:]
        return answer

    @staticmethod
    def _requests_trends(question: str) -> bool:
        return any(
            word in question
            for word in (
                "trend", "trends", "over time", "increase", "decrease",
                "pattern", "change",
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local AI assistant with Excel data analysis."
    )
    parser.add_argument(
        "--workbook",
        type=Path,
        default=Path(__file__).with_name(DEFAULT_WORKBOOK_NAME),
        help="Path to the Excel workbook.",
    )
    parser.add_argument(
        "--model", default="llama3.2", help="Installed Ollama model name."
    )
    args = parser.parse_args()

    try:
        workbook = WorkbookData(args.workbook)
    except Exception as error:
        print(f"Could not load workbook: {error}")
        print("Place the workbook beside this script or pass --workbook <path>.")
        return

    assistant = IncidentAI(workbook, args.model)
    print("=" * 60)
    print("        LOCAL AI DATA AND INCIDENT ASSISTANT")
    print("=" * 60)
    print(f"AI model: {args.model} | {workbook.overview().splitlines()[1]}")
    print("Ask about Python, cybersecurity, IT systems, incidents, programming, or workbook data.")
    print("Ask for trends, changes, patterns, averages, or insights to trigger analysis.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            question = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break
        if question.strip().lower() in {"exit", "quit"}:
            print("Assistant: Goodbye!")
            break
        print(f"\nAssistant:\n{assistant.ask(question)}\n")


if __name__ == "__main__":
    main()
