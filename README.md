# Bank System — Python & SQL Server

A full-stack banking application built with Python and Microsoft SQL Server. Supports user registration and secure login, multiple bank accounts per user, deposits, withdrawals, and transfers — with two different interfaces: command-line and desktop GUI.

## Features

- **Secure authentication** — passwords hashed with `bcrypt`, never stored in plain text
- **Multiple accounts per user** — Savings, Checking, or Business
- **Safe transactions** — deposits, withdrawals, and transfers use database transactions with rollback, so a failure mid-operation can never leave balances in an inconsistent state
- **Transaction history** — full audit trail of every deposit, withdrawal, and transfer per account
- **Database-level integrity** — foreign keys, check constraints (e.g. balances can never go negative), and unique constraints enforced directly in SQL Server, not just in application code
- **Three interfaces to the same backend:**
  - `main.py` — command-line interface
  - `gui.py` — desktop GUI built with Tkinter

## Tech Stack

- **Language:** Python 3.13
- **Database:** Microsoft SQL Server
- **DB Driver:** `pyodbc`
- **Password hashing:** `bcrypt`
- **Web framework:** Flask
- **Desktop GUI:** Tkinter (built into Python)

## Database Schema

Four core tables:

| Table | Purpose |
|---|---|
| `Users` | Login credentials and identity info |
| `Accounts` | Each user's bank account(s) and balance |
| `Transactions` | History of deposits, withdrawals, and transfers |
| `AuditLog` | Tracks security/admin events |

Key design choices:
- `Accounts.Balance` has a `CHECK (Balance >= 0)` constraint — the database itself refuses to let a balance go negative, regardless of application logic
- `Transactions.Amount` has a `CHECK (Amount > 0)` constraint
- Foreign keys link `Accounts → Users` and `Transactions → Accounts`, with `RelatedAccountID` on `Transactions` used to track both sides of a transfer

Full schema script: [`schema.sql`](./schema.sql)

## Project Structure
bank_app/
├── main.py              # CLI entry point
├── gui.py                # Tkinter desktop GUI
├── app.py                # Flask web app
├── db.py                  # Database connection layer
├── auth.py               # Registration & login logic
├── accounts.py         # Account creation & lookup
├── transactions.py  # Deposit, withdraw, transfer logic
├── config.example.py # Template for database connection settings
├── schema.sql          # Full SQL Server schema
├── templates/          # HTML templates for the Flask app
└── tests/                 # Manual test scripts for each module

## Setup

**1. Clone the repository**
```bash
git clone https://github.com/silvesterntwaele-debug/Python_BankSystem_SQL.git
cd Python_BankSystem_SQL

2. Install dependencies
pip install pyodbc bcrypt flask --break-system-packages

3. Set up the database
Install SQL Server Express and SQL Server Management Studio (SSMS)
Create a database named BankSystemDB
Run schema.sql in SSMS to create all tables, constraints, and indexes

4. Configure your connection
Copy config.example.py and rename the copy to config.py
Edit config.py with your actual SQL Server instance name

5. Run the app
CLI version:
python main.py

Desktop GUI version:
python gui.py

Then open http://127.0.0.1:5000 in your browser.
Key Learnings
This project involved designing a normalized relational schema from scratch, implementing secure password handling, and — critically — writing transaction logic that's safe under failure. Every money-moving operation (deposit, withdraw, transfer) wraps its database writes in a single transaction: if any step fails partway through, the whole operation rolls back, so funds can never be deducted from one account without landing in another.
Author
Thato Silvester Ntwaele — Diploma in IT (Software Development), Nelson Mandela University
