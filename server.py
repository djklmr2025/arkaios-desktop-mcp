import os
import sys
from mcp.server.fastmcp import FastMCP
import pyautogui
import mss
import platform
import base64
from io import BytesIO
from PIL import Image

# Import from local copies
from ui_extraction import extract_interactive_elements
from actions import launch_application, focus_app, get_running_apps, type_unicode_smart

# Create the FastMCP server
mcp = FastMCP("ARKAIOS Desktop Control")

@mcp.tool()
def get_client_info() -> str:
    """Returns information about the host client (Claude, VS Code, etc.) for compatibility logic."""
    client = os.getenv("ARKAIOS_CLIENT", "unknown")
    if client == "claude":
        return "Connected to Claude Desktop (Anthropic Labs). Full image format support enabled."
    elif client == "vscode":
        return "Connected to VS Code (Cline/Roo). Text-based optimized responses enabled."
    else:
        return f"Connected to generic agent: {client}"

@mcp.tool()
def extract_ui() -> list:
    """Extract interactive elements from the current screen/window."""
    return extract_interactive_elements()

@mcp.tool()
def get_apps() -> list:
    """Get a list of currently running applications."""
    return get_running_apps()

@mcp.tool()
def click(x: int, y: int, clicks: int = 1, button: str = "left") -> str:
    """Click on the screen at the given coordinates."""
    pyautogui.click(x=x, y=y, clicks=clicks, button=button)
    return f"Clicked at ({x}, {y})"

@mcp.tool()
def type_text(text: str) -> str:
    """Type the given text using the keyboard."""
    type_unicode_smart(text)
    return "Typed text successfully"

@mcp.tool()
def hotkey(keys: list[str]) -> str:
    """Press a combination of keys (e.g. ['ctrl', 'c'])."""
    pyautogui.hotkey(*keys)
    return f"Pressed hotkey: {keys}"

@mcp.tool()
def open_app(app_name: str) -> str:
    """Launch an application by its name."""
    launch_application(app_name)
    return f"Launched {app_name}"

@mcp.tool()
def focus_window(app_name: str) -> str:
    """Bring an application window to the foreground."""
    success = focus_app(app_name)
    return f"Focused {app_name}" if success else f"Failed to focus {app_name}"

@mcp.tool()
def take_screenshot() -> str:
    """Take a screenshot and return it as a base64 encoded PNG."""
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        shot = sct.grab(monitor)
        img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
        # Resize to manageable size like in the original agent
        img = img.resize((1280, 720))
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("utf-8")

if __name__ == "__main__":
    mcp.run()
