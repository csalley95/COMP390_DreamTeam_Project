import sqlite3 as sql
class Enrollment:

    def __init__(self, enrollmentID, studentID, sectionID, courseID, conn: sql.Connection, curs: sql.Cursor):
        self.enrollmentID = enrollmentID
        self.studentID = studentID
        self.sectionID = sectionID
        self.courseID = courseID
        self.conn = conn
        self.curs = curs


    def addStudentToSection(self):
        #check through the individual foreign tables for values
        CHECK_studentID = self.curs.execute("""SELECT studentID FROM Student WHERE studentID = ? """), (self.studentID)
        CHECK_sectionID = self.curs.execute("""SELECT sectionID FROM Section WHERE sectionID = ? """), (self.sectionID)
        CHECK_courseID = self.curs.execute("""SELECT courseID FROM Course WHERE courseID = ? """), (self.courseID)

        #if they exist add the entries to enrollment  table
        if (CHECK_studentID != False) and (CHECK_sectionID != False) and (CHECK_courseID != False):
            self.curs.execute("""INSERT INTO Enrollment (studentID, sectionID, courseID)
                                                             VALUES (?,?,?)""", (self.studentID, self.sectionID, self.courseID))
            self.conn.commit()


    def removeStudentFromSection(self):

        self.curs.execute("""DELETE FROM Enrollment WHERE studentID = ?, sectionID = ? , courseID = ? """),\
                                                                         (self.studentID, self.sectionID, self.courseID)

        self.conn.commit()


    #def addFlag(self):

    #def removeFlag(self):

