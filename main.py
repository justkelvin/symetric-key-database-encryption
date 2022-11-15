#!/usr/bin/env python3

# imports go here
import src.app as app

# main function
def main():
    app_instance = app.App()
    app_instance.insert_data()

if __name__ == "__main__":
    main()