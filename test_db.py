from db import execute_query

rows = execute_query("SELECT * FROM Users", fetch=True)
print(rows)