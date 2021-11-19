import sqlite3 as sql
class Student:

    def __init__(self, studentID, studentName, conn: sql.Connection, curs: sql.Cursor):
        self.studentID = studentID
        self.studentName = studentName
        self.conn = conn
        self.curs = curs

    def addStudent(self):
        self.curs.execute("""INSERT INTO Student (studentID, studentName)
                                        VALUES (?,?)""", (self.studentID, self.studentName))
        self.conn.commit()

    def removeStudent(self):
        sql_update_query = """DELETE FROM Student WHERE studentID = ?"""
        data = (self.studentID)
        self.curs.execute(sql_update_query, data)
        self.conn.commit()