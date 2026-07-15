"""
terminal.py — The core SVG rendering engine.

Converts plain text (with directives) into a complete SVG
that looks like a 90s hacker terminal window, complete with:

  • macOS-style traffic light buttons
  • CRT phosphor glow effect
  • Horizontal scanline overlay
  • Blinking block cursor
  • Directive-based text coloring and formatting
"""

from xml.sax.saxutils import escape
from . import theme


# ── Directive Parser ────────────────────────────────────────

def _parse_lines(body: str) -> list[dict]:
    """
    Parse body text into a list of render-able line dicts.

    Each dict has:
      type:  'text' | 'prompt' | 'comment' | 'highlight' | 'success'
             | 'warning' | 'error' | 'divider' | 'blank' | 'label' | 'ascii'
      text:  the string to render (already escaped for SVG)
      color: fill color
      extra: optional dict for label key/value split
    """
    lines = body.splitlines()
    parsed = []

    for raw in lines:
        stripped = raw.strip()

        # ── @blank ──
        if stripped == "@blank" or stripped == "":
            parsed.append({"type": "blank", "text": "", "color": theme.TEXT})
            continue

        # ── @divider ──
        if stripped == "@divider":
            parsed.append({"type": "divider", "text": "", "color": theme.COMMENT})
            continue

        # ── @prompt <text> ──
        if stripped.startswith("@prompt "):
            content = stripped[8:]
            parsed.append({
                "type": "prompt",
                "text": escape(content),
                "color": theme.PROMPT,
            })
            continue

        # ── @comment <text> ──
        if stripped.startswith("@comment "):
            content = stripped[9:]
            parsed.append({
                "type": "comment",
                "text": escape(f"# {content}"),
                "color": theme.COMMENT,
            })
            continue

        # ── @highlight <text> ──
        if stripped.startswith("@highlight "):
            content = stripped[11:]
            parsed.append({
                "type": "highlight",
                "text": escape(content),
                "color": theme.HIGHLIGHT,
            })
            continue

        # ── @success <text> ──
        if stripped.startswith("@success "):
            content = stripped[9:]
            parsed.append({
                "type": "success",
                "text": escape(f"  ✓ {content}"),
                "color": theme.SUCCESS,
            })
            continue

        # ── @warning <text> ──
        if stripped.startswith("@warning "):
            content = stripped[9:]
            parsed.append({
                "type": "warning",
                "text": escape(f"  ⚠ {content}"),
                "color": theme.WARNING,
            })
            continue

        # ── @error <text> ──
        if stripped.startswith("@error "):
            content = stripped[7:]
            parsed.append({
                "type": "error",
                "text": escape(f"  ✗ {content}"),
                "color": theme.ERROR,
            })
            continue

        # ── @label key :: value ──
        if stripped.startswith("@label "):
            content = stripped[7:]
            if "::" in content:
                key, value = content.split("::", 1)
                parsed.append({
                    "type": "label",
                    "text": "",
                    "color": theme.TEXT,
                    "extra": {
                        "key": escape(key.strip()),
                        "value": escape(value.strip()),
                    },
                })
            else:
                parsed.append({
                    "type": "text",
                    "text": escape(content),
                    "color": theme.TEXT,
                })
            continue

        # ── @ascii <text> (preserve as-is) ──
        if stripped.startswith("@ascii "):
            content = stripped[7:]
            parsed.append({
                "type": "ascii",
                "text": escape(content),
                "color": theme.TEXT,
            })
            continue

        # ── plain text (preserve leading whitespace) ──
        parsed.append({
            "type": "text",
            "text": escape(raw),
            "color": theme.TEXT,
        })

    return parsed


# ── Label Alignment ─────────────────────────────────────────

def _compute_label_width(parsed: list[dict]) -> int:
    """Find the longest key among all @label lines for alignment."""
    max_len = 0
    for line in parsed:
        if line["type"] == "label" and "extra" in line:
            key_len = len(line["extra"]["key"])
            if key_len > max_len:
                max_len = key_len
    return max_len + 2  # 2 char padding


