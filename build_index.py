from collections import defaultdict
from html import escape
from pathlib import Path


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


def display_name(path: Path) -> str:
    if path.name.lower() == "index.html":
        return "index"
    return path.stem.replace("_", " ").replace("-", " ")


def collect_html_files(root: Path) -> dict[str, list[Path]]:
    grouped = defaultdict(list)

    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)

        if is_hidden(rel):
            continue
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if path.is_dir():
            continue
        if path.name in IGNORE_FILES:
            continue
        if path.suffix.lower() not in HTML_SUFFIXES:
            continue

        parent = rel.parent.as_posix()
        group = "." if parent == "." else parent
        grouped[group].append(rel)

    return dict(sorted(grouped.items(), key=lambda kv: kv[0]))


def build_group_sections(grouped: dict[str, list[Path]]) -> str:
    if not grouped:
        return """\
            <div class="card">
                <h2>No HTML pages found</h2>
                <p>Add some exported HTML files and push again.</p>
            </div>"""

    sections = []
    for group, files in grouped.items():
        title = "Root" if group == "." else group
        items = []
        for rel in files:
            href = escape(rel.as_posix())
            label = escape(display_name(rel))
            sublabel = escape(rel.as_posix())
            items.append(
                "                    <li>"
                f'<a href="{href}">{label}</a>'
                f'<span class="path">{sublabel}</span>'
                "</li>"
            )

        section = f"""\
            <div class="card">
                <h2>{escape(title)}</h2>
                <ul>
{chr(10).join(items)}
                </ul>
            </div>"""
        sections.append(section)

    return "\n".join(sections)


def build_html(root: Path) -> str:
    grouped = collect_html_files(root)
    sections = build_group_sections(grouped)

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
            max-width: 1100px;
            margin: 0 auto;
            padding: 4rem 1.5rem;
        }}

        h1 {{
            font-size: 2.4rem;
            margin-bottom: 0.5rem;
        }}

        p {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: #444;
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }}

        .card {{
            background: white;
            border-radius: 14px;
            padding: 1.5rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }}

        h2 {{
            margin-top: 0;
            margin-bottom: 1rem;
            font-size: 1.2rem;
        }}

        ul {{
            padding-left: 1.2rem;
            margin: 0;
        }}

        li {{
            margin: 0.7rem 0;
            overflow-wrap: anywhere;
        }}

        a {{
            color: #0b57d0;
            text-decoration: none;
            font-weight: 600;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        .path {{
            display: block;
            margin-top: 0.15rem;
            color: #666;
            font-size: 0.92rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
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
{sections}
        </div>

        <p class="footer">
            This page is auto-generated on push by GitHub Actions.
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