import sqlite3 as lite
con = lite.connect('student_fingerprint.db')

with con:
    cur = con.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()

    for row in rows:
        for place in row:
            print(place)