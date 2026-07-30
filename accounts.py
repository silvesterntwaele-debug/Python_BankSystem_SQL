import random
from db import execute_query


def generate_account_number():
    """Generates a random 10-digit account number as a string."""
    return str(random.randint(1000000000, 9999999999))


def create_account(user_id, account_type):
    """
    Creates a new account for a user. account_type must be
    'Savings', 'Checking', or 'Business'.
    Returns the new account number on success, or an error message.
    """
    valid_types = ("Savings", "Checking", "Business")
    if account_type not in valid_types:
        return f"Invalid account type. Must be one of: {valid_types}"

    account_number = generate_account_number()

    execute_query(
        "INSERT INTO Accounts (UserID, AccountNumber, AccountType) VALUES (?, ?, ?)",
        (user_id, account_number, account_type)
    )

    return account_number


def get_accounts_for_user(user_id):
    """Returns all accounts belonging to a user."""
    return execute_query(
        "SELECT AccountID, AccountNumber, AccountType, Balance FROM Accounts WHERE UserID = ?",
        (user_id,),
        fetch=True
    )


def get_balance(account_id):
    """Returns the balance of a specific account."""
    result = execute_query(
        "SELECT Balance FROM Accounts WHERE AccountID = ?",
        (account_id,),
        fetch=True
    )
    if not result:
        return None
    return result[0].Balance


def get_account_by_number(account_number):
    """Looks up an account by its AccountNumber. Returns AccountID or None."""
    result = execute_query(
        "SELECT AccountID FROM Accounts WHERE AccountNumber = ?",
        (account_number,),
        fetch=True
    )
    if not result:
        return None
    return result[0].AccountID