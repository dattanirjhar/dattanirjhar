"""
Base theme — every visual token for the Terminal Profile Engine.

Subclass this and override colors/effects to create new themes.
"""


class Theme:
    """Base theme with all configurable design tokens."""

    # ── Identity ────────────────────────────────────────────
    NAME = "base"
    LABEL = "Base"

    # ── Dimensions ──────────────────────────────────────────
    WIDTH           = 900
    PADDING         = 28
    LINE_HEIGHT     = 28
    HEADER_HEIGHT   = 42
    RADIUS          = 12

    # ── Chrome ──────────────────────────────────────────────
    BACKGROUND      = "#0D1117"
    HEADER_BG       = "#161B22"
    BORDER          = "#30363D"

    # ── Text Colors ─────────────────────────────────────────
    TEXT            = "#00FF41"
    PROMPT          = "#39FF14"
    MUTED           = "#7EE787"
    COMMENT         = "#6E7681"
    HIGHLIGHT       = "#58A6FF"
    SUCCESS         = "#3FB950"
    WARNING         = "#F0883E"
    ERROR           = "#FF7B72"
    TITLE_COLOR     = "#8B949E"
    CURSOR_COLOR    = "#00FF41"

    # ── Traffic Light Buttons ───────────────────────────────
    BUTTON_RED      = "#FF5F56"
    BUTTON_YELLOW   = "#FFBD2E"
    BUTTON_GREEN    = "#27C93F"

    # ── Typography ──────────────────────────────────────────
    FONT_FAMILY     = "JetBrains Mono, Cascadia Code, Fira Code, Consolas, monospace"
    FONT_SIZE       = 14
    TITLE_FONT_SIZE = 13
    CHAR_WIDTH      = 8.4

    # ── CRT Effects ─────────────────────────────────────────
    CRT_GLOW        = True
    GLOW_STD_DEV    = 2
    SCANLINES       = True
    SCANLINE_GAP    = 4
    SCANLINE_OPACITY = 0.06
    CURSOR_BLINK    = True
    CURSOR_WIDTH    = 9
    CURSOR_HEIGHT   = 16

    # ── Bar Charts ──────────────────────────────────────────
    BAR_HEIGHT      = 10
    BAR_RADIUS      = 4
    BAR_TRACK       = "#21262D"

    # ── Pipeline Diagrams ───────────────────────────────────
    PIPE_BOX_H      = 28
    PIPE_BOX_R      = 6
    PIPE_ARROW_GAP  = 22
