import tkinter as tk
from tkinter import ttk, messagebox
from auth import register_user, login_user
from accounts import create_account, get_accounts_for_user, get_account_by_number
from transactions import deposit, withdraw, transfer, get_transaction_history


class BankApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bank System")
        self.geometry("500x600")
        self.resizable(False, False)
        self.current_user = None

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_login_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # ---------------- LOGIN / REGISTER ----------------
    def show_login_screen(self):
        self.current_user = None
        self.clear_container()
        frame = self.container

        tk.Label(frame, text="Bank System", font=("Arial", 20, "bold")).pack(pady=20)

        tk.Label(frame, text="Username").pack()
        username_entry = tk.Entry(frame, width=30)
        username_entry.pack(pady=5)

        tk.Label(frame, text="Password").pack()
        password_entry = tk.Entry(frame, width=30, show="*")
        password_entry.pack(pady=5)

        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            if not username or not password:
                messagebox.showwarning("Missing info", "Enter both username and password.")
                return

            user = login_user(username, password)
            if user:
                self.current_user = user
                self.show_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")

        tk.Button(frame, text="Login", width=20, command=do_login).pack(pady=15)
        tk.Button(frame, text="Create an account", command=self.show_register_screen).pack()

    def show_register_screen(self):
        self.clear_container()
        frame = self.container

        tk.Label(frame, text="Register", font=("Arial", 20, "bold")).pack(pady=20)

        fields = {}
        for label in ["Username", "Email", "Password", "Full Name"]:
            tk.Label(frame, text=label).pack()
            show = "*" if label == "Password" else ""
            entry = tk.Entry(frame, width=30, show=show)
            entry.pack(pady=5)
            fields[label] = entry

        def do_register():
            username = fields["Username"].get().strip()
            email = fields["Email"].get().strip()
            password = fields["Password"].get().strip()
            full_name = fields["Full Name"].get().strip()

            if not all([username, email, password, full_name]):
                messagebox.showwarning("Missing info", "Please fill in all fields.")
                return

            result = register_user(username, email, password, full_name)
            if result is True:
                messagebox.showinfo("Success", "Registration successful! Please log in.")
                self.show_login_screen()
            else:
                messagebox.showerror("Registration Failed", str(result))

        tk.Button(frame, text="Register", width=20, command=do_register).pack(pady=15)
        tk.Button(frame, text="Back to login", command=self.show_login_screen).pack()

    # ---------------- DASHBOARD ----------------
    def show_dashboard(self):
        self.clear_container()
        frame = self.container

        tk.Label(frame, text=f"Welcome, {self.current_user['FullName']}",
                 font=("Arial", 16, "bold")).pack(pady=15)
        tk.Label(frame, text=f"User ID: {self.current_user['UserID']}",
                 font=("Arial", 9), fg="gray").pack()

        columns = ("AccountID", "Type", "Number", "Balance")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=6)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(pady=10)

        def refresh_accounts():
            for row in tree.get_children():
                tree.delete(row)
            accounts = get_accounts_for_user(self.current_user["UserID"])
            for acc in accounts:
                tree.insert("", "end", values=(acc.AccountID, acc.AccountType, acc.AccountNumber, f"R{acc.Balance:.2f}"))

        refresh_accounts()

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="New Account", width=15,
                  command=lambda: self.show_create_account(refresh_accounts)).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Deposit", width=15,
                  command=lambda: self.show_deposit(refresh_accounts)).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Withdraw", width=15,
                  command=lambda: self.show_withdraw(refresh_accounts)).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Transfer", width=15,
                  command=lambda: self.show_transfer(refresh_accounts)).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="History", width=15,
                  command=self.show_history).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Logout", width=15,
                  command=self.logout).grid(row=2, column=1, padx=5, pady=5)

    def logout(self):
        self.current_user = None
        self.show_login_screen()

    # ---------------- ACTION POPUPS ----------------
    def show_create_account(self, on_done):
        popup = tk.Toplevel(self)
        popup.title("New Account")
        popup.geometry("300x200")

        tk.Label(popup, text="Account Type").pack(pady=5)
        acc_type = ttk.Combobox(popup, values=["Savings", "Checking", "Business"], state="readonly")
        acc_type.pack(pady=5)

        def submit():
            chosen = acc_type.get()
            if not chosen:
                messagebox.showwarning("Missing info", "Please select an account type.")
                return

            user_id = self.current_user["UserID"]
            result = create_account(user_id, chosen)

            if isinstance(result, str) and result.startswith("Invalid"):
                messagebox.showerror("Error", result)
            elif isinstance(result, str) and ("FOREIGN KEY" in result or "conflicted" in result):
                messagebox.showerror(
                    "Error",
                    "Your session's User ID is no longer valid. Please log out and log back in."
                )
            else:
                messagebox.showinfo("Success", f"Account created: {result}")
                on_done()
                popup.destroy()

        tk.Button(popup, text="Create", command=submit).pack(pady=15)

    def show_deposit(self, on_done):
        self._amount_popup("Deposit", on_done, deposit)

    def show_withdraw(self, on_done):
        self._amount_popup("Withdraw", on_done, withdraw)

    def _amount_popup(self, title, on_done, action_fn):
        popup = tk.Toplevel(self)
        popup.title(title)
        popup.geometry("300x220")

        tk.Label(popup, text="Account Number").pack(pady=5)
        acc_entry = tk.Entry(popup)
        acc_entry.pack(pady=5)

        tk.Label(popup, text="Amount").pack(pady=5)
        amount_entry = tk.Entry(popup)
        amount_entry.pack(pady=5)

        def submit():
            account_number = acc_entry.get().strip()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Enter a valid amount.")
                return

            account_id = get_account_by_number(account_number)
            if account_id is None:
                messagebox.showerror("Error", "Account number not found.")
                return

            result = action_fn(account_id, amount)
            if isinstance(result, (int, float)):
                messagebox.showinfo("Success", f"New balance: R{result:.2f}")
                on_done()
                popup.destroy()
            else:
                messagebox.showerror("Error", str(result))

        tk.Button(popup, text=title, command=submit).pack(pady=15)

    def show_transfer(self, on_done):
        popup = tk.Toplevel(self)
        popup.title("Transfer")
        popup.geometry("300x260")

        tk.Label(popup, text="From Account Number").pack(pady=5)
        from_entry = tk.Entry(popup)
        from_entry.pack(pady=5)

        tk.Label(popup, text="To Account Number").pack(pady=5)
        to_entry = tk.Entry(popup)
        to_entry.pack(pady=5)

        tk.Label(popup, text="Amount").pack(pady=5)
        amount_entry = tk.Entry(popup)
        amount_entry.pack(pady=5)

        def submit():
            from_number = from_entry.get().strip()
            to_number = to_entry.get().strip()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Enter a valid amount.")
                return

            from_id = get_account_by_number(from_number)
            to_id = get_account_by_number(to_number)

            if from_id is None:
                messagebox.showerror("Error", "Source account number not found.")
                return
            if to_id is None:
                messagebox.showerror("Error", "Destination account number not found.")
                return

            result = transfer(from_id, to_id, amount)
            if result is True:
                messagebox.showinfo("Success", "Transfer completed.")
                on_done()
                popup.destroy()
            else:
                messagebox.showerror("Error", str(result))

        tk.Button(popup, text="Transfer", command=submit).pack(pady=15)

    def show_history(self):
        popup = tk.Toplevel(self)
        popup.title("Transaction History")
        popup.geometry("500x350")

        tk.Label(popup, text="Account Number").pack(pady=5)
        acc_entry = tk.Entry(popup)
        acc_entry.pack(pady=5)

        columns = ("Date", "Type", "Amount", "Balance After")
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110)
        tree.pack(pady=10, fill="both", expand=True)

        def load_history():
            account_number = acc_entry.get().strip()
            account_id = get_account_by_number(account_number)
            if account_id is None:
                messagebox.showerror("Error", "Account number not found.")
                return

            for row in tree.get_children():
                tree.delete(row)
            history = get_transaction_history(account_id)
            if not history:
                messagebox.showinfo("No data", "No transactions found.")
                return
            for t in history:
                tree.insert("", "end", values=(
                    t.TransactionDate.strftime("%Y-%m-%d %H:%M"),
                    t.TransactionType,
                    f"R{t.Amount:.2f}",
                    f"R{t.BalanceAfter:.2f}"
                ))

        tk.Button(popup, text="Load History", command=load_history).pack(pady=5)


if __name__ == "__main__":
    app = BankApp()
    app.mainloop()