import sqlite3 as sql
class Student:

    def __init__(self, studentID, studentName, conn: sql.Connection, curs: sql.Cursor):
        self.studentID = studentID
        self.studentName = studentName

    #def addStudent(self):

    #def removeStudent(self):