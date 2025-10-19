import yt_dlp
import os
import sys

# Import resource_path robustly so the module works when run from `src/` or
# from project root. Try the most common import paths, then fall back to a
# local implementation that computes paths relative to the repository.
try:
    # when running with CWD = src/
    from utils.resource import resource_path
except Exception:
    try:
        # when running with project root on sys.path
        from src.utils.resource import resource_path
    except Exception:
        # fallback: local implementation similar to utils.resource.resource_path
        def resource_path(rel_path: str) -> str:
            if getattr(sys, "frozen", False):
                base_path = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
            else:
                base_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "..")
                )
            return os.path.join(base_path, rel_path)


# Default ffmpeg path (used in development). For bundled app, resource_path will locate the
# provided binary under 'bin/ffmpeg.exe'.
FFMPEG_PATH = r"C:\\ffmpeg\\bin\\ffmpeg.exe"


class Downloader:
    def __init__(self, ffmpegPath: str = FFMPEG_PATH):
        # prefer provided path, but when frozen use bundled binary
        self.ffmpeg_path = ffmpegPath
        if getattr(sys, "frozen", False):
            # when bundled we expect ffmpeg to be under bin/ffmpeg.exe inside the bundle
            bundled = resource_path(os.path.join("ffmpeg/bin", "ffmpeg.exe"))
            if os.path.exists(bundled):
                self.ffmpeg_path = bundled

    # Function to Download Videos
    def downloadVideo(self, url: str, save_path: str, resolution: int):
        # Defining Options/Arguments for Downloading
        ydl_opts: dict = {
            "format": f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
            "ffmpeg_location": self.ffmpeg_path,
        }

        # Actual Downloading
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    # Function to Download Playlist
    def downloadPlaylist(self, url: str, save_path: str, resolution: int):
        ydl_opts = {
            "format": f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]",
            "merge_output_format": "mp4",
            "outtmpl": os.path.join(
                save_path, "%(playlist_title)s", "%(title)s.%(ext)s"
            ),
            "noplaylist": False,
            "ffmpeg_location": self.ffmpeg_path,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])


def main():
    ytDown = Downloader()
    ytDown.downloadPlaylist("https://www.youtube.com/playlist?list=PLKZJAqRtlIlG58B1cLWYeziIkbPJmDilX", os.curdir, 720)


if __name__ == "__main__":
    main()
