import sqlite3 as sql

class Section:

    def __init__(self, sectionID, instructor, conn: sql.Connection, curs: sql.Cursor):
        self.sectionID = sectionID
        self.instructor = instructor
        self.conn = conn
        self.curs = curs

    def addInstructorToSection(self):
        CHECK_instructorID = self.curs.execute("""SELECT instructorID FROM instructor WHERE instructorID = ? """), (self.instructorID)
        CHECK_sectionID = self.curs.execute("""SELECT sectionID FROM Section WHERE sectionID = ? """), (self.sectionID)

        if (CHECK_instructorID != False) and (CHECK_sectionID != False):
            self.curs.execute("""INSERT INTO Section (instructorID, sectionID)
                                                             VALUES (?,?,?)""", (self.studentID, self.sectionID))
            self.conn.commit()

    def removeInstructorFromSection(self):

        self.curs.execute("""DELETE FROM Section WHERE instructorID = ?, sectionID = ? """),\
                                                                         (self.insturctorID, self.sectionID)
        self.conn.commit()

    def addSection(self):
        sectionID_form, sectionID_exists = self.valid_sectionID()
        if sectionID_form == 0 and sectionID_exists == 0:
            self.curs.execute("""INSERT INTO Section (SectionID, Instructor_Name)
                                VALUES (?,?)""", (self.sectionID, self.instructor_Name))
            self.conn.commit()
        return sectionID_form, sectionID_exists

    def removeSection(self):
        sql_update_query = """DELETE FROM Section WHERE sectionID = ?"""
        data = self.sectionID,
        self.curs.execute(sql_update_query, data)
        self.conn.commit()