# ── SVG Filters (CRT Glow) ─────────────────────────────────

def _build_glow_filter() -> str:
    """SVG filter definition for CRT phosphor glow."""
    if not theme.CRT_GLOW:
        return ""
    return f"""
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="{theme.GLOW_STD_DEV}" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>"""


# ── Scanline Pattern ───────────────────────────────────────

def _build_scanlines(height: int) -> str:
    """SVG pattern overlay for horizontal CRT scanlines."""
    if not theme.SCANLINES:
        return ""
    return f"""
  <defs>
    <pattern id="scanlines" width="100%" height="{theme.SCANLINE_GAP}" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="{theme.WIDTH}" y2="0"
            stroke="#000000" stroke-width="1" opacity="{theme.SCANLINE_OPACITY}"/>
    </pattern>
  </defs>
  <rect width="{theme.WIDTH}" height="{height}"
        fill="url(#scanlines)" pointer-events="none"/>"""


# ── Blinking Cursor ────────────────────────────────────────

def _build_cursor(x: float, y: float) -> str:
    """Animated blinking block cursor at the given position."""
    if not theme.CURSOR_BLINK:
        return ""
    return f"""
  <rect x="{x}" y="{y - theme.CURSOR_HEIGHT + 3}"
        width="{theme.CURSOR_WIDTH}" height="{theme.CURSOR_HEIGHT}"
        fill="{theme.CURSOR_COLOR}">
    <animate attributeName="opacity"
             values="1;1;0;0" dur="1.2s"
             repeatCount="indefinite"/>
  </rect>"""


# ── Main Builder ───────────────────────────────────────────

