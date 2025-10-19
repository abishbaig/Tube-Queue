import pytest
import sys
from pathlib import Path
import yt_dlp

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
from src.core.main_worker import Downloader


@pytest.fixture
def ytDownloader():
    return Downloader()


def test_downloadVideo(mocker):
    # Mock the yt_dlp.YoutubeDL class and its download method
    mock_yt_dlp = mocker.patch("yt_dlp.YoutubeDL")

    # Create a mock instance to replace the real YoutubeDL object
    mock_instance = mock_yt_dlp.return_value

    # Mock the download method to simulate downloading behavior
    mock_instance.download.return_value = None  # or any expected return

    # Now call your function that uses yt_dlp.YoutubeDL internally
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ydl_opts = {}  # pass options as needed

    # Example of using YoutubeDL in your function (to be tested)
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    result = ydl.download([url])

    # Assertions
    mock_yt_dlp.assert_called_once_with(ydl_opts)
    mock_instance.download.assert_called_once_with([url])
