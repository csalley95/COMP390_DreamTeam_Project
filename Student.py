import sqlite3 as sql


class Student:

    def __init__(self, studentID, studentName, conn: sql.Connection, curs: sql.Cursor):
        self.student_ID = studentID
        self.studentName = studentName
        self.conn = conn
        self.curs = curs

    def addStudent(self):
        studentID_form, studentID_exists = self.valid_studentID()
        if studentID_form == 0 and studentID_exists == 0:
            self.curs.execute("""INSERT INTO Student (studentID, studentName)
                                        VALUES (?,?)""", (self.studentID, self.studentName))
            self.conn.commit()
        return studentID_form, studentID_exists

    def valid_studentID(self):
        self.studentID_form = 0
        self.studentID_exists = 0

        for i in range(3):
            if not self.student_ID[i].isalpha():
                self.studentID_form = 1
                break
        if self.studentID_form == 0:
            for i in range(4, 6):
                if not self.student_ID[i].isdigit():
                    self.studentID_form = 1
                    break

        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Student WHERE studentID = ?) """
        data = self.student_ID,
        self.curs.execute(check_exists_query, data)
        # only commits if course doesnt already exist
        if self.curs.fetchone()[0] == 1:
            self.studentID_exists = 1

        return self.studentID_form, self.studentID_exists

    def removeStudent(self):
        sql_update_query = """DELETE FROM Student WHERE studentID = ?"""
        data = (self.studentID)
        self.curs.execute(sql_update_query, data)
        self.conn.commit()
