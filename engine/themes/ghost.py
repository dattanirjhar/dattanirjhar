from .base import Theme

class GhostTheme(Theme):
    """Ghost in the Shell — Minimalist futuristic interfaces, cyan HUDs."""
    NAME = "ghost"
    LABEL = "Ghost"

    BACKGROUND      = "#05080F"
    HEADER_BG       = "#08101C"
    BORDER          = "#1A2F4C"

    TEXT            = "#E0F2FE"      # off-white / light cyan
    PROMPT          = "#38BDF8"      # light blue
    MUTED           = "#7DD3FC"      # sky blue
    COMMENT         = "#334155"      # slate
    HIGHLIGHT       = "#0EA5E9"      # bright cyan
    SUCCESS         = "#38BDF8"
    WARNING         = "#FACC15"
    ERROR           = "#F87171"
    TITLE_COLOR     = "#7DD3FC"
    CURSOR_COLOR    = "#38BDF8"

    BUTTON_RED      = "#1E293B"
    BUTTON_YELLOW   = "#334155"
    BUTTON_GREEN    = "#475569"

    BAR_TRACK       = "#0F172A"

    CRT_GLOW        = False
    SCANLINES       = True
    SCANLINE_OPACITY= 0.04
