from .base import Theme

class CyberpunkTheme(Theme):
    """Cyberpunk 2077 — Neon colors, corporate dystopia, high contrast."""
    NAME = "cyberpunk"
    LABEL = "Cyberpunk"

    BACKGROUND      = "#0F0F1A"
    HEADER_BG       = "#161622"
    BORDER          = "#FCEE09"      # Cyberpunk yellow

    TEXT            = "#00F0FF"      # Cyan
    PROMPT          = "#FCEE09"      # Yellow
    MUTED           = "#FF003C"      # Pinkish Red
    COMMENT         = "#5C5C77"
    HIGHLIGHT       = "#FCEE09"
    SUCCESS         = "#00F0FF"
    WARNING         = "#FCEE09"
    ERROR           = "#FF003C"
    TITLE_COLOR     = "#00F0FF"
    CURSOR_COLOR    = "#FCEE09"

    BUTTON_RED      = "#FF003C"
    BUTTON_YELLOW   = "#FCEE09"
    BUTTON_GREEN    = "#00F0FF"

    BAR_TRACK       = "#1A1A2B"

    CRT_GLOW        = True
    GLOW_STD_DEV    = 1.5
    SCANLINES       = False
