import sys
import os


def resource_path(rel_path: str) -> str:
    """Return absolute path to resource, working for dev and PyInstaller onedir/onefile.

    rel_path is relative to project root (e.g. 'assets/icon.png' or 'bin/ffmpeg.exe').
    """
    if getattr(sys, 'frozen', False):
        # When frozen by PyInstaller: _MEIPASS for onefile; for onedir use dirname of executable
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # project root is two levels up from this file (src/utils -> project root)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    return os.path.join(base_path, rel_path)
