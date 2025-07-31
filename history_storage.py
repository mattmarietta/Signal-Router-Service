import json
import os
from security_utils import encrypt_log, decrypt_log # Import our new utilities

class HistoryStorage:
    def __init__(self, log_file='history_store.json.encrypted'):
        self.log_file = log_file

    def write_log(self, data: dict):
        """Encrypts and writes a single log entry."""
        encrypted_token = encrypt_log(data)
        # In a real system, we'd append to a log stream.
        # For this trial, we'll just overwrite a single file for simplicity.
        with open(self.log_file, "wb") as f:
            f.write(encrypted_token)
        print(f"Log for session {data.get('session_id')} written and encrypted.")

    def read_log(self) -> dict:
        """Reads and decrypts the log file."""
        if not os.path.exists(self.log_file):
            return {"error": "Log file not found."}
        with open(self.log_file, "rb") as f:
            encrypted_token = f.read()
        
        return decrypt_log(encrypted_token)