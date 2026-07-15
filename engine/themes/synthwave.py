from .base import Theme

class SynthwaveTheme(Theme):
    """Ready Player One / Synthwave — Gamified UI, purple & pink retrowave."""
    NAME = "synthwave"
    LABEL = "Synthwave"

    BACKGROUND      = "#140A26"
    HEADER_BG       = "#1F1235"
    BORDER          = "#D926FF"      # Bright Purple

    TEXT            = "#FF2A6D"      # Neon Pink
    PROMPT          = "#05D9E8"      # Cyan
    MUTED           = "#B37DDB"
    COMMENT         = "#5A3A7E"
    HIGHLIGHT       = "#01FFE5"      # Aquamarine
    SUCCESS         = "#05D9E8"
    WARNING         = "#FFB320"      # Neon Orange
    ERROR           = "#FF2A6D"
    TITLE_COLOR     = "#D926FF"
    CURSOR_COLOR    = "#FF2A6D"

    BUTTON_RED      = "#FF2A6D"
    BUTTON_YELLOW   = "#FFB320"
    BUTTON_GREEN    = "#05D9E8"

    BAR_TRACK       = "#2D1B4E"

    CRT_GLOW        = True
    GLOW_STD_DEV    = 3.0
    SCANLINES       = True
    SCANLINE_OPACITY= 0.05
