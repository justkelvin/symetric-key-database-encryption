#!/usr/bin/env python3

# Generate an encryption key with password and salt
# imports go here
import os
import sys
import hashlib
from click import prompt
import typer
import cryptography
from rich.console import Console
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64

console = Console()
console.print('Database Encryption Project', style='bold red')
app = typer.Typer()

# get password
@app.command(short_help='Get password for key generation.')
def get_password():
    """Get the password from the user"""
    password = prompt('Enter the password: ', hide_input=True)
    conf_password = prompt('Confirm the password: ', hide_input=True)
    if password != conf_password:
        print('Passwords do not match')
        sys.exit(0)
    return password

# Generate a key
@app.command(short_help='Generate a key and salt it.')
def generate_key(password):
    """Generate a key from the password and salt and return it"""
    password = password.encode('utf-8') # Convert to bytes
    os.urandom(16) # Generate a random salt
    salt = b'\x8b\x9d\x8f\x9e\x8b\x9d\x8f\x9e\x8b\x9d\x8f\x9e\x8b\x9d\x8f\x9e' # Hardcoded salt

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once 
    return key

# Save the key
@app.command(short_help='Save the key to a file.')
def save_key(key):
    """Save the key to a file called key.key"""
    with open('credentials/key.key', 'wb') as key_file:
        key_file.write(key)
    key_file.close()

# # main function
@app.command(short_help='Generate a key and save it to a file.')
def main():
    """Main function to generate the key and save it to a file"""
    password = get_password()
    print(password)
    key = generate_key(password)
    save_key(key)
    print(key)

if __name__ == "__main__":
    main()


