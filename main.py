#!/usr/bin/env python3

# imports go here
import sys
import src.app as APP
import src.encryption as Enc
from rich.console import Console
from rich.table import Table
import typer

app = typer.Typer(add_completion=False)
console = Console()

# main function
@app.command('login' ,short_help='Login to the application.')
def login(email: str = None, password: str = None):
    """Login to the application"""
    app = APP.App()
    app.login(email, password)

@app.command('database', short_help='Get all the data from the database.')
def get_data():
    """Get data from the database"""
    app = APP.App()
    data = app.get_data()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name", style="dim", width=12)
    table.add_column("Email", style="dim", width=12)
    table.add_column("Password", style="dim", width=120)
    for row in data:
        table.add_row(str(row[0]), row[1], row[2], row[3])
    console.print(table)

@app.command('signup', short_help='Sign up for the application.')
def add_data(name: str = None, email: str = None, password: str = None):
    """Add data to the database"""
    console.print('Enter your details to signup\n', style='bold green')
    app = APP.App()
    app.signup(name, email, password) # Pass this data to the signup function if it exists

@app.command('reset', short_help='Reset your password.')
def update_data(id: int, name: str, email: str, password: str):
    """Update data in the database"""
    app = APP.App()
    app.update_data(id, name, email, password)

@app.command('leave', short_help='Delete your data from the database.')
def delete_data(id: int):
    """Delete data from the database"""
    app = APP.App()
    app.delete_data(id)

@app.command('generate', short_help='Generate a key and save it to a file.')
def encryption():
    """Generate a key and save it to a file"""
    password = Enc.get_password()
    key = Enc.generate_key(password)
    Enc.save_key(key)

@app.command('regenerate', short_help='Regenerate a key and save it to a file.')
def regenerate():
    """Regenerate a key and save it to a file"""
    console.print('Enter your password to regenerate your key\n', style='bold green')
    console.print('⚠️ WARNING: This will delete your old key and replace it with a new one. Make sure you have a backup of your old key before proceeding.\n', style='bold red')
    Enc.main()

@app.command('encrypt', short_help='Encrypt the database.')
def encrypt_db():
    """Encrypt the database"""
    app = APP.App()
    app.encrypt_db()

@app.command('decrypt', short_help='Decrypt the database.')
def decrypt_db():
    """Decrypt the database"""
    app = APP.App()
    app.decrypt_db()

if __name__ == '__main__':
    app()



# def main():
#     app_instance = app.App()
#     if len(sys.argv) == 1:
#         print('Please enter a command')
#         sys.exit(0)
#     if sys.argv[1] == 'login':
#         app_instance.login(sys.argv[2], sys.argv[3])
#     elif sys.argv[1] == 'genkey':
#         gen_key.main()
#     elif sys.argv[1] == 'getdata':
#         print(app_instance.get_data())
#     elif sys.argv[1] == 'insertdata':
#         app_instance.insert_data(sys.argv[2], sys.argv[3], sys.argv[4])
#     else:
#         # Print usage
#         print('Usage: python3 main.py [command] [args]')
#         print('Commands:')
#         print('login [email] [password]')
#         print('genkey')
#         print('getdata')
#         print('insertdata [name] [email] [password]')
#         print('Invalid command')
#         sys.exit(0)
        

# if __name__ == '__main__':
#     main()

#     while True:
#         try:
#             print('1. Login')
#             print('2. Register')
#             print('3. Exit')
#             print('4. Reset')
#             choice = input('Enter your choice: ')
#             if choice == '1':
#                 email = input('Enter your email: ')
#                 password = input('Enter your password: ')
#                 app_instance.login(email, password)
#             elif choice == '2':
#                 name = input('Enter your name: ')
#                 email = input('Enter your email: ')
#                 password = input('Enter your password: ')
#                 app_instance.insert_data(name, email, password)
#             elif choice == '4':
#                 name = input('Enter your name: ')
#                 email = input('Enter your email: ')
#                 password = input('Enter new password: ')
#                 app_instance.reset(name, email, password)
#             elif choice == '3':
#                 sys.exit(0)
#             else:
#                 print('Invalid choice')
#         except KeyboardInterrupt:
#             sys.exit(0)


# if __name__ == "__main__":
#     main()