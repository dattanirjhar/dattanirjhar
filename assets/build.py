#!/usr/bin/env python3
"""
build.py — Build all terminal SVG panels from content files.

Usage:
    python build.py              # build all panels
    python build.py whoami       # build a single panel
    python build.py --list       # list available content files

Content files live in content/*.txt
Output SVGs are written to output/*.svg
"""

import sys
from pathlib import Path

# Add templates to path so imports work when running from assets/
sys.path.insert(0, str(Path(__file__).parent))

from templates.terminal import build_terminal


CONTENT_DIR = Path(__file__).parent / "content"
OUTPUT_DIR  = Path(__file__).parent / "output"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Parse optional YAML-like frontmatter from a content file.

    Frontmatter is delimited by --- lines:
        ---
        title: some title
        command: some command
        order: 1
        ---
        Body content here...

    Returns (metadata_dict, body_string).
    """
    meta = {}
    body = text

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            # parts[0] is empty (before first ---)
            # parts[1] is the frontmatter
            # parts[2] is the body
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip()
            body = parts[2].strip()

    return meta, body


def build_one(file: Path) -> Path:
    """Build a single content file into an SVG. Returns output path."""
    raw = file.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)

    title = meta.get("title", file.stem)
    command = meta.get("command", None)

    svg = build_terminal(title=title, body=body, command=command)

    out = OUTPUT_DIR / f"{file.stem}.svg"
    out.write_text(svg, encoding="utf-8")

    return out


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    # List mode
    if "--list" in sys.argv:
        files = sorted(CONTENT_DIR.glob("*.txt"))
        print(f"\n  📁 {len(files)} content files in {CONTENT_DIR}/\n")
        for f in files:
            raw = f.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(raw)
            order = meta.get("order", "?")
            cmd = meta.get("command", "—")
            print(f"  [{order}] {f.stem:20s}  cmd: {cmd}")
        print()
        return

    # Single file mode
    if len(sys.argv) > 1 and sys.argv[1] != "--list":
        name = sys.argv[1]
        file = CONTENT_DIR / f"{name}.txt"
        if not file.exists():
            print(f"  ✗ Content file not found: {file}")
            sys.exit(1)
        out = build_one(file)
        size = out.stat().st_size
        print(f"  ✓ Built {out.name} ({size:,} bytes)")
        return

    # Build all
    files = sorted(CONTENT_DIR.glob("*.txt"))
    if not files:
        print("  ✗ No content files found in content/")
        sys.exit(1)

    # Sort by order if available
    def sort_key(f):
        raw = f.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(raw)
        try:
            return int(meta.get("order", 999))
        except ValueError:
            return 999

    files = sorted(files, key=sort_key)

    print()
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║  Terminal SVG Generator — Building panels... ║")
    print("  ╚══════════════════════════════════════════════╝")
    print()

    total_size = 0
    for file in files:
        out = build_one(file)
        size = out.stat().st_size
        total_size += size
        print(f"  ✓ {out.name:25s} {size:>6,} bytes")

    print()
    print(f"  ──────────────────────────────────────────────")
    print(f"  Built {len(files)} panels → {OUTPUT_DIR}/")
    print(f"  Total size: {total_size:,} bytes")
    print()


if __name__ == "__main__":
    main()
