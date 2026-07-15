"""
terminal.py — The core SVG rendering engine.

Converts plain text (with directives) into a complete SVG
that looks like a 90s hacker terminal window.

Features:
  • macOS chrome (optional — header bar + traffic lights)
  • CRT phosphor glow + scanline overlay
  • Matrix digital rain + HUD grid + corner brackets
  • Blinking block cursor
  • Directives: @prompt @comment @highlight @success @warning
                @error @label @divider @blank @ascii
                @bar (horizontal skill bars)
                @pipeline (flow diagrams)
"""

import random
from xml.sax.saxutils import escape
from . import theme


# ═══════════════════════════════════════════════════════════
#  Directive Parser
# ═══════════════════════════════════════════════════════════

def _parse_lines(body: str) -> list[dict]:
    """Parse body text into a list of renderable line dicts."""
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
            parsed.append({
                "type": "prompt",
                "text": escape(stripped[8:]),
                "color": theme.PROMPT,
            })
            continue

        # ── @comment <text> ──
        if stripped.startswith("@comment "):
            parsed.append({
                "type": "comment",
                "text": escape(f"# {stripped[9:]}"),
                "color": theme.COMMENT,
            })
            continue

        # ── @highlight <text> ──
        if stripped.startswith("@highlight "):
            parsed.append({
                "type": "highlight",
                "text": escape(stripped[11:]),
                "color": theme.HIGHLIGHT,
            })
            continue

        # ── @success <text> ──
        if stripped.startswith("@success "):
            parsed.append({
                "type": "success",
                "text": escape(f"  ✓ {stripped[9:]}"),
                "color": theme.SUCCESS,
            })
            continue

        # ── @warning <text> ──
        if stripped.startswith("@warning "):
            parsed.append({
                "type": "warning",
                "text": escape(f"  ⚠ {stripped[9:]}"),
                "color": theme.WARNING,
            })
            continue

        # ── @error <text> ──
        if stripped.startswith("@error "):
            parsed.append({
                "type": "error",
                "text": escape(f"  ✗ {stripped[7:]}"),
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
                parsed.append({"type": "text", "text": escape(content), "color": theme.TEXT})
            continue

        # ── @bar label :: percentage ──
        if stripped.startswith("@bar "):
            content = stripped[5:]
            if "::" in content:
                parts = content.split("::", 1)
                label = parts[0].strip()
                try:
                    pct = min(100, max(0, int(parts[1].strip())))
                except ValueError:
                    pct = 0
                parsed.append({
                    "type": "bar",
                    "text": "",
                    "color": theme.TEXT,
                    "extra": {"label": escape(label), "pct": pct},
                })
            continue

        # ── @pipeline step >> step >> step ──
        if stripped.startswith("@pipeline "):
            content = stripped[10:]
            steps = [s.strip() for s in content.split(">>")]
            parsed.append({
                "type": "pipeline",
                "text": "",
                "color": theme.TEXT,
                "extra": {"steps": [escape(s) for s in steps]},
            })
            continue

        # ── @ascii <text> (preserve as-is) ──
        if stripped.startswith("@ascii "):
            parsed.append({
                "type": "ascii",
                "text": escape(stripped[7:]),
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


# ═══════════════════════════════════════════════════════════
#  Alignment Helpers
# ═══════════════════════════════════════════════════════════

def _compute_label_width(parsed: list[dict]) -> int:
    """Max key length among @label lines, plus padding."""
    max_len = 0
    for line in parsed:
        if line["type"] == "label" and "extra" in line:
            max_len = max(max_len, len(line["extra"]["key"]))
    return max_len + 2 if max_len else 0


def _compute_bar_label_width(parsed: list[dict]) -> int:
    """Max label length among @bar lines, plus padding."""
    max_len = 0
    for line in parsed:
        if line["type"] == "bar" and "extra" in line:
            max_len = max(max_len, len(line["extra"]["label"]))
    return max_len + 2 if max_len else 0


# ═══════════════════════════════════════════════════════════
#  SVG Definitions (filters, patterns, markers)
# ═══════════════════════════════════════════════════════════

def _build_defs(has_pipeline: bool) -> str:
    """Single <defs> block with all filters, patterns, and markers."""
    parts = []

    if theme.CRT_GLOW:
        parts.append(
            f'    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">\n'
            f'      <feGaussianBlur in="SourceGraphic" stdDeviation="{theme.GLOW_STD_DEV}" result="blur"/>\n'
            f'      <feMerge>\n'
            f'        <feMergeNode in="blur"/>\n'
            f'        <feMergeNode in="SourceGraphic"/>\n'
            f'      </feMerge>\n'
            f'    </filter>'
        )

    if theme.SCANLINES:
        parts.append(
            f'    <pattern id="scanlines" width="100%" height="{theme.SCANLINE_GAP}" patternUnits="userSpaceOnUse">\n'
            f'      <line x1="0" y1="0" x2="{theme.WIDTH}" y2="0"\n'
            f'            stroke="#000" stroke-width="1" opacity="{theme.SCANLINE_OPACITY}"/>\n'
            f'    </pattern>'
        )

    # Background Grid pattern
    parts.append(
        f'    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">\n'
        f'      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="{theme.GRID_COLOR}" stroke-width="0.5" opacity="{theme.GRID_OPACITY}"/>\n'
        f'    </pattern>'
    )

    if has_pipeline:
        parts.append(
            f'    <marker id="arrow" markerWidth="8" markerHeight="6"\n'
            f'            refX="8" refY="3" orient="auto">\n'
            f'      <polygon points="0 0, 8 3, 0 6" fill="{theme.COMMENT}"/>\n'
            f'    </marker>'
        )

    return "  <defs>\n" + "\n".join(parts) + "\n  </defs>"


# ═══════════════════════════════════════════════════════════
#  Overlays, HUD, & Cyber Rain
# ═══════════════════════════════════════════════════════════

def _build_hud_elements(width: int, height: int, chrome: bool) -> str:
    """Corner brackets and background elements for the Ghost in the Shell HUD aesthetic."""
    cx = width
    cy = height
    m = theme.PADDING // 2
    l = 16 # Bracket leg length
    s = 1.5 # Stroke width
    
    y_offset = theme.HEADER_HEIGHT if chrome else 0
    top = y_offset + m
    bot = cy - m

    paths = [
        # Top-left bracket
        f'M {m+l} {top} L {m} {top} L {m} {top+l}',
        # Top-right bracket
        f'M {cx-m-l} {top} L {cx-m} {top} L {cx-m} {top+l}',
        # Bottom-left bracket
        f'M {m+l} {bot} L {m} {bot} L {m} {bot-l}',
        # Bottom-right bracket
        f'M {cx-m-l} {bot} L {cx-m} {bot} L {cx-m} {bot-l}',
    ]
    
    d = " ".join(paths)
    return f'  <path d="{d}" fill="none" stroke="{theme.PROMPT}" stroke-width="{s}" opacity="0.6"/>'

def _build_matrix_rain(width: int, height: int) -> str:
    """Subtle matrix code rain in the background."""
    # Generate static digital rain so SVG doesn't need JS
    chars = "01ﾊﾐﾋｰｳｼﾅﾓﾆｻﾜﾂｵﾘｱﾎﾃﾏｹﾒｴｶｷﾑﾕﾗｾﾈｽﾀﾇﾍ123456789"
    lines = []
    random.seed(42) # Deterministic for SVG reproducibility
    
    num_columns = width // 30
    for col in range(num_columns):
        if random.random() > 0.4: # Only 60% of columns have rain
            x = col * 30 + 15
            y_start = random.randint(-50, height // 2)
            length = random.randint(5, 20)
            
            col_chars = []
            for i in range(length):
                char = random.choice(chars)
                y = y_start + (i * 16)
                if 0 < y < height:
                    opacity = random.uniform(0.01, 0.05) # VERY subtle
                    col_chars.append(f'<text x="{x}" y="{y}" fill="{theme.TEXT}" font-family="{theme.FONT_FAMILY}" font-size="14" opacity="{opacity:.2f}">{char}</text>')
            
            lines.extend(col_chars)
            
    return "\n".join(["  <g class=\"matrix-rain\">"] + lines + ["  </g>"])


def _build_scanline_overlay(height: int) -> str:
    if not theme.SCANLINES:
        return ""
    return (
        f'  <rect width="{theme.WIDTH}" height="{height}"\n'
        f'        fill="url(#scanlines)" pointer-events="none"/>'
    )


def _build_cursor(x: float, y: float) -> str:
    if not theme.CURSOR_BLINK:
        return ""
    return (
        f'  <rect x="{x}" y="{y - theme.CURSOR_HEIGHT + 3}"\n'
        f'        width="{theme.CURSOR_WIDTH}" height="{theme.CURSOR_HEIGHT}"\n'
        f'        fill="{theme.CURSOR_COLOR}">\n'
        f'    <animate attributeName="opacity"\n'
        f'             values="1;1;0;0" dur="1.2s"\n'
        f'             repeatCount="indefinite"/>\n'
        f'  </rect>'
    )


# ═══════════════════════════════════════════════════════════
#  Main Builder
# ═══════════════════════════════════════════════════════════

def build_terminal(
    title: str,
    body: str,
    command: str | None = None,
    chrome: bool = True,
) -> str:
    """
    Build a complete SVG terminal panel.
    """
    parsed = _parse_lines(body)
    label_width = _compute_label_width(parsed)
    bar_label_width = _compute_bar_label_width(parsed)
    has_pipeline = any(l["type"] == "pipeline" for l in parsed)

    # ── Calculate height ────────────────────────────────────
    total_lines = len(parsed)
    for l in parsed:
        if l["type"] == "pipeline":
            total_lines += 1          # pipelines take 2x line height
    if command:
        total_lines += 2              # prompt + blank after prompt

    content_height = total_lines * theme.LINE_HEIGHT

    if chrome:
        height = theme.HEADER_HEIGHT + theme.PADDING * 2 + content_height + 8
    else:
        height = theme.PADDING * 2 + content_height + 8

    svg = []

    # ── SVG root ────────────────────────────────────────────
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg"'
        f' width="{theme.WIDTH}" height="{height}"'
        f' viewBox="0 0 {theme.WIDTH} {height}">'
    )

    # ── Defs ────────────────────────────────────────────────
    svg.append(_build_defs(has_pipeline))

    # ── Background & Grid & Rain ────────────────────────────
    svg.append(
        f'  <rect x="1" y="1" rx="{theme.RADIUS}" ry="{theme.RADIUS}"'
        f' width="{theme.WIDTH - 2}" height="{height - 2}"'
        f' fill="{theme.BACKGROUND}" stroke="{theme.BORDER}" stroke-width="1"/>'
    )
    svg.append(f'  <rect x="1" y="1" rx="{theme.RADIUS}" ry="{theme.RADIUS}" width="{theme.WIDTH - 2}" height="{height - 2}" fill="url(#grid)" pointer-events="none"/>')
    svg.append(_build_matrix_rain(theme.WIDTH, height))

    # ── HUD Brackets ────────────────────────────────────────
    svg.append(_build_hud_elements(theme.WIDTH, height, chrome))


    # ── Chrome: header bar + buttons + title ────────────────
    if chrome:
        # Clipped header for rounded top corners
        svg.append(
            f'  <clipPath id="headerClip">'
            f'<rect width="{theme.WIDTH}" height="{theme.HEADER_HEIGHT}"'
            f' rx="{theme.RADIUS}" ry="{theme.RADIUS}"/></clipPath>'
        )
        svg.append(
            f'  <rect width="{theme.WIDTH}" height="{theme.HEADER_HEIGHT}"'
            f' fill="{theme.HEADER_BG}" clip-path="url(#headerClip)"/>'
        )
        # Fill gap below header's rounded corners
        svg.append(
            f'  <rect y="{theme.HEADER_HEIGHT - theme.RADIUS}"'
            f' width="{theme.WIDTH}" height="{theme.RADIUS}"'
            f' fill="{theme.HEADER_BG}"/>'
        )
        # Header border line
        svg.append(
            f'  <line x1="0" y1="{theme.HEADER_HEIGHT}" x2="{theme.WIDTH}"'
            f' y2="{theme.HEADER_HEIGHT}" stroke="{theme.BORDER}" stroke-width="1"/>'
        )

        # Traffic light buttons
        for color, cx in [(theme.BUTTON_RED, 20), (theme.BUTTON_YELLOW, 40), (theme.BUTTON_GREEN, 60)]:
            svg.append(
                f'  <circle cx="{cx}" cy="{theme.HEADER_HEIGHT // 2}"'
                f' r="6" fill="{color}"/>'
            )

        # Title text
        svg.append(
            f'  <text x="{theme.WIDTH // 2}" y="{theme.HEADER_HEIGHT // 2 + 4}"'
            f' fill="{theme.TITLE_COLOR}" font-family="{theme.FONT_FAMILY}"'
            f' font-size="{theme.TITLE_FONT_SIZE}" text-anchor="middle">'
            f'{escape(title)}</text>'
        )

    # ── Content area ────────────────────────────────────────
    glow = ' filter="url(#glow)"' if theme.CRT_GLOW else ""
    svg.append(f'  <g{glow}>')

    x = theme.PADDING
    y = (theme.HEADER_HEIGHT + theme.PADDING + theme.FONT_SIZE) if chrome \
        else (theme.PADDING + theme.FONT_SIZE)

    # Optional command prompt
    if command:
        prompt_text = f"root@dattanirjhar:~# {command}"
        svg.append(
            f'    <text x="{x}" y="{y}" fill="{theme.PROMPT}"'
            f' font-family="{theme.FONT_FAMILY}" font-size="{theme.FONT_SIZE}">'
            f'{escape(prompt_text)}</text>'
        )
        y += theme.LINE_HEIGHT * 2   # prompt + blank

    last_x = x
    last_y = y

    # ── Render each line ────────────────────────────────────
    for line in parsed:

        # blank
        if line["type"] == "blank":
            y += theme.LINE_HEIGHT
            continue

        # divider
        if line["type"] == "divider":
            dy = y - theme.FONT_SIZE // 2 + 2
            svg.append(
                f'    <line x1="{x}" y1="{dy}" x2="{theme.WIDTH - theme.PADDING}"'
                f' y2="{dy}" stroke="{theme.COMMENT}" stroke-width="1"'
                f' stroke-dasharray="4,6" opacity="0.5"/>'
            )
            y += theme.LINE_HEIGHT
            continue

        # label (key :: value)
        if line["type"] == "label":
            extra = line["extra"]
            padded = extra["key"].ljust(label_width)
            svg.append(
                f'    <text x="{x}" y="{y}"'
                f' font-family="{theme.FONT_FAMILY}" font-size="{theme.FONT_SIZE}">'
                f'<tspan fill="{theme.MUTED}">{padded}</tspan>'
                f'<tspan fill="{theme.TEXT}">{extra["value"]}</tspan></text>'
            )
            last_x = x + (len(padded) + len(extra["value"])) * theme.CHAR_WIDTH
            last_y = y
            y += theme.LINE_HEIGHT
            continue

        # ── @bar ── horizontal skill meter ──────────────────
        if line["type"] == "bar":
            extra = line["extra"]
            label = extra["label"]
            pct = extra["pct"]

            # Label
            padded = label.ljust(bar_label_width)
            svg.append(
                f'    <text x="{x}" y="{y}" fill="{theme.MUTED}"'
                f' font-family="{theme.FONT_FAMILY}" font-size="{theme.FONT_SIZE}">'
                f'{padded}</text>'
            )

            # Track + fill
            bar_x = x + bar_label_width * theme.CHAR_WIDTH + 8
            bar_y = y - theme.BAR_HEIGHT + 1
            bar_w = theme.WIDTH - bar_x - theme.PADDING - 48
            fill_w = bar_w * (pct / 100)

            # Track background
            svg.append(
                f'    <rect x="{bar_x}" y="{bar_y}" width="{bar_w}"'
                f' height="{theme.BAR_HEIGHT}" rx="{theme.BAR_RADIUS}"'
                f' fill="{theme.BAR_TRACK}"/>'
            )
            # Filled portion
            if fill_w > 0:
                svg.append(
                    f'    <rect x="{bar_x}" y="{bar_y}" width="{fill_w:.1f}"'
                    f' height="{theme.BAR_HEIGHT}" rx="{theme.BAR_RADIUS}"'
                    f' fill="{theme.TEXT}" opacity="0.85"/>'
                )
            # Percentage
            pct_x = bar_x + bar_w + 8
            svg.append(
                f'    <text x="{pct_x}" y="{y}" fill="{theme.COMMENT}"'
                f' font-family="{theme.FONT_FAMILY}" font-size="{theme.FONT_SIZE - 1}">'
                f'{pct}%</text>'
            )

            last_x = pct_x + 30
            last_y = y
            y += theme.LINE_HEIGHT
            continue

        # ── @pipeline ── horizontal flow diagram ────────────
        if line["type"] == "pipeline":
            steps = line["extra"]["steps"]
            n = len(steps)

            avail = theme.WIDTH - theme.PADDING * 2
            gap = theme.PIPE_ARROW_GAP
            box_w = (avail - (n - 1) * gap) / n
            box_h = theme.PIPE_BOX_H
            step_w = box_w + gap
            box_y = y - 14

            for i, step in enumerate(steps):
                bx = x + i * step_w

                # Box
                svg.append(
                    f'    <rect x="{bx:.1f}" y="{box_y}" width="{box_w:.1f}"'
                    f' height="{box_h}" rx="{theme.PIPE_BOX_R}"'
                    f' fill="{theme.HEADER_BG}" stroke="{theme.BORDER}"/>'
                )
                # Text centered in box
                tx = bx + box_w / 2
                svg.append(
                    f'    <text x="{tx:.1f}" y="{y + 2}" fill="{theme.TEXT}"'
                    f' font-family="{theme.FONT_FAMILY}"'
                    f' font-size="{theme.FONT_SIZE - 2}"'
                    f' text-anchor="middle">{step}</text>'
                )
                # Arrow to next box
                if i < n - 1:
                    ax1 = bx + box_w + 2
                    ax2 = bx + step_w - 2
                    ay = box_y + box_h / 2
                    svg.append(
                        f'    <line x1="{ax1:.1f}" y1="{ay:.1f}"'
                        f' x2="{ax2:.1f}" y2="{ay:.1f}"'
                        f' stroke="{theme.COMMENT}" stroke-width="1.5"'
                        f' marker-end="url(#arrow)"/>'
                    )

            last_x = x + (n - 1) * step_w + box_w
            last_y = y
            y += theme.LINE_HEIGHT * 2    # pipelines take double height
            continue

        # ── All other types (text, prompt, comment, etc.) ───
        svg.append(
            f'    <text x="{x}" y="{y}" fill="{line["color"]}"'
            f' font-family="{theme.FONT_FAMILY}" font-size="{theme.FONT_SIZE}">'
            f'{line["text"]}</text>'
        )
        last_x = x + len(line["text"]) * theme.CHAR_WIDTH
        last_y = y
        y += theme.LINE_HEIGHT

    svg.append("  </g>")

    # ── Scanlines overlay ───────────────────────────────────
    svg.append(_build_scanline_overlay(height))

    # ── Blinking cursor ─────────────────────────────────────
    svg.append(_build_cursor(last_x + 4, last_y))

    svg.append("</svg>")

    return "\n".join(svg)
