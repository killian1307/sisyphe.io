# -*- coding: utf-8 -*-
"""Cross-platform UI font resolution.

The game uses one font family everywhere (stored on :data:`context.FONT`). Any
``.ttf`` / ``.otf`` dropped in ``assets/fonts/`` is bundled with the game and
used on every platform — no system install needed — and is preferred over the
built-in fonts so a font you ship "just works" identically everywhere.

Two-step usage, because the order matters on macOS (Tk only sees a font that was
registered *before* the Tk root is created):

    bundled = fonts.register(assets_dir)   # call BEFORE creating the Tk root
    family  = fonts.resolve(bundled)       # call AFTER the Tk root exists

Registration uses the OS font APIs via ctypes (CoreText on macOS, GDI on
Windows, fontconfig on Linux) — no extra dependency.
"""
import glob
import os
import sys

# Built-in fallbacks, only used when no font is bundled in assets/fonts/.
LEGACY = "Small Fonts"             # the original Windows design font
FALLBACKS = ["Tahoma", "Verdana"]  # available on both macOS and Windows


def _register_macos(path):
    import ctypes
    from ctypes import util
    core_text = ctypes.cdll.LoadLibrary(util.find_library('CoreText'))
    core_foundation = ctypes.cdll.LoadLibrary(util.find_library('CoreFoundation'))
    core_foundation.CFStringCreateWithCString.restype = ctypes.c_void_p
    core_foundation.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
    core_foundation.CFURLCreateWithFileSystemPath.restype = ctypes.c_void_p
    core_foundation.CFURLCreateWithFileSystemPath.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_bool]
    core_text.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool
    core_text.CTFontManagerRegisterFontsForURL.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    cfstr = core_foundation.CFStringCreateWithCString(None, os.path.abspath(path).encode('utf-8'), 0x08000100)
    cfurl = core_foundation.CFURLCreateWithFileSystemPath(None, cfstr, 0, False)  # kCFURLPOSIXPathStyle
    core_text.CTFontManagerRegisterFontsForURL(cfurl, 1, None)  # kCTFontManagerScopeProcess


def _register_windows(path):
    import ctypes
    FR_PRIVATE = 0x10
    ctypes.windll.gdi32.AddFontResourceExW(ctypes.c_wchar_p(os.path.abspath(path)), FR_PRIVATE, 0)


def _register_linux(path):
    import ctypes
    from ctypes import util
    fontconfig = ctypes.cdll.LoadLibrary(util.find_library('fontconfig'))
    fontconfig.FcConfigAppFontAddFile.restype = ctypes.c_int
    fontconfig.FcConfigAppFontAddFile.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    fontconfig.FcConfigAppFontAddFile(None, os.path.abspath(path).encode('utf-8'))


def _register_file(path):
    try:
        if sys.platform == 'win32':
            _register_windows(path)
        elif sys.platform == 'darwin':
            _register_macos(path)
        else:
            _register_linux(path)
        return True
    except Exception:
        return False


def _family_name(path):
    """Read the font's real family name from its name table (via Pillow)."""
    try:
        from PIL import ImageFont
        return ImageFont.truetype(path).getname()[0]
    except Exception:
        return None


def register(assets_dir):
    """Register every font in ``assets/fonts/``. Returns their family names.

    Call this BEFORE creating the Tk root so Tk can see the fonts on macOS.
    """
    fonts_dir = os.path.join(assets_dir, 'assets', 'fonts')
    families = []
    for path in sorted(glob.glob(os.path.join(fonts_dir, '*.ttf')) + glob.glob(os.path.join(fonts_dir, '*.otf'))):
        if _register_file(path):
            family = _family_name(path)
            if family and family not in families:
                families.append(family)
    return families


def resolve(bundled):
    """Pick the UI font family. Bundled fonts win on every platform.

    Call this AFTER the Tk root exists. Sets module :data:`FAMILY` too.
    """
    global FAMILY
    try:
        import tkinter.font as tkfont
        available = set(tkfont.families())
    except Exception:
        available = set()

    for family in list(bundled) + [LEGACY] + FALLBACKS:
        if family in available:
            FAMILY = family
            return family

    try:
        import tkinter.font as tkfont
        FAMILY = tkfont.nametofont("TkDefaultFont").actual("family")
    except Exception:
        FAMILY = LEGACY
    return FAMILY


FAMILY = LEGACY
