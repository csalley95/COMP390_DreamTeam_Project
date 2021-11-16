import sqlite3 as sql
class Instructor:

    def __init__(self, instructorID, instructorName, conn: sql.Connection, curs: sql.Cursor):
        self.instructorID = instructorID
        self.instructorName = instructorName

    #def addInstructor(self):

    #def removeInstructor(self):