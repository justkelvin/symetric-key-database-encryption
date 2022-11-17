#!/usr/bin/env python3

# imports go here
import sys
import src.app as app
import src.gen_key as gen_key

# main function
def main():
    app_instance = app.App()
    if len(sys.argv) == 1:
        print('Please enter a command')
        sys.exit(0)
    if sys.argv[1] == 'login':
        app_instance.login(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'genkey':
        gen_key.main()
    elif sys.argv[1] == 'getdata':
        print(app_instance.get_data())
    elif sys.argv[1] == 'insertdata':
        app_instance.insert_data(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print('Invalid command')

if __name__ == '__main__':
    main()

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