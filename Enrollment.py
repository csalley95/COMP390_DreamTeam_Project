import sqlite3 as sql
class Enrollment:

    def __init__(self, StudentID, CourseID, SectionID, conn: sql.Connection, curs: sql.Cursor):
        self.Over_Capacity = 0
        self.Over_Credits = 0
        self.StudentID = StudentID
        self.CourseID = CourseID
        self.SectionID = SectionID
        self.CourseSectionID = f'{self.CourseID}-{self.SectionID}'
        self.conn = conn
        self.curs = curs
        self.studentID_exists = 0
        self.sectionID_exists = 0

    def addStudentToSection(self):
        # check for valid studentID and sectionID
        self.check_CourseSectionID_StudentID()

        if self.studentID_exists == 1 and self.sectionID_exists == 1:
            self.addFlag()

            self.curs.execute("""INSERT INTO Enrollment (CouseID, SectionID, StudentID, Over_Credit_Flag, Over_Capacity_Flag)
                                                    VALUES (?,?,?,?,?)""", (self.CourseID, self.SectionID, self.StudentID, self.Over_Credits, self.Over_Capacity))
            self.conn.commit()

        return self.studentID_exists, self.sectionID_exists, self.Over_Credits, self.Over_Capacity

    def removeStudentFromSection(self):
        # check for valid studentID and sectionID
        self.check_CourseSectionID_StudentID()

        if self.studentID_exists == 1 and self.sectionID_exists == 1:
            sql_delete_query = """DELETE FROM Enrollment WHERE StudentID = ? AND CouseID = ? AND SectionID = ?"""
            data = self.StudentID, self.CourseID, self.SectionID
            self.curs.execute(sql_delete_query, data)
            self.conn.commit()

        return self.studentID_exists, self.sectionID_exists


    def addFlag(self):
        credit_limit = 18
        enrolled_credits = 0

        # credit flag
        credit_query = """SELECT Course_Credits, StudentID FROM Enrollment INNER JOIN Course ON Course.CourseID = Enrollment.CouseID"""
        self.curs.execute(credit_query)
        credits_per_course_enrolled = self.curs.fetchall()

        for i in credits_per_course_enrolled:
            if i[1] == self.StudentID:
                enrolled_credits += i[0]

        # get credits of course trying to be enrolled
        check_credit_query = """SELECT Course_Credits FROM Course WHERE CourseID = ?"""
        data = self.CourseID,
        self.curs.execute(check_credit_query, data)
        course_credits = self.curs.fetchone()

        tentative_credits = enrolled_credits + course_credits[0]
        if tentative_credits > credit_limit:
            self.Over_Credits = 1

        # capacity flag
        capacity_query = """SELECT Section_Capacity FROM Course_Section WHERE CourseSectionID = ?"""
        data = self.CourseSectionID,
        self.curs.execute(capacity_query, data)
        section_capacity = self.curs.fetchone()

        enrolled_in_section_query = """SELECT COUNT(*) FROM Enrollment WHERE CouseID = ? AND SectionID = ?"""
        data = self.CourseID, self.SectionID
        self.curs.execute(enrolled_in_section_query, data)
        enrolled_in_section = self.curs.fetchall()[0][0]
        print(enrolled_in_section)

        if enrolled_in_section >= section_capacity[0]:
            self.Over_Capacity = 1

    def removeFlag(self):
        print()


    def check_CourseSectionID_StudentID(self):
        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Course_Section WHERE CourseSectionID = ?)"""
        data = self.CourseSectionID,
        self.curs.execute(check_exists_query, data)
        if self.curs.fetchone()[0] == 1:
            self.sectionID_exists = 1

        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Student WHERE StudentID = ?)"""
        data = self.StudentID,
        self.curs.execute(check_exists_query, data)
        if self.curs.fetchone()[0] == 1:
            self.studentID_exists = 1


    def check_student_flags(self):
        find_flags_query = """SELECT Over_Credit_Flag, Over_Capacity_Flag FROM Enrollment WHERE StudentID = ?"""
        data = self.StudentID,
        self.curs.execute(find_flags_query, data)
        flags_found = self.curs.fetchall()

