from cryptography.fernet import Fernet
import json
import time
from config import ENCRYPTION_KEY, SESSION_TIMEOUT

class CredentialsManager:
    def __init__(self):
        self.cipher = Fernet(ENCRYPTION_KEY.encode())
        self.credentials_store = {}
    
    def encrypt_data(self, data):
        json_data = json.dumps(data)
        encrypted = self.cipher.encrypt(json_data.encode())
        return encrypted.decode()
    
    def decrypt_data(self, encrypted_data):
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return json.loads(decrypted.decode())
        except:
            return None
    
    def save_credentials(self, user_id, username, password):
        data = {
            'username': username,
            'password': password,
            'timestamp': time.time()
        }
        encrypted = self.encrypt_data(data)
        self.credentials_store[user_id] = encrypted
        return True
    
    def get_credentials(self, user_id):
        if user_id not in self.credentials_store:
            return None
        
        encrypted = self.credentials_store[user_id]
        data = self.decrypt_data(encrypted)
        
        if not data:
            return None
        
        if time.time() - data['timestamp'] > SESSION_TIMEOUT:
            self.delete_credentials(user_id)
            return None
        
        return {
            'username': data['username'],
            'password': data['password']
        }
    
    def delete_credentials(self, user_id):
        if user_id in self.credentials_store:
            del self.credentials_store[user_id]
            return True
        return False
    
    def has_credentials(self, user_id):
        return self.get_credentials(user_id) is not None
    
    def get_session_time_remaining(self, user_id):
        if user_id not in self.credentials_store:
            return 0
        
        encrypted = self.credentials_store[user_id]
        data = self.decrypt_data(encrypted)
        
        if not data:
            return 0
        
        remaining = SESSION_TIMEOUT - (time.time() - data['timestamp'])
        return max(0, int(remaining))

creds_manager = CredentialsManager()
