import bcrypt
from db import execute_query


def register_user(username, email, password, full_name):
    """
    Registers a new user. Returns True on success, or a string error message on failure.
    """
    # Check if username or email already exists
    existing = execute_query(
        "SELECT UserID FROM Users WHERE Username = ? OR Email = ?",
        (username, email),
        fetch=True
    )
    if existing:
        return "Username or email already exists."

    # Hash the password with bcrypt (salt is generated and embedded inside the hash automatically)
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    hashed_str = hashed.decode('utf-8')

    # bcrypt embeds its own salt, so we store a placeholder in the Salt column
    salt_placeholder = "bcrypt_embedded"

    # Insert the new user into the database
    execute_query(
        "INSERT INTO Users (Username, Email, PasswordHash, Salt, FullName) VALUES (?, ?, ?, ?, ?)",
        (username, email, hashed_str, salt_placeholder, full_name)
    )

    return True  # Registration successful


def login_user(username, password):
    """
    Verifies user credentials. Returns the user's info (as a dict) on success, or None on failure.
    """
    result = execute_query(
        "SELECT UserID, Username, Email, PasswordHash, FullName, IsActive FROM Users WHERE Username = ?",
        (username,),
        fetch=True
    )

    if not result:
        return None  # No such user

    user = result[0]

    if not user.IsActive:
        return None  # Account deactivated

    stored_hash = user.PasswordHash.encode('utf-8')
    password_bytes = password.encode('utf-8')

    if bcrypt.checkpw(password_bytes, stored_hash):
        return {
            "UserID": user.UserID,
            "Username": user.Username,
            "FullName": user.FullName
        }
    else:
        return None  # Wrong password