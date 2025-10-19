import pytest
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
from src.gui.app_gui import TubeQueue
from tkinter import TclError


@pytest.fixture(scope="function")
def tubeQueue():
    app = TubeQueue()
    yield app
    try:
        app.destroy()  # Tear Down Phase
    except TclError:
        pass  # ignore if already destroyed


def test_mainWindow(tubeQueue: TubeQueue):
    # should NOT raise since all steps are valid
    try:
        tubeQueue._createMainWindow()
    except TclError:
        pytest.fail("_createMainWindow should not raise TclError for valid setup")


def test_createFrames(tubeQueue):
    tubeQueue._createMainWindow()
    result = tubeQueue._createFrames()
    assert result is None  # Means All Frames are Created
    assert hasattr(
        tubeQueue, "sidebarFrame"
    )  # Checks whether an Instance holds an named attribute/widget
    assert hasattr(
        tubeQueue, "mainbarFrame"
    )  # Checks whether an Instance holds an named attribute/widget
    assert hasattr(
        tubeQueue, "bodyFrame"
    )  # Checks whether an Instance holds an named attribute/widget


def test_sidebarWidgets(tubeQueue):
    tubeQueue._createMainWindow()
    tubeQueue._createFrames()
    tubeQueue._sidebar_widgets()

    assert hasattr(tubeQueue, "output_label")
    assert tubeQueue.output_label.cget("text") == "Output Folder"

    assert hasattr(tubeQueue, "output_folder_entry")

    
