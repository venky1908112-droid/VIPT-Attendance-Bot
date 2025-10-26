from cryptography.fernet import Fernet

key = Fernet.generate_key()
print("=" * 60)
print("YOUR ENCRYPTION KEY:")
print("=" * 60)
print(key.decode())
print("=" * 60)
print("\nCOPY THIS KEY!")
print("You will paste it in config.py")
