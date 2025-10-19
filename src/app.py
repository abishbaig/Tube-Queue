from gui.app_gui import TubeQueue
import os
import atexit
import sys

# Define the PID file path (e.g., in the system's temporary directory)
PID_FILE = os.path.join(os.path.curdir, "tube_queue_app.pid")


def check_single_instance():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read())
            # Check if the process with the stored PID is still running
            os.kill(pid, 0)  # Sends signal 0 to check if process exists
            print("Another instance of the application is already running.")
            sys.exit()
        except (FileNotFoundError, ValueError, ProcessLookupError):
            # PID file exists but process is not running, or file is corrupted
            pass  # Proceed to create new PID file

    # Create the PID file for the current instance
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Register cleanup function to delete PID file on exit
    atexit.register(cleanup_pid_file)


def cleanup_pid_file():
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)


def main():

    try:
        check_single_instance()
        tube_queue: TubeQueue = None
        tube_queue = TubeQueue()
        tube_queue.mainloop()
    except Exception as e:
        print("Fatal error starting app:", e)
        try:
            if "tube_queue" in locals() and tube_queue is not None:
                tube_queue.destroy()
        except Exception:
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
