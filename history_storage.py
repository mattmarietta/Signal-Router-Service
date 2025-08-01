import os
from security_utils import encrypt_log, decrypt_log

#Class is used to read and write to the file we defined as history_store
class HistoryStorage:

    def __init__(self, log_file='history_store.json.encrypted'):
        #Initialize the log file path which we will store encrypted logs within
        self.log_file = log_file

    def write_log(self, log_entry: dict):
        """
        This function will read the existing log list and append the new entry
        Then writes the list back to the file in an encrypted format.
        """

        #Read the current log and decrypt it into a list
        log_list = self._read_and_decrypt()
        
        #Append the new entry
        log_list.append(log_entry)
        
        #Encrypt the entire updated list and write it back
        self._encrypt_and_write(log_list)
        
        print(f"Log for session {log_entry.get('session_id')} appended and encrypted.")

    def get_all_logs(self) -> list:
        #Helper function to read and decrypt the entire log history

        return self._read_and_decrypt()
    
    def get_last_log(self) -> dict:
        #Helper function to read and decrypt the last log in the entry
        log_list = self._read_and_decrypt()
        if not log_list:
            return {}  
        return log_list[-1] 

    def _read_and_decrypt(self) -> list:
        #Internal function to safely read and decrypt the log file

        if not os.path.exists(self.log_file):
            return []  
        
        with open(self.log_file, "rb") as f:
            encrypted_token = f.read()
        
        if not encrypted_token:
            return []

        try:
            #The decrypt_log function now expects to decrypt a list
            return decrypt_log(encrypted_token)
        except Exception:
            return [] 
        

    def _encrypt_and_write(self, log_list: list):
        #Function to encrypt and write the entire log list
        encrypted_token = encrypt_log(log_list)
        with open(self.log_file, "wb") as f:
            f.write(encrypted_token)