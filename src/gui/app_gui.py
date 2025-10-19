import customtkinter as ctk
from PIL import Image, ImageTk
from typing import Optional
from tkinter import TclError, StringVar, filedialog, messagebox
import os
import threading

# import Downloader and resource_path robustly (work whether module is loaded as
# 'src.gui.app_gui' or executed from 'src/')
try:
    from core.main_worker import Downloader
except Exception:
    from src.core.main_worker import Downloader

try:
    # prefer top-level utils if running from src/ dir
    from utils.resource import resource_path
except Exception:
    from src.utils.resource import resource_path


ctk.set_appearance_mode("system")  # Default System-Theme
ctk.set_appearance_mode("dark-blue")  # Default Color Theme comes with the Package


class TubeQueue(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Creating an Instance of the Downloader Class
        self.YTDownloader = Downloader()

        self._createMainWindow()

        # Creating Widgets after Window Configurations
        self._create_widgets()

    # Main Window Configurations
    def _createMainWindow(self) -> Optional[str]:
        try:
            if self:
                # Setting Title of the Main Window
                self.title("Tube Queue")

                # Setting Size of the Main Window
                self.geometry("640x480")

                # Setting Icon (use resource_path so bundled exe can find it)
                try:
                    icon_path = resource_path(os.path.join("assets", "icon.png"))
                    icon_img: Image = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(icon_img)
                    try:
                        self.iconphoto(True, photo)
                    except Exception:
                        pass
                    # keep reference to avoid GC
                    self._icon_image = photo
                except Exception as e:
                    print("icon load error:", e)
                # Setting Resizability Factor
                self.resizable(False, False)
            else:
                raise TclError("Failed to Load Main Window")
        except TclError as e:
            raise e

    # Instantiating Frames
    def _createFrames(self) -> Optional[str]:
        try:
            # Side Bar Frame
            self.sidebarFrame: ctk.CTkFrame = ctk.CTkFrame(self, width=189, height=450)
            # Prevent the sidebar from shrinking to fit its children
            self.sidebarFrame.pack_propagate(False)
            self.sidebarFrame.pack(side="left", padx=10, pady=15, fill="y")
            if self.sidebarFrame.winfo_exists() != True:
                raise TclError("Failed to Create Side Bar Frame")
        except TclError as e:
            raise e

        try:
            # Main Header Bar Frame
            self.mainbarFrame: ctk.CTkFrame = ctk.CTkFrame(self, width=416, height=70)
            self.mainbarFrame.pack_propagate(False)
            self.mainbarFrame.pack(side="top", pady=15, padx=9, fill="x")
            if self.mainbarFrame.winfo_exists() != True:
                raise TclError("Failed to Create Main Bar Frame")
        except TclError as e:
            raise e

        # Main Body Frame
        try:
            self.bodyFrame: ctk.CTkFrame = ctk.CTkFrame(self, width=416, height=352)
            self.bodyFrame.pack_propagate(False)
            self.bodyFrame.pack(side="top", fill="both", padx=9)
            if self.bodyFrame.winfo_exists() != True:
                raise TclError("Failed to Create Body Frame")
        except TclError as e:
            raise e

    # Instantiate a Default Output Folder
    def _createDefaultOutFolder(self):
        # Creating a Default Path for Downloads
        try:
            os.mkdir(f"{os.curdir}/Downloads")
        except FileExistsError:
            pass  # As the Folder Already Exits

        self.defaultPath: str = f"{os.path.abspath(os.curdir)}/Downloads"

    # Change Path Function
    def _changePath(self):
        newFolderPath: str = filedialog.askdirectory(initialdir=self.defaultPath)
        self.defaultPath = newFolderPath
        self.output_folder_entry.configure(
            textvariable=StringVar(value=self.defaultPath)
        )

    # Filling Side Bar with Widgets
    def _sidebar_widgets(self) -> Optional[str]:
        try:
            # Main Text
            self.output_label: ctk.CTkLabel = ctk.CTkLabel(
                master=self.sidebarFrame,
                text="Output Folder",
                font=("Inter", 20),
            )
            self.output_label.pack(pady=33)
        except TclError as e:
            raise e

        self._createDefaultOutFolder()

        try:
            # Output Folder Entry
            self.output_folder_entry: ctk.CTkEntry = ctk.CTkEntry(
                self.sidebarFrame,
                textvariable=StringVar(value=self.defaultPath),
                state="disabled",
            )
            self.output_folder_entry.pack(fill="x", padx=5)
        except TclError as e:
            raise e

        try:
            # Change Path Button
            self.change_path_btn: ctk.CTkButton = ctk.CTkButton(
                self.sidebarFrame,
                text="Browse Path",
                command=self._changePath,
            )
            self.change_path_btn.pack(pady=10)
        except TclError as e:
            raise e

    # Filling Main Bar with Widgets
    def _mainBar_widgets(self) -> Optional[str]:
        try:
            # Setting Logo (use resource_path)
            try:
                logo_path = resource_path(os.path.join("assets", "icon.png"))
                logo = ctk.CTkImage(dark_image=Image.open(logo_path), size=(80, 80))
            except Exception:
                logo = None
            self.logoImg: ctk.CTkLabel = ctk.CTkLabel(
                self.mainbarFrame,
                image=logo,
                text=None,
            )
            self.logoImg.grid(row=0, column=0, padx=10)
        except TclError as e:
            raise e

        try:
            # Main Heading Text
            self.heading_text: ctk.CTkLabel = ctk.CTkLabel(
                self.mainbarFrame,
                font=("Inter", 24, "bold"),
                text="Tube Queue",
            )
            self.heading_text.grid(row=0, column=1, padx=50)
        except TclError as e:
            raise e

    # Main Function for Downloading Video
    def _downloadVideo(
        self, url: str, resolution: int, status_lable: ctk.CTkLabel, btn: ctk.CTkButton
    ):
        if not url:
            messagebox.showerror("Invalid URL", "Please Provide a Correct URL")
            btn.configure(state="normal")
            return
        status_lable.configure(text="Status: Downloading...")
        try:
            self.YTDownloader.downloadVideo(url, self.defaultPath, resolution)
            status_lable.configure(text="Video Downloaded")
            btn.configure(state="normal")
        except Exception as e:
            status_lable.configure(text=f"Error: {str(e)}")

    # Main Function for Downloading Playlist
    def _downloadPlaylist(
        self, url: str, resolution: int, status_lable: ctk.CTkLabel, btn: ctk.CTkButton
    ):
        if not url:
            messagebox.showerror("Invalid URL", "Please Provide a Correct URL")
            btn.configure(state="normal")
            return
        status_lable.configure(text="Status: Downloading...")
        try:
            self.YTDownloader.downloadPlaylist(url, self.defaultPath, resolution)
            status_lable.configure(text="Playlist Downloaded")
            btn.configure(state="normal")
        except Exception as e:
            status_lable.configure(text=f"Error: {str(e)}")
            btn.configure(state="normal")

    # Function to Create a Thread for Downloading a Video
    def _startVideoDownload(
        self,
        link_url: str,
        reso: int,
        status_lable: ctk.CTkLabel,
        btn: ctk.CTkButton,
    ):
        thread = threading.Thread(
            target=self._downloadVideo, args=(link_url, reso, status_lable, btn)
        )
        thread.start()

    # Function to Create a Thread for Downloading a Playlist
    def _startPlaylistDownload(
        self,
        link_url: str,
        reso: int,
        status_lable: ctk.CTkLabel,
        btn: ctk.CTkButton,
    ):
        thread = threading.Thread(
            target=self._downloadPlaylist, args=(link_url, reso, status_lable, btn)
        )
        thread.start()

    # Generic Function for Checking whether to Download a Video or Playlist
    def _checkVidPlay_DownloadOption(
        self,
        callingFrame: str,
        url: str,
        resolution: str,
        status_lable: ctk.CTkLabel,
        btn: ctk.CTkButton,
    ):
        # First Deactivating the Button State
        btn.configure(state="disabled")

        if callingFrame.lower() == "video":
            self._startVideoDownload(url.strip(), int(resolution), status_lable, btn)
        elif callingFrame.lower() == "playlist":
            print("Playlist Selected")
            self._startPlaylistDownload(url.strip(), int(resolution), status_lable, btn)
        else:
            print("No Tab Selected")
            btn.configure(state="normal")

    # Widgets for Video and Playlist Tabs
    def _createVidPlay_widgets(self, link_Of: str, frame: ctk.CTkFrame):
        try:
            # Link Text
            link_text: ctk.CTkLabel = ctk.CTkLabel(frame, text=f"{link_Of} Link")
            link_text.grid(row=0, column=0, padx=10, pady=10)

            # Link Entry
            link_entry: ctk.CTkEntry = ctk.CTkEntry(frame, width=290)
            link_entry.grid(row=0, column=1, padx=10, pady=10)

            # Resolution Text
            reso_text: ctk.CTkLabel = ctk.CTkLabel(frame, text="Resolution")
            reso_text.grid(row=1, column=0, pady=10)

            # Resolution Selector
            reso_option: StringVar = StringVar(value="1080")
            reso_selector: ctk.CTkComboBox = ctk.CTkComboBox(
                frame,
                values=["1080", "720", "480", "360", "144"],
                variable=reso_option,
            )
            reso_selector.grid(row=1, column=1, pady=10)

            # Download Button
            download_btn: ctk.CTkButton = ctk.CTkButton(
                frame,
                text=f"Download {link_Of}",
                command=lambda: self._checkVidPlay_DownloadOption(
                    link_Of, link_entry.get(), reso_option.get(), status, download_btn
                ),
            )
            download_btn.grid(row=2, column=1, pady=30)

            # Status of Downloads
            status: ctk.CTkLabel = ctk.CTkLabel(
                frame,
                text="Status: None",
            )
            status.grid(row=3, column=1, pady=10)

        except TclError as e:
            raise e

    # Video Tab
    def _createVdieoTab(self) -> Optional[str]:
        self.video_tab: ctk.CTkFrame = self.tabs.add("Video")
        # Filling Widgets
        self._createVidPlay_widgets("Video", self.video_tab)

    # Playlist Tab
    def _createPlaylistTab(self) -> Optional[str]:
        self.playlist_tab: ctk.CTkFrame = self.tabs.add("Playlist")
        # Filling Widgets
        self._createVidPlay_widgets("Playlist", self.playlist_tab)

    # Filling Main Bar with Widgets
    def _mainBody_widgets(self) -> Optional[str]:
        try:
            # Making a Tab View for Separate Video and Playlist Downloading Options
            self.tabs = ctk.CTkTabview(self.bodyFrame, width=416, height=352)
            self.tabs.pack(pady=5)

            # Adding Tabs
            self._createVdieoTab()
            self._createPlaylistTab()

        except TclError as e:
            raise e

        self.tabs.get()

    # Create Widgets within the Main Window
    def _create_widgets(self):
        # Creating Frames
        self._createFrames()

        # Creating Side Bar Frame Widgets
        self._sidebar_widgets()

        # Creating Main Bar Frame Widgets
        self._mainBar_widgets()

        # Creating Main Body Frame Widgets
        self._mainBody_widgets()
