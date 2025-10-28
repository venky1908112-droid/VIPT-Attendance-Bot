import json
import time
from cryptography.fernet import Fernet
from config import ENCRYPTION_KEY, SESSION_TIMEOUT

CREDENTIALS_FILE = "credentials_store.json"

class CredentialsManager:
    def __init__(self):
        self.cipher = Fernet(ENCRYPTION_KEY.encode())
        self.credentials_store = self.load_store()

    def load_store(self):
        try:
            with open(CREDENTIALS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_store(self):
        with open(CREDENTIALS_FILE, "w") as f:
            json.dump(self.credentials_store, f)

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
        print(f"[DEBUG] Saving creds for user_id: {user_id}, username: {username}")
        data = {
            'username': username,
            'password': password,
            'timestamp': time.time()
        }
        encrypted = self.encrypt_data(data)
        self.credentials_store[str(user_id)] = encrypted
        self.save_store()
        return True

    def get_credentials(self, user_id):
        print(f"[DEBUG] Getting creds for user_id: {user_id}")
        if str(user_id) not in self.credentials_store:
            return None
        encrypted = self.credentials_store[str(user_id)]
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
        print(f"[DEBUG] Deleting creds for user_id: {user_id}")
        if str(user_id) in self.credentials_store:
            del self.credentials_store[str(user_id)]
            self.save_store()
            return True
        return False

    def has_credentials(self, user_id):
        return self.get_credentials(user_id) is not None

    def get_session_time_remaining(self, user_id):
        if str(user_id) not in self.credentials_store:
            return 0
        encrypted = self.credentials_store[str(user_id)]
        data = self.decrypt_data(encrypted)
        if not data:
            return 0
        remaining = SESSION_TIMEOUT - (time.time() - data['timestamp'])
        return max(0, int(remaining))

creds_manager = CredentialsManager()
