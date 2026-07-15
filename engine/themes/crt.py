from .base import Theme

class CRTTheme(Theme):
    """Classic CRT — Retro amber monitor, warm and nostalgic."""
    NAME = "crt"
    LABEL = "CRT"

    BACKGROUND      = "#1C140D"
    HEADER_BG       = "#261A10"
    BORDER          = "#8C5820"

    TEXT            = "#FFB000"      # Bright Amber
    PROMPT          = "#FFC745"      # Light Amber
    MUTED           = "#CC8C00"      # Dim Amber
    COMMENT         = "#664600"      # Dark Amber
    HIGHLIGHT       = "#FFE08A"
    SUCCESS         = "#FFB000"
    WARNING         = "#FFC745"
    ERROR           = "#FF3300"
    TITLE_COLOR     = "#CC8C00"
    CURSOR_COLOR    = "#FFB000"

    BUTTON_RED      = "#8C3A20"
    BUTTON_YELLOW   = "#8C6A20"
    BUTTON_GREEN    = "#6A8C20"

    BAR_TRACK       = "#332418"

    CRT_GLOW        = True
    GLOW_STD_DEV    = 2.2
    SCANLINES       = True
    SCANLINE_GAP    = 3
    SCANLINE_OPACITY= 0.1
