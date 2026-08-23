"""Desktop entry point: the launcher inside the Windows .exe.

The analysis and the interface are the same code the web app runs. This
only starts Streamlit's server against a bundled copy of ``app.py`` and
points a browser at it, so the desktop build and the hosted site never
drift apart.

Run directly (``python desktop.py``) it behaves the same way, which is how
the launcher gets tested without building an executable first.
"""

import os
import socket
import sys
import threading
import time
import webbrowser
from pathlib import Path

STARTUP_TIMEOUT_SECONDS = 60


def bundle_dir() -> Path:
    """Where the app files live.

    PyInstaller unpacks a onefile build into a temporary directory and
    records it on ``sys._MEIPASS``; running from a checkout, it is just the
    directory this file sits in.
    """
    return Path(getattr(sys, "_MEIPASS", Path(__file__).parent))


def free_port() -> int:
    """Ask the OS for an unused port.

    Hardcoding 8501 would collide with a Streamlit the user already has
    running, and the second instance would either fail or silently attach
    to the first one's page.
    """
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def open_browser_when_ready(port: int, timeout: float = STARTUP_TIMEOUT_SECONDS) -> None:
    """Open the page once the server is actually accepting connections.

    Opening immediately shows a connection error, because the first launch
    of a frozen build spends a while unpacking before the server binds.
    """
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        with socket.socket() as probe:
            probe.settimeout(0.5)
            if probe.connect_ex(("127.0.0.1", port)) == 0:
                webbrowser.open(f"http://localhost:{port}")
                return
        time.sleep(0.3)


def main() -> None:
    root = bundle_dir()
    app_path = root / "app.py"

    # The bundled package lives beside app.py rather than on the normal
    # import path, so make it importable before Streamlit executes the app.
    sys.path.insert(0, str(root))

    # Streamlit reads config from the working directory; point it at the
    # bundle so the packaged .streamlit/config.toml is the one that applies.
    os.chdir(root)

    port = free_port()

    # Headless does two things that matter here. It suppresses Streamlit's
    # first-run "enter your email" prompt, which otherwise blocks a
    # double-clicked executable on a question the user cannot see; and it
    # stops Streamlit opening the browser itself, which it would do before
    # the server is ready. We open the browser ourselves once the port
    # answers.
    threading.Thread(target=open_browser_when_ready, args=(port,), daemon=True).start()

    sys.argv = [
        "streamlit",
        "run",
        str(app_path),
        "--server.port",
        str(port),
        "--server.headless",
        "true",
        "--browser.gatherUsageStats",
        "false",
        "--global.developmentMode",
        "false",
    ]

    from streamlit.web import cli as stcli

    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
