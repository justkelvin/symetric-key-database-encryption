#!/usr/bin/env python3

# Generate an encryption key with password and salt
# imports go here
import base64
import hashlib
import os
import sys

import cryptography
import typer
from click import prompt
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from rich.console import Console

console = Console()
console.print('Database Encryption Project\n', style='bold red')
app = typer.Typer()

# get password
@app.command(short_help='Get password for key generation.')
def get_password():
    """Get the password from the user"""
    password = prompt('Enter the password: ', hide_input=True)
    conf_password = prompt('Confirm the password: ', hide_input=True)
    if password != conf_password:
        console.print('❌ Passwords do not match', style='bold red')
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
    console.print('🔐 Key generated successfully\n', style='bold green')
    return key

# Save the key
@app.command(short_help='Save the key to a file.')
def save_key(key):
    """Save the key to a file called key.key"""
    with open('credentials/key.key', 'wb') as key_file:
        key_file.write(key)
    key_file.close()
    console.print(f'🔑 Key: {key}\n', style='italic green')
    console.print('✅ Encryption Key saved to file at credentials/key.key', style='bold green')

# # main function
@app.command(short_help='Generate a key and save it to a file.')
def main():
    """Main function to generate the key and save it to a file"""
    password = get_password()
    key = generate_key(password)
    save_key(key)
    print(key)

if __name__ == "__main__":
    main()


