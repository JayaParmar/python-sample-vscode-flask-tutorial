# https://realpython.com/prevent-python-sql-injection/
import sqlite3

conn = sqlite3.connect('sqlite/app.db')
stmnt = '''CREATE TABLE IF NOT EXISTS users (username TEXT, admin INTEGER)'''
cursor = conn.execute(stmnt)

stmnt = '''INSERT INTO users (username, admin) VALUES ("ran", 1), ("haki", 0)'''
cursor = conn.execute(stmnt)
    
stmnt = '''SELECT * FROM users'''
cursor = conn.execute(stmnt)
result = cursor.fetchone()
#print(result)
conn.commit()


def is_admin(username: str) -> bool:
    cursor = conn.execute(""" SELECT admin FROM users WHERE username = '%s'""" % username)
    result = cursor.fetchone()
    print(result)
    admin, = result
    conn.commit()
    return admin

#is_admin('haki')
#is_admin('ran')
#is_admin('foo')
#is_admin("'; select 1; --")
#is_admin("'; update users set admin = '1' where username = 'haki'; select 1;")
#is_admin('haki')
#username = username.replace("'", "''")

def count_rows(table_name: str) -> int:
    cursor = conn.execute("""SELECT count(*) FROM {}""".format(table_name))
    result = cursor.fetchone()
    rowcount, = result
    return rowcount

# print(count_rows('users'))

# add an option to count rows in the table up to a certain limit. This feature might be useful for very large tables
def count_rows(table_name: str, limit: int) -> int:
    stmt = """SELECT COUNT(*) FROM (SELECT 1 FROM {} LIMIT {}) AS limit_query""".format(
            (table_name), (limit))
    cursor= conn.execute(stmt)
    result = cursor.fetchone()

    rowcount, = result
    return rowcount

print(count_rows('users', 10))

conn.commit()
conn.close()