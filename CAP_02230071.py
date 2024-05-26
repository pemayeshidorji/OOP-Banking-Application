import os
import random

# File to store account information
ACCOUNTS_FILE = "accounts.txt"

# Base Account class
class Account:
    def __init__(self, account_number, password, account_type, balance=0.0):
        self.account_number = account_number
        self.password = password
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}.")
        else:
            print("Invalid deposit amount.")

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            print("Invalid withdrawal amount.")

    def display_balance(self):
        print(f"Current balance: ${self.balance}")

# PersonalAccount class inheriting from Account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Personal", balance)

# BusinessAccount class inheriting from Account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0.0):
        super().__init__(account_number, password, "Business", balance)

# Function to create an account
def create_account(account_type):
    account_number = str(random.randint(100000, 999999))
    password = str(random.randint(1000, 9999))
    balance = 0.0

    # Create account based on type
    if account_type == "Personal":
        account = PersonalAccount(account_number, password, balance)
    elif account_type == "Business":
        account = BusinessAccount(account_number, password, balance)
    else:
        print("Invalid account type.")
        return

    # Save account information to file
    with open(ACCOUNTS_FILE, 'a') as file:
        file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")
    
    print(f"Account created! Account Number: {account.account_number}, Password: {account.password}")

# Function to load all accounts from the file
def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, 'r') as file:
            for line in file:
                account_number, password, account_type, balance = line.strip().split(',')
                balance = float(balance)
                if account_type == "Personal":
                    accounts[account_number] = PersonalAccount(account_number, password, balance)
                elif account_type == "Business":
                    accounts[account_number] = BusinessAccount(account_number, password, balance)
    return accounts

# Function to save all accounts to the file
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, 'w') as file:
        for account in accounts.values():
            file.write(f"{account.account_number},{account.password},{account.account_type},{account.balance}\n")

# Function to login to an account
def login(account_number, password):
    accounts = load_accounts()
    if account_number in accounts and accounts[account_number].password == password:
        print("Login successful!")
        return accounts[account_number]
    else:
        print("Invalid account number or password.")
        return None

# Function to delete an account
def delete_account(account_number, password):
    accounts = load_accounts()
    if account_number in accounts and accounts[account_number].password == password:
        del accounts[account_number]
        save_accounts(accounts)
        print("Account deleted successfully.")
    else:
        print("Invalid account number or password.")

# Function to transfer money between accounts
def transfer_money(from_account, to_account_number, amount):
    accounts = load_accounts()
    if to_account_number in accounts:
        if from_account.balance >= amount:
            from_account.withdraw(amount)
            accounts[to_account_number].deposit(amount)
            save_accounts(accounts)
            print(f"Transferred ${amount} to account {to_account_number}.")
        else:
            print("Insufficient funds.")
    else:
        print("Receiving account does not exist.")

# Main function to interact with the banking system
def main():
    while True:
        print("\nBanking System")
        print("1. Create Account")
        print("2. Login")
        print("3. Delete Account")
        print("4. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            account_type = input("Enter account type (Personal/Business): ")
            create_account(account_type)

        elif choice == '2':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = login(account_number, password)
            if account:
                while True:
                    print("\nAccount Menu")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Display Balance")
                    print("4. Transfer Money")
                    print("5. Logout")
                    choice = input("Enter choice: ")

                    if choice == '1':
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                        save_accounts({account.account_number: account})

                    elif choice == '2':
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                        save_accounts({account.account_number: account})

                    elif choice == '3':
                        account.display_balance()

                    elif choice == '4':
                        to_account_number = input("Enter account number to transfer to: ")
                        amount = float(input("Enter amount to transfer: "))
                        transfer_money(account, to_account_number, amount)
                        save_accounts({account.account_number: account})

                    elif choice == '5':
                        break

                    else:
                        print("Invalid choice.")

        elif choice == '3':
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            delete_account(account_number, password)

        elif choice == '4':
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