def build_terminal(title: str, body: str, command: str | None = None) -> str:
    """
    Build a complete SVG terminal window.

    Args:
        title:   Window title bar text (e.g. "root@dattanirjhar:~")
        body:    Content text, may include @directives
        command: Optional shell command shown as first line
                 (e.g. "whoami", "cat current_ops.log")

    Returns:
        Complete SVG string
    """
    parsed = _parse_lines(body)
    label_width = _compute_label_width(parsed)

    # Calculate total content lines (command line counts as one extra)
    total_lines = len(parsed)
    if command:
        total_lines += 1  # the prompt line
        total_lines += 1  # blank line after prompt

    # Calculate SVG height
    content_height = total_lines * theme.LINE_HEIGHT
    height = theme.HEADER_HEIGHT + theme.PADDING * 2 + content_height + 8

    svg = []

    # ── SVG root ──
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg"'
        f' width="{theme.WIDTH}" height="{height}"'
        f' viewBox="0 0 {theme.WIDTH} {height}">'
    )

    # ── Glow filter ──
    svg.append(_build_glow_filter())

    # ── Background ──
    svg.append(
        f'  <rect x="1" y="1" rx="{theme.RADIUS}" ry="{theme.RADIUS}"'
        f' width="{theme.WIDTH - 2}" height="{height - 2}"'
        f' fill="{theme.BACKGROUND}" stroke="{theme.BORDER}" stroke-width="1"/>'
    )

    # ── Header bar ──
    # Clip the header so rounded corners only appear at top
    svg.append(
        f'  <clipPath id="headerClip">'
        f'<rect width="{theme.WIDTH}" height="{theme.HEADER_HEIGHT}"'
        f' rx="{theme.RADIUS}" ry="{theme.RADIUS}"/></clipPath>'
    )
    svg.append(
        f'  <rect width="{theme.WIDTH}" height="{theme.HEADER_HEIGHT}"'
        f' fill="{theme.HEADER_BG}" clip-path="url(#headerClip)"/>'
    )
    # Header bottom edge (covers rounded bottom corners of header rect)
    svg.append(
        f'  <rect y="{theme.HEADER_HEIGHT - theme.RADIUS}"'
        f' width="{theme.WIDTH}" height="{theme.RADIUS}"'
        f' fill="{theme.HEADER_BG}"/>'
    )
    # Subtle header border
    svg.append(
        f'  <line x1="0" y1="{theme.HEADER_HEIGHT}" x2="{theme.WIDTH}"'
        f' y2="{theme.HEADER_HEIGHT}" stroke="{theme.BORDER}" stroke-width="1"/>'
    )

    # ── macOS traffic light buttons ──
    buttons = [
        (theme.BUTTON_RED, 20),
        (theme.BUTTON_YELLOW, 40),
        (theme.BUTTON_GREEN, 60),
    ]
    for color, cx in buttons:
        svg.append(
            f'  <circle cx="{cx}" cy="{theme.HEADER_HEIGHT // 2}"'
            f' r="6" fill="{color}"/>'
        )

    # ── Title text ──
    svg.append(
        f'  <text x="{theme.WIDTH // 2}" y="{theme.HEADER_HEIGHT // 2 + 4}"'
        f' fill="{theme.TITLE_COLOR}" font-family="{theme.FONT_FAMILY}"'
        f' font-size="{theme.TITLE_FONT_SIZE}" text-anchor="middle">'
        f'{escape(title)}</text>'
    )

    # ── Content area ──
    glow_attr = ' filter="url(#glow)"' if theme.CRT_GLOW else ""
    content_group = f'  <g{glow_attr}>'
    svg.append(content_group)

    y = theme.HEADER_HEIGHT + theme.PADDING + theme.FONT_SIZE
    x = theme.PADDING

    # Optional command prompt line
    if command:
        prompt_text = f"root@dattanirjhar:~# {command}"
        svg.append(
            f'    <text x="{x}" y="{y}"'
            f' fill="{theme.PROMPT}" font-family="{theme.FONT_FAMILY}"'
            f' font-size="{theme.FONT_SIZE}">'
            f'{escape(prompt_text)}</text>'
        )
        y += theme.LINE_HEIGHT  # move past prompt
        y += theme.LINE_HEIGHT  # blank line after prompt

    # Track cursor position for blinking cursor
    last_text_x = x
    last_text_y = y

    for line in parsed:
        if line["type"] == "blank":
            y += theme.LINE_HEIGHT
            continue

        if line["type"] == "divider":
            # Dotted horizontal line
            svg.append(
                f'    <line x1="{x}" y1="{y - theme.FONT_SIZE // 2 + 2}"'
                f' x2="{theme.WIDTH - theme.PADDING}"'
                f' y2="{y - theme.FONT_SIZE // 2 + 2}"'
                f' stroke="{theme.COMMENT}" stroke-width="1"'
                f' stroke-dasharray="4,6" opacity="0.5"/>'
            )
            y += theme.LINE_HEIGHT
            continue

        if line["type"] == "label":
            extra = line["extra"]
            key = extra["key"]
            value = extra["value"]
            # Pad key to align values
            padded_key = key.ljust(label_width)
            svg.append(
                f'    <text x="{x}" y="{y}"'
                f' font-family="{theme.FONT_FAMILY}"'
                f' font-size="{theme.FONT_SIZE}">'
                f'<tspan fill="{theme.MUTED}">{padded_key}</tspan>'
                f'<tspan fill="{theme.TEXT}">{value}</tspan>'
                f'</text>'
            )
            last_text_x = x + (len(padded_key) + len(value)) * theme.CHAR_WIDTH
            last_text_y = y
            y += theme.LINE_HEIGHT
            continue

        # All other types: text, prompt, comment, highlight, success, warning, error, ascii
        svg.append(
            f'    <text x="{x}" y="{y}"'
            f' fill="{line["color"]}" font-family="{theme.FONT_FAMILY}"'
            f' font-size="{theme.FONT_SIZE}">'
            f'{line["text"]}</text>'
        )
        text_len = len(line["text"])
        last_text_x = x + text_len * theme.CHAR_WIDTH
        last_text_y = y
        y += theme.LINE_HEIGHT

    svg.append("  </g>")

    # ── Scanlines ──
    svg.append(_build_scanlines(height))

    # ── Blinking cursor ──
    svg.append(_build_cursor(last_text_x + 4, last_text_y))

    svg.append("</svg>")

    return "\n".join(svg)
