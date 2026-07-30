from accounts import create_account, get_accounts_for_user, get_balance

acc_num = create_account(1, "Savings")   # user_id=1 is your silvester_test user
print("New account number:", acc_num)

accounts = get_accounts_for_user(1)
print("Accounts:", accounts)