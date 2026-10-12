import csv
import os
import secrets
import string

# Define the file name where credentials will be saved
CREDENTIALS_FILE = "users.csv"

def initialize_db():
    """Creates the CSV file with headers if it does not exist."""
    if not os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])

def generate_strong_password(length=12):
    """Generates a secure, strong random password."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(secrets.choice(characters) for _ in range(length))

def load_users():
    """Reads all users from the CSV file and returns them as a dictionary."""
    users = {}
    initialize_db()
    with open(CREDENTIALS_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users[row["username"]] = row["password"]
    return users

def save_user(username, password):
    """Appends a single new user to the CSV file."""
    with open(CREDENTIALS_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

def register():
    print("\n--- Account Registration ---")
    username = input("Enter a name for your account: ").strip()

    if not username:
        print("Username cannot be empty!")
        return

    # Load fresh data from the CSV file to check for duplicates
    users_db = load_users()
    if username in users_db:
        print("This account name already exists! Please log in.")
        return

    # Generate a strong password for the user
    suggested_password = generate_strong_password()
    print(f"Suggested Strong Password: {suggested_password}")

    choice = input("Do you want to use this password? (y/n): ").strip().lower()
    if choice == 'y':
        password = suggested_password
    else:
        password = input("Enter your custom password: ").strip()
        if len(password) < 6:
            print("Warning: Custom password is quite short!")

    # Permanently append to our CSV database
    save_user(username, password)
    print(f"Account '{username}' successfully created and saved!")

def login():
    print("\n--- Account Login ---")
    username = input("Enter account name: ").strip()
    password = input("Enter password: ").strip()

    # Always pull current credentials from the CSV file
    users_db = load_users()

    if username in users_db and users_db[username] == password:
        print(f"\n Login successful! Welcome back, {username}.")
        expense_tracker_menu()
    else:
        print(" Invalid account name or password.")

def expense_tracker_menu():
    """Placeholder for your actual Expense Tracker code logic."""
    print("--- Expense Tracker Dashboard ---")
    print("[Now you can add, view, or delete expenses here...]")
    input("\nPress Enter to log out and return to the main menu.")

def main():
    # Make sure file system is ready on boot
    initialize_db()

    while True:
        print("\n===== MAIN MENU =====")
        print("1. Create New Account")
        print("2. Log In")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
