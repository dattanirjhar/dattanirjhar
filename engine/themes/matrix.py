from .base import Theme

class MatrixTheme(Theme):
    """The Matrix — Green phosphor terminals, code rain, hacking."""
    NAME = "matrix"
    LABEL = "Matrix"

    BACKGROUND      = "#000000"
    HEADER_BG       = "#051005"
    BORDER          = "#003300"

    TEXT            = "#00FF41"
    PROMPT          = "#39FF14"
    MUTED           = "#008F11"
    COMMENT         = "#005F00"
    HIGHLIGHT       = "#00FF41"
    SUCCESS         = "#00FF41"
    WARNING         = "#39FF14"
    ERROR           = "#FF0000"
    TITLE_COLOR     = "#008F11"
    CURSOR_COLOR    = "#39FF14"

    BUTTON_RED      = "#003300"
    BUTTON_YELLOW   = "#005F00"
    BUTTON_GREEN    = "#008F11"

    BAR_TRACK       = "#001100"

    CRT_GLOW        = True
    GLOW_STD_DEV    = 2.5
    SCANLINES       = True
    SCANLINE_OPACITY= 0.08
