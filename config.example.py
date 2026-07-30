SERVER = "localhost"  # or your SQL Server instance name
DATABASE = "BankSystemDB"
DRIVER = "{ODBC Driver 17 for SQL Server}"

CONNECTION_STRING = (
    f"DRIVER={DRIVER};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)