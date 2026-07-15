"""
Theme registry for Terminal Profile Engine.
"""

from .base import Theme
from .matrix import MatrixTheme
from .ghost import GhostTheme
from .cyberpunk import CyberpunkTheme
from .synthwave import SynthwaveTheme
from .crt import CRTTheme

_REGISTRY = {
    "base": Theme,
    "matrix": MatrixTheme,
    "ghost": GhostTheme,
    "cyberpunk": CyberpunkTheme,
    "synthwave": SynthwaveTheme,
    "crt": CRTTheme,
}

def get_theme(name: str) -> type[Theme]:
    """Return the theme class for the given name, falling back to base."""
    return _REGISTRY.get(name.lower(), Theme)
