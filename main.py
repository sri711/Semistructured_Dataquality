# python main.py sample.md         
import asyncio
import sys
import json
from evaluate import evaluate_all
from rich.table import Table
from rich.console import Console
from io import StringIO

def render_score_table(results):
    table = Table(title="Data Quality Scores", show_lines=True)
    table.add_column("Dimension", style="cyan", no_wrap=True)
    table.add_column("Score", style="green")

    for dimension, output in results.items():
        score = output.get("score", "N/A")
        table.add_row(dimension.capitalize(), f"{score:.2f}" if isinstance(score, float) else str(score))
    return table

def render_json_section(dimension, output):
    section = StringIO()
    section.write(f"\n\n=== {dimension.upper()} DETAILS ===\n\n")
    
    details = output.get("details", [])
    if not details:
        section.write("No detailed information available.\n")
        return section.getvalue()

    # Use the first dictionary's keys as headers
    keys = sorted(set().union(*(d.keys() for d in details)))

    table = Table(show_header=True, header_style="bold magenta")
    for key in keys:
        table.add_column(key)

    for entry in details:
        row = [json.dumps(entry.get(k, ""), ensure_ascii=False) for k in keys]
        table.add_row(*row)

    console = Console(file=section, width=120, force_terminal=False)
    console.print(table)
    return section.getvalue()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <markdown_file.md>")
        exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        markdown = f.read()

    results = asyncio.run(evaluate_all(markdown))

    output_lines = StringIO()

    # Generate and write the summary score table
    console = Console(file=output_lines, width=100, force_terminal=False)
    console.print(render_score_table(results))

    # Append the detailed JSON reasoning for each dimension
    for dimension, output in results.items():
        output_lines.write(render_json_section(dimension, output))

    # Write final results to output.txt
    with open("output.txt", "w", encoding="utf-8") as out_file:
        out_file.write(output_lines.getvalue())

    print("✅ Evaluation completed. See 'output.txt' for structured results.")
