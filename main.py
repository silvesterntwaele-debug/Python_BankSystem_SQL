from auth import register_user, login_user
from accounts import create_account, get_accounts_for_user, get_balance
from transactions import deposit, withdraw, transfer, get_transaction_history


def print_menu(title, options):
    print(f"\n--- {title} ---")
    for key, label in options.items():
        print(f"{key}. {label}")


def main_menu():
    options = {
        "1": "Register",
        "2": "Login",
        "3": "Exit"
    }
    while True:
        print_menu("Bank System", options)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_register()
        elif choice == "2":
            user = handle_login()
            if user:
                account_menu(user)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")


def handle_register():
    print("\n--- Register ---")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = input("Password: ").strip()
    full_name = input("Full Name: ").strip()

    result = register_user(username, email, password, full_name)
    if result is True:
        print("Registration successful! You can now log in.")
    else:
        print(f"Registration failed: {result}")


def handle_login():
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = login_user(username, password)
    if user:
        print(f"Welcome, {user['FullName']}!")
        return user
    else:
        print("Invalid username or password.")
        return None


def account_menu(user):
    options = {
        "1": "Create new account",
        "2": "View my accounts",
        "3": "Deposit",
        "4": "Withdraw",
        "5": "Transfer",
        "6": "Transaction history",
        "7": "Logout"
    }
    while True:
        print_menu(f"Account Menu - {user['FullName']}", options)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            handle_create_account(user)
        elif choice == "2":
            handle_view_accounts(user)
        elif choice == "3":
            handle_deposit()
        elif choice == "4":
            handle_withdraw()
        elif choice == "5":
            handle_transfer()
        elif choice == "6":
            handle_history()
        elif choice == "7":
            print("Logged out.")
            break
        else:
            print("Invalid option, try again.")


def handle_create_account(user):
    print("\nAccount types: Savings, Checking, Business")
    acc_type = input("Account type: ").strip().capitalize()
    result = create_account(user["UserID"], acc_type)
    if isinstance(result, str) and result.startswith("Invalid"):
        print(result)
    else:
        print(f"Account created! Account number: {result}")


def handle_view_accounts(user):
    accounts = get_accounts_for_user(user["UserID"])
    if not accounts:
        print("You have no accounts yet.")
        return
    print("\nYour accounts:")
    for acc in accounts:
        print(f"  AccountID: {acc.AccountID} | {acc.AccountType} | {acc.AccountNumber} | Balance: R{acc.Balance}")


def handle_deposit():
    account_id = input("Account ID: ").strip()
    amount = input("Amount to deposit: ").strip()
    try:
        result = deposit(int(account_id), float(amount))
        print(f"New balance: R{result}" if isinstance(result, (int, float)) else result)
    except ValueError:
        print("Invalid input.")


def handle_withdraw():
    account_id = input("Account ID: ").strip()
    amount = input("Amount to withdraw: ").strip()
    try:
        result = withdraw(int(account_id), float(amount))
        print(f"New balance: R{result}" if isinstance(result, (int, float)) else result)
    except ValueError:
        print("Invalid input.")


def handle_transfer():
    from_id = input("From Account ID: ").strip()
    to_id = input("To Account ID: ").strip()
    amount = input("Amount to transfer: ").strip()
    try:
        result = transfer(int(from_id), int(to_id), float(amount))
        print("Transfer successful!" if result is True else result)
    except ValueError:
        print("Invalid input.")


def handle_history():
    account_id = input("Account ID: ").strip()
    try:
        history = get_transaction_history(int(account_id))
        if not history:
            print("No transactions found.")
            return
        print("\nTransaction History:")
        for t in history:
            print(f"  {t.TransactionDate} | {t.TransactionType} | R{t.Amount} | Balance after: R{t.BalanceAfter}")
    except ValueError:
        print("Invalid input.")


if __name__ == "__main__":
    main_menu()