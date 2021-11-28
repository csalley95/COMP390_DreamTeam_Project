import sqlite3 as sql


class Instructor:

    def __init__(self, instructorID, instructor_Name, conn: sql.Connection, curs: sql.Cursor):
        self.instructorID = instructorID
        self.instructor_Name = instructor_Name
        self.conn = conn
        self.curs = curs

    def addInstructor(self):
        instructorID_form, instructorID_exists = self.valid_instructorID()
        if instructorID_form == 0 and instructorID_exists == 0:
            self.curs.execute("""INSERT INTO Instructor (InstructorID, Instructor_Name)
                                VALUES (?,?)""", (self.instructorID, self.instructor_Name))
            self.conn.commit()
        return instructorID_form, instructorID_exists

    def removeInstructor(self):
        check_exists_query = """SELECT EXISTS(SELECT 1 FROM instructor WHERE instructorID = ? )"""
        data = self.instructorID,
        self.curs.execute(check_exists_query, data)
        if self.curs.fetchone()[0] == 1:
            self.instructorID_exists = 1
            sql_update_query = """DELETE FROM Instructor WHERE InstructorID = ?"""
            data = self.instructorID,
            self.curs.execute(sql_update_query, data)
            self.conn.commit()
        else:
            self.instructorID_exists = 0

        return self.instructorID_exists

    def valid_instructorID(self):
        self.instructorID_form = 0
        self.instructorID_exists = 0

        if len(str(self.instructorID)) == 8:
            for i in range(len(str(self.instructorID))):
                if not str(self.instructorID)[i].isdigit():
                    self.instructorID_form = 1
                    break
        else:
            self.instructorID = 1

        check_exists_query = """SELECT EXISTS(SELECT 1 FROM instructor WHERE instructorID = ? )"""
        data = self.instructorID,
        self.curs.execute(check_exists_query, data)
        # only commits if instructor doesnt already exist
        if self.curs.fetchone()[0] == 1:
            self.instructorID_exists = 1

        return self.instructorID_form, self.instructorID_exists