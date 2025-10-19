# Tube Queue - Modern Youtube Downloader

Small desktop GUI to download YouTube videos/playlists using yt-dlp and ffmpeg, built with CustomTkinter.

## Contents
- `src/` - application source code
	- `app.py` - application entry that protects single-instance PID and starts the GUI
	- `gui/` - GUI code (main window and widgets)
	- `core/` - core logic (downloader using `yt_dlp`/`ffmpeg`)
- `assets/` - images and static assets used by the GUI
- `tests/` - unit tests for GUI and downloader logic
- `requirements.txt` - Python dependencies (keep this updated)

## Requirements
- Python 3.10+ (this repository has been used with Python 3.12 in the workspace)
- pip and a virtual environment (recommended)
- ffmpeg installed for merging audio/video and for format conversion

Optional (but recommended for running GUI and tests):
- Pillow (`pip install pillow`) — if you use non-PNG icon images (JPEG etc.)
- `pytest` for running tests and `pytest-mock` if tests use the `mocker` fixture

## Quick setup (Windows / PowerShell)
1. Create and activate a venv (if not already created):

```powershell
# from project root
python -m venv .\venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Optional) Install extras used in tests or for better image handling:

```powershell
pip install pillow pytest pytest-mock
```

3. Configure `ffmpeg` path if you don't have it in PATH or want to use a specific binary. Edit `src/core/main_worker.py` and set `FFMPEG_PATH` to your ffmpeg executable path, for example `C:\ffmpeg\bin\ffmpeg.exe`.

## Run the application
The code is runnable in two modes: development (run from source) and packaged (built with PyInstaller).

Development (recommended while editing): run from the project root and invoke the `src` entry script:

```powershell
# from project root
Set-Location -Path 'D:\...\Youtube Downloader'
.\venv\Scripts\Activate.ps1
python src\app.py
```

Packaging / running the built app:
- The repository contains a PyInstaller spec `tubequeue.spec` that builds an onedir bundle named `TubeQueue`.
- If you bundle ffmpeg, place the ffmpeg binary at `ffmpeg/bin/ffmpeg.exe` (the spec expects `ffmpeg/bin/ffmpeg.exe`) before building.
- Build with the spec (venv activated):

```powershell
Set-Location -Path 'D:\...\Youtube Downloader'
.\venv\Scripts\Activate.ps1
pyinstaller --clean tubequeue.spec
```

- After a successful onedir build, run the EXE inside the created folder (do NOT run the stray top-level EXE in `dist\`):

```powershell
& ".\dist\TubeQueue\TubeQueue.exe"
```

The app uses a PID file (`tube_queue_app.pid`) to prevent multiple instances.

## Tests
- Run pytest from the project root (recommended):

```powershell
# from project root
pytest
# or run a single test file
pytest tests/test_app_gui.py -q
```

Notes about tests:
- Some tests instantiate GUI classes. Creating a real `Tk` instance requires a working Tcl/Tk runtime. If your Python environment can't find `init.tcl` you'll see a `_tkinter.TclError`. To avoid this in unit tests:
	- Either run tests in an environment that has Tcl/Tk available (install `tk` via conda or use a Python that includes Tk), or
	- Prefer stubbing/mocking GUI modules (the test suite can inject a lightweight `customtkinter` stub) so tests don't construct a real window.
- If tests use the `mocker` fixture, install `pytest-mock` or convert tests to use `monkeypatch`/`unittest.mock`.

Tip: The code includes a small helper `src/utils/resource.py` (`resource_path`) that your application and the PyInstaller bundle use to locate bundled assets and binaries (assets, `bin/ffmpeg.exe`) both in development and when frozen. Tests or custom scripts can reuse this helper to find resources reliably.

## Common issues & troubleshooting

- "Can't find a usable init.tcl" (TclError):
	- Cause: The Python/Tkinter runtime cannot find Tcl library files. This happens with mixed installations (conda/venv) or missing Tcl/Tk on the system.
	- Fix: Use a Python interpreter that includes Tcl/Tk or install `tk` (e.g., `conda install tk`) or run tests with the GUI module mocked.

- Icon image errors like `couldn't recognize data in image file` or `can't use "pyimageN" as iconphoto: not a photo image`:
	- Use Pillow's `Image` + `ImageTk.PhotoImage` for non-PNG images and ensure you keep a reference to the PhotoImage object on the instance (store it as `self._icon_image`) so Python's GC doesn't collect it.
	- Example (in GUI init):

```python
from PIL import Image, ImageTk
img = Image.open(path_to_icon)
photo = ImageTk.PhotoImage(img)
self.iconphoto(True, photo)
# keep a reference
self._icon_image = photo
```

- `ffmpeg` issues: ensure `ffmpeg` is installed and `ffmpeg_location` passed to `yt_dlp` points to the correct executable.
	- If you are bundling ffmpeg with the provided spec, put the binary at `ffmpeg/bin/ffmpeg.exe` before building; at runtime the bundled app will prefer the bundled `bin/ffmpeg.exe`.

Packaging-specific notes:
- If you see an error like "Failed to load Python DLL '...dist\_internal\python312.dll'": make sure you run the EXE inside the onedir folder (for our onedir build the correct EXE is `dist\TubeQueue\TubeQueue.exe`). A stray `dist\TubeQueue.exe` at the root is not the proper launcher for the `dist\TubeQueue\_internal` folder.
- If the built exe fails to start because of missing Tcl/Tk files (init.tcl), build with a CPython interpreter that has a working Tk runtime (Anaconda sometimes requires extra steps).

## Project structure

```
README.md
requirements.txt
assets/
src/
	app.py
	gui/
		app_gui.py
	core/
		main_worker.py
tests/
	test_app_gui.py
	test_downloader.py
```

## Contributing
- Keep tests green. If you add runtime dependencies, add them to `requirements.txt`.
- For GUI changes, prefer adding logic tests that can run without a real GUI (using stubs/mocks) and keep integration tests that actually open windows separate and optional.

## Authors
Muhammad Abish Baig

## License
[MIT](LICENSE)