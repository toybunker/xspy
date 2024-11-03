from cryptography.fernet import Fernet
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def generate_key():
    """
    Generate a new encryption key.
    """
    return Fernet.generate_key()

def load_key():
    """
    Load the previously generated key.
    """
    return open("secret.key", "rb").read()

def save_key(key):
    """
    Save the generated key to a file.
    """
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def encrypt_data(data, key):
    """
    Encrypt the data using the provided key.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode())

def decrypt_data(data, key):
    """
    Decrypt the data using the provided key.
    """
    fernet = Fernet(key)
    return fernet.decrypt(data).decode()

def send_email(smtp_server, port, sender_email, sender_password, receiver_email, subject, body, attachments):
    """
    Send an email with the specified attachments.
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment in attachments:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attachment, "rb").read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment)}')
        msg.attach(part)

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
