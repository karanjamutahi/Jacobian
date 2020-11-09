import sqlite3 as lite
#from typing import ContextManager
con = lite.connect('student_fingerprint.db')

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()
    content = ""

    for row in rows:
        for place in row:
            content = content + " " + str(place)
        print(content)
