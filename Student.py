import sqlite3 as sql


class Student:

    def __init__(self, studentID, student_Name, conn: sql.Connection, curs: sql.Cursor):
        self.studentID = studentID
        self.student_Name = student_Name
        self.conn = conn
        self.curs = curs

    def addStudent(self):
        studentID_form, studentID_exists = self.valid_studentID()
        if studentID_form == 0 and studentID_exists == 0:
            self.curs.execute("""INSERT INTO Student (studentID, student_Name)
                                        VALUES (?,?)""", (self.studentID, self.student_Name))
            self.conn.commit()
        return studentID_form, studentID_exists

    def valid_studentID(self):
        self.studentID_form = 0
        self.studentID_exists = 0

        for i in range(len(self.studentID)):
            if not self.studentID[i].isdigit():
                self.studentID_form = 1
                break

        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Student WHERE studentID = ? )"""
        data = self.studentID,
        self.curs.execute(check_exists_query, data)
        # only commits if course doesnt already exist
        if self.curs.fetchone()[0] == 1:
            self.studentID_exists = 1

        return self.studentID_form, self.studentID_exists

    def removeStudent(self):
        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Student WHERE studentID = ? )"""
        data = self.studentID,
        self.curs.execute(check_exists_query, data)
        # only commits if course doesnt already exist
        if self.curs.fetchone()[0] == 1:
            self.studentID_exists = 1

            sql_delete_query = """DELETE FROM Student WHERE studentID = ?"""
            data = self.studentID,
            self.curs.execute(sql_delete_query, data)
            self.conn.commit()
        else:
            self.studentID_exists = 0

        return self.studentID_exists
