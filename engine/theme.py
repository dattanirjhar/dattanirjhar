"""
theme.py — The definitive Terminal Profile Engine design tokens.

Integrates all hacker aesthetics:
- Retro computing & UNIX philosophy (monospaced, CLI-first)
- Green phosphor terminals & CRT monitors (glow, scanlines, amber/green)
- Cyberpunk & Neon colors (cyan highlights, magenta alerts)
- Ghost in the Shell HUDs (corner brackets, grids, minimal data design)
- The Matrix (digital rain overlays)
"""

# ── Dimensions ──────────────────────────────────────────
WIDTH           = 900
PADDING         = 32
LINE_HEIGHT     = 28
HEADER_HEIGHT   = 42
RADIUS          = 8    # Sharper corners for a more hardware/HUD feel

# ── Chrome & Background ─────────────────────────────────
BACKGROUND      = "#050A05"  # Deep CRT black/green
HEADER_BG       = "#0A140A"
BORDER          = "#1A331A"
GRID_COLOR      = "#00FF41"
GRID_OPACITY    = 0.03

# ── Text Colors ─────────────────────────────────────────
TEXT            = "#00FF41"  # Primary: Matrix Green
PROMPT          = "#00F0FF"  # Cyberpunk Cyan
MUTED           = "#008F11"  # Dim Green
COMMENT         = "#4A5568"  # Slate grey
HIGHLIGHT       = "#FCEE09"  # Cyberpunk Yellow
SUCCESS         = "#00FF41"
WARNING         = "#FFB320"  # Neon Orange
ERROR           = "#FF003C"  # Neon Magenta/Red
TITLE_COLOR     = "#00F0FF"
CURSOR_COLOR    = "#00FF41"

# ── HUD & Chrome Elements ───────────────────────────────
BUTTON_RED      = "#FF003C"
BUTTON_YELLOW   = "#FCEE09"
BUTTON_GREEN    = "#00FF41"

# ── Typography ──────────────────────────────────────────
FONT_FAMILY     = "Fira Code, JetBrains Mono, monospace"
FONT_SIZE       = 14
TITLE_FONT_SIZE = 13
CHAR_WIDTH      = 8.4

# ── CRT Effects ─────────────────────────────────────────
CRT_GLOW        = True
GLOW_STD_DEV    = 2.0

SCANLINES       = True
SCANLINE_GAP    = 4
SCANLINE_OPACITY= 0.08

CURSOR_BLINK    = True
CURSOR_WIDTH    = 9
CURSOR_HEIGHT   = 16

# ── Bar Charts ──────────────────────────────────────────
BAR_HEIGHT      = 10
BAR_RADIUS      = 2
BAR_TRACK       = "#0A1A0A"

# ── Pipeline Diagrams ───────────────────────────────────
PIPE_BOX_H      = 28
PIPE_BOX_R      = 2
PIPE_ARROW_GAP  = 22
