import sqlite3 as sql

class Section:

    def __init__(self, sectionID, instructor, conn: sql.Connection, curs: sql.Cursor):
        self.sectionID = sectionID
        self.instructor = instructor
        self.conn = conn
        self.curs = curs


    def addInstructorToSection(self, instructor):
        CHECK_instructorID = self.curs.execute("""SELECT instructorID FROM instructor WHERE instructorID = ? """), (self.instructorID)
        CHECK_instructorName = self.curs.execute("""SELECT instructorName FROM instructor WHERE instructorNameID = ? """), (self.instructorName)


    def removeInstructorFromSection(self, instructor):

        self.curs.execute("""DELETE FROM section WHERE instructorID = ?, instructorName = ? """),\
                                                                         (self.instructorID, self.instructorName)

        self.conn.commit()

    def addSection(self):
        self.curs.execute("""INSERT INTO Section (sectionID, instructor)
                               VALUES (?,?)""", (self.sectionID, self.instructor))
        self.conn.commit()

    def removeSection(self):
        sql_update_query = """DELETE FROM Section WHERE SectionID = ?"""
        data = (self.sectionID)
        self.curs.execute(sql_update_query, data)
        self.conn.commit()
