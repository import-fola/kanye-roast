import pyautogui
import time
from PIL import Image
import pywinctl as gw
from dotenv import load_dotenv


def find_browser_window(title_substring):
    """
    Finds a browser window that contains the given substring in its title.
    
    :param title_substring: Substring to look for in the window title
    :return: Window object if found, None otherwise
    """
    windows = gw.getWindowsWithTitle(title_substring)
    return windows[0] if windows else None

def capture_browser_window(window_title_substring, output_folder="frames", interval=5, image_format='png'):
    """
    Captures screenshots of the browser window at specified intervals.
    
    :param window_title_substring: Substring to identify the browser window
    :param output_folder: Folder to save the captured images
    :param interval: Time interval between screenshots in seconds
    :param image_format: Format of the saved image
    """
    browser_window = find_browser_window(window_title_substring)
    if not browser_window:
        print(f"No window with title containing '{window_title_substring}' found.")
        return

    try:
        while True:
            browser_window.activate()  # Bring the browser window to the front
            screenshot = pyautogui.screenshot(region=(
                browser_window.left,
                browser_window.top,
                browser_window.width,
                browser_window.height
            ))
            timestamp = int(time.time())
            filename = f"{output_folder}/frame.{image_format}"
            screenshot.save(filename)
            print(f"Saved screenshot to {filename}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Stopped capturing screenshots.")

if __name__ == "__main__":
    load_dotenv()
    # Example usage: capture screenshots of a window with 'Google' in its title
    capture_browser_window("Promptlib")