import platform

_SYSTEM = platform.system()

VERSION = "2.0.0"
APP_NAME = "Keyboard Emulator"

COLORS = {
    "bg": "#000000",
    "bg2": "#0d0d0d",
    "bg3": "#1a1a1a",
    "fg": "#ffffff",
    "fg2": "#aaaaaa",
    "accent": "#00e5ff",
    "accent_bg": "#003d44",
    "green": "#00e676",
    "yellow": "#ffab00",
    "red": "#ff1744",
}

DEFAULTS = {
    "delay": "3",
    "speed": "0.05",
    "width": 520,
    "text_height": 10,
}


def get_font():
    if _SYSTEM == "Darwin":
        return {"title": ("SF Pro Display", 16, "bold"), "body": ("SF Pro Text", 12), "mono": ("Menlo", 11)}
    elif _SYSTEM == "Windows":
        return {"title": ("Segoe UI", 16, "bold"), "body": ("Segoe UI", 12), "mono": ("Consolas", 11)}
    else:
        return {"title": ("Ubuntu", 16, "bold"), "body": ("Ubuntu", 12), "mono": ("DejaVu Sans Mono", 11)}


FONTS = get_font()
PAD = 16
