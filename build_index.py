from pathlib import Path
from html import escape


TITLE = "Misc Slides Pages"
INTRO = (
    "This GitHub Pages site hosts miscellaneous HTML content used for "
    "slide presentations and interactive demos."
)
OUTPUT_FILE = "index.html"
IGNORE_DIRS = {".git", ".github", "__pycache__"}
IGNORE_FILES = {OUTPUT_FILE}
HTML_SUFFIXES = {".html", ".htm"}


def is_hidden(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def nice_name(path: Path) -> str:
    name = path.stem if path.is_file() else path.name
    return name.replace("_", " ").replace("-", " ").strip().title()


def collect_entries(root: Path) -> tuple[list[Path], list[Path]]:
    dirs = []
    html_files = []

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)

        if is_hidden(rel):
            continue

        if any(part in IGNORE_DIRS for part in rel.parts):
            continue

        if path.is_dir():
            dirs.append(rel)
            continue

        if path.name in IGNORE_FILES:
            continue

        if path.suffix.lower() in HTML_SUFFIXES:
            html_files.append(rel)

    return dirs, html_files


def build_list_items(paths: list[Path]) -> str:
    if not paths:
        return "<li>No entries found.</li>"

    items = []
    for rel in paths:
        href = escape(rel.as_posix())
        label = escape(rel.as_posix())
        items.append(f'                <li><a href="{href}">{label}</a></li>')
    return "\n".join(items)


def build_html(root: Path) -> str:
    dirs, html_files = collect_entries(root)

    dir_items = build_list_items(dirs)
    file_items = build_list_items(html_files)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(TITLE)}</title>
    <style>
        body {{
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                Roboto, Helvetica, Arial, sans-serif;
            background: #f7f7f8;
            color: #1f1f1f;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            padding: 4rem 1.5rem;
        }}

        h1 {{
            font-size: 2.4rem;
            margin-bottom: 0.5rem;
        }}

        h2 {{
            margin-top: 0;
        }}

        p {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: #444;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }}

        .card {{
            background: white;
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }}

        ul {{
            padding-left: 1.2rem;
            margin-bottom: 0;
        }}

        li {{
            margin: 0.55rem 0;
            overflow-wrap: anywhere;
        }}

        a {{
            color: #0b57d0;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .footer {{
            margin-top: 3rem;
            font-size: 0.95rem;
            color: #666;
        }}

        code {{
            background: #f1f3f5;
            padding: 0.15rem 0.35rem;
            border-radius: 6px;
            font-size: 0.95em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{escape(TITLE)}</h1>
        <p>{escape(INTRO)}</p>

        <div class="grid">
            <div class="card">
                <h2>Directories</h2>
                <ul>
{dir_items}
                </ul>
            </div>

            <div class="card">
                <h2>HTML Pages</h2>
                <ul>
{file_items}
                </ul>
            </div>
        </div>

        <p class="footer">
            This page is auto-generated from the repository contents.
            Re-run <code>build_index.py</code> after adding new files.
        </p>
    </div>
</body>
</html>
"""


def main() -> None:
    root = Path.cwd()
    html = build_html(root)
    (root / OUTPUT_FILE).write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()