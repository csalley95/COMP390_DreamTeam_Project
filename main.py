import sqlite3 as sql
from typing import Tuple
import pandas as pd
import sys

import GUI
from Student import Student
from Instructor import Instructor
from Course import Course
from Section import Section
from Enrollment import Enrollment




def main():
    conn, curs = open_db('NorthStarProject.db')

    #test_select(curs, """SELECT * FROM Course WHERE CourseID = 'DRM150' """)

    app = GUI.QApplication(sys.argv)
    window = GUI.MainWindow(conn, curs)
    window.show()
    sys.exit(app.exec_())

    #close_db(conn)


def open_db(filename: str) -> Tuple[sql.Connection, sql.Cursor]:
    db_connection = sql.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor

def close_db(connection: sql.Connection):
    connection.close()


def test_select(curs: sql.Cursor, testString: str):  # Use this to test select statements
    curs.execute(testString)
    data = curs.fetchall()
    print(data)

main()
