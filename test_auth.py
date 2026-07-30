from auth import register_user, login_user

#Try registering a new user
result = register_user("silvester_test", "silvester@example.com", "Mypassword123", "Silvester Ntwaele")
print("Register result:", result)

#Try logging in
user = login_user("silvester_test", "Mypassword123")
print("Login result:", user)

#Try wrong password
user_wrong = login_user("silvester_test", "WrongPassword")
print("Login with wrong password result:", user_wrong)
