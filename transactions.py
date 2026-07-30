from db import get_db_connection


def deposit(account_id, amount, description="Deposit"):
    """Adds money to an account. Returns the new balance."""
    if amount <= 0:
        return "Amount must be greater than zero."

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Balance FROM Accounts WHERE AccountID = ?", (account_id,))
        row = cursor.fetchone()
        if not row:
            return "Account not found."

        new_balance = float(row.Balance) + amount

        cursor.execute(
            "UPDATE Accounts SET Balance = ? WHERE AccountID = ?",
            (new_balance, account_id)
        )
        cursor.execute(
            """INSERT INTO Transactions (AccountID, TransactionType, Amount, BalanceAfter, Description)
               VALUES (?, 'Deposit', ?, ?, ?)""",
            (account_id, amount, new_balance, description)
        )

        conn.commit()
        return new_balance
    except Exception as e:
        conn.rollback()
        return f"Deposit failed: {e}"
    finally:
        cursor.close()
        conn.close()


def withdraw(account_id, amount, description="Withdrawal"):
    """Removes money from an account. Returns the new balance, or an error message."""
    if amount <= 0:
        return "Amount must be greater than zero."

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Balance FROM Accounts WHERE AccountID = ?", (account_id,))
        row = cursor.fetchone()
        if not row:
            return "Account not found."

        current_balance = float(row.Balance)
        if current_balance < amount:
            return "Insufficient funds."

        new_balance = current_balance - amount

        cursor.execute(
            "UPDATE Accounts SET Balance = ? WHERE AccountID = ?",
            (new_balance, account_id)
        )
        cursor.execute(
            """INSERT INTO Transactions (AccountID, TransactionType, Amount, BalanceAfter, Description)
               VALUES (?, 'Withdraw', ?, ?, ?)""",
            (account_id, amount, new_balance, description)
        )

        conn.commit()
        return new_balance
    except Exception as e:
        conn.rollback()
        return f"Withdrawal failed: {e}"
    finally:
        cursor.close()
        conn.close()


def transfer(from_account_id, to_account_id, amount, description="Transfer"):
    """Moves money between two accounts safely. Returns True on success, or an error message."""
    if amount <= 0:
        return "Amount must be greater than zero."
    if from_account_id == to_account_id:
        return "Cannot transfer to the same account."

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Balance FROM Accounts WHERE AccountID = ?", (from_account_id,))
        from_row = cursor.fetchone()
        if not from_row:
            return "Source account not found."

        from_balance = float(from_row.Balance)
        if from_balance < amount:
            return "Insufficient funds."

        cursor.execute("SELECT Balance FROM Accounts WHERE AccountID = ?", (to_account_id,))
        to_row = cursor.fetchone()
        if not to_row:
            return "Destination account not found."

        to_balance = float(to_row.Balance)

        from_new_balance = from_balance - amount
        to_new_balance = to_balance + amount

        cursor.execute("UPDATE Accounts SET Balance = ? WHERE AccountID = ?", (from_new_balance, from_account_id))
        cursor.execute("UPDATE Accounts SET Balance = ? WHERE AccountID = ?", (to_new_balance, to_account_id))

        cursor.execute(
            """INSERT INTO Transactions (AccountID, TransactionType, Amount, BalanceAfter, RelatedAccountID, Description)
               VALUES (?, 'TransferOut', ?, ?, ?, ?)""",
            (from_account_id, amount, from_new_balance, to_account_id, description)
        )
        cursor.execute(
            """INSERT INTO Transactions (AccountID, TransactionType, Amount, BalanceAfter, RelatedAccountID, Description)
               VALUES (?, 'TransferIn', ?, ?, ?, ?)""",
            (to_account_id, amount, to_new_balance, from_account_id, description)
        )

        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return f"Transfer failed: {e}"
    finally:
        cursor.close()
        conn.close()


def get_transaction_history(account_id):
    """Returns all transactions for an account, most recent first."""
    from db import execute_query
    return execute_query(
        "SELECT * FROM Transactions WHERE AccountID = ? ORDER BY TransactionDate DESC",
        (account_id,),
        fetch=True
    )