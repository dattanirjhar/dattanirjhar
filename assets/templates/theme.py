"""
theme.py — Design tokens for the 90s hacker terminal SVG generator.

Every visual constant lives here. Change the theme once,
every panel updates on rebuild.
"""

# ── Dimensions ──────────────────────────────────────────────

WIDTH           = 900
PADDING         = 28
LINE_HEIGHT     = 28
HEADER_HEIGHT   = 42
RADIUS          = 12

# ── Colors ──────────────────────────────────────────────────

BACKGROUND      = "#0D1117"
HEADER_BG       = "#161B22"
BORDER          = "#30363D"

TEXT            = "#00FF41"      # primary terminal green
PROMPT          = "#39FF14"      # bright green for prompts
MUTED           = "#7EE787"      # softer green for secondary
COMMENT         = "#6E7681"      # grey for comments / dimmed
HIGHLIGHT       = "#58A6FF"      # blue accent
SUCCESS         = "#3FB950"      # green checkmarks
WARNING         = "#F0883E"      # amber / orange
ERROR           = "#FF7B72"      # red

TITLE_COLOR     = "#8B949E"      # window title bar text
CURSOR_COLOR    = "#00FF41"      # blinking cursor

# macOS traffic-light buttons
BUTTON_RED      = "#FF5F56"
BUTTON_YELLOW   = "#FFBD2E"
BUTTON_GREEN    = "#27C93F"

# ── Typography ──────────────────────────────────────────────

FONT_FAMILY     = "JetBrains Mono, Cascadia Code, Fira Code, Consolas, monospace"
FONT_SIZE       = 14
TITLE_FONT_SIZE = 13
CHAR_WIDTH      = 8.4           # approx width of one monospace char at 14px

# ── CRT Effects ────────────────────────────────────────────

CRT_GLOW        = True          # phosphor glow around text
GLOW_STD_DEV    = 2             # gaussian blur radius
GLOW_OPACITY    = 0.35          # glow layer opacity

SCANLINES       = True          # horizontal CRT scanlines
SCANLINE_GAP    = 4             # px between scanlines
SCANLINE_OPACITY= 0.06          # very subtle

CURSOR_BLINK    = True          # animated block cursor
CURSOR_WIDTH    = 9
CURSOR_HEIGHT   = 16
