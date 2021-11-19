import sqlite3 as sql
class Instructor:

    def __init__(self, instructorID, instructorName, conn: sql.Connection, curs: sql.Cursor):
        self.instructorID = instructorID
        self.instructorName = instructorName
        self.conn = conn
        self.curs = curs

    def addInstructor(self):
        self.curs.execute("""INSERT INTO Instructor (instructorID, instructorName)
                                VALUES (?,?)""", (self.instructorID, self.instructorName))
        self.conn.commit()

    def removeInstructor(self):
        sql_update_query = """DELETE FROM Instructor WHERE instuctorID = ?"""
        data = (self.instructorID)
        self.curs.execute(sql_update_query, data)
        self.conn.commit()