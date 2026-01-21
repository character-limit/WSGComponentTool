import os
from datetime import datetime
from user import User
from userdb import UserDB

def title_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Inventory Management System ===")
    print("1: Login")
    print("2: Create Account")
    print("3: Exit")
    choice = input("Select an option: ")

    if choice == "1":
        login_page()
    elif choice == "2":
        create_user_page()
    elif choice == "3":
        exit()
    else:
        title_page()

def login_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Login ===")
    username = input("Username: ").lower()
    password = input("Password: ")

    if db.check_login(username, password):
        print("Successful login!")
        print(f"Welcome, {User.session.firstName}!")
    else:
        print("Login failed.")

def create_user_page():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=== Create User Page ===")
    firstName = input("First Name: ")
    lastName = input("Last Name: ")
    username = input("Username: ")
    password = input("Password: ")

    user = User(firstName, lastName, username, password)

    try:
        db.add_user(user)
        print("User created")
    except Exception as e:
        print(f"Error creating user: {e}")

if __name__ == "__main__":

    db = UserDB()
    title_page()