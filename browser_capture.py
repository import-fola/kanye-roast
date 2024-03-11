import pyautogui
import time
from PIL import Image
import pywinctl as gw
from dotenv import load_dotenv
import os
import sys


def find_browser_window(title_substring):
    """
    Finds a browser window that contains the given substring in its title.
    
    :param title_substring: Substring to look for in the window title
    :return: Window object if found, None otherwise
    """
    windows = gw.getWindowsWithTitle(title_substring)
    return windows[0] if windows else None

def capture_browser_window(window_title_substring, output_folder="frames", interval=30, image_format='png'):
    """
    Captures screenshots of the browser window at specified intervals.
    
    :param window_title_substring: Substring to identify the browser window
    :param output_folder: Folder to save the captured images
    :param interval: Time interval between screenshots in seconds
    :param image_format: Format of the saved image
    """
    # Create the frames folder if it doesn't exist
    frames_dir = os.path.join(os.getcwd(), output_folder)
    os.makedirs(frames_dir, exist_ok=True)

    browser_window = find_browser_window(window_title_substring)
    if not browser_window:
        print(f"No window with title containing '{window_title_substring}' found.")
        return
    else:
        print("Window found:", browser_window.title)

    try:
        while True:
            browser_window.activate()  # Bring the browser window to the front
            time.sleep(.5) 
            region=(
                browser_window.left,
                browser_window.top,
                browser_window.width,
                browser_window.height
            )
            print("Attempting to capture region:", region)
            screenshot = pyautogui.screenshot(region=region)
            timestamp = int(time.time())
            filename = f"{output_folder}/frame.{image_format}"
            screenshot.save(filename)
            print(f"📸 Saved screenshot to {filename}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("❌ Stopped capturing screenshots.")
    except Exception as e:
        print(f"⚠️ An error occurred: {e}")

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) > 1:
        window_title_substring = sys.argv[1]
        print("Trying to find window: ", window_title_substring)
        capture_browser_window(window_title_substring)
    else:
        default_window_title = 'Promptlib'
        print("You didn't provide a browser window title as an arg, so will use: ", default_window_title)
        capture_browser_window(default_window_title)
    