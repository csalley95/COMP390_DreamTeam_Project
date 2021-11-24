import sqlite3 as sql


class Section:

    def __init__(self, CourseID, SectionNumber, InstructorID, Section_Capacity, conn: sql.Connection, curs: sql.Cursor):
        self.CourseID = CourseID
        self.SectionID = SectionNumber
        self.InstructorID = InstructorID
        self.Section_Capacity = Section_Capacity
        self.conn = conn
        self.curs = curs

        self.CourseSectionID = f"{CourseID}-{SectionNumber}"

    def addInstructorToSection(self):
        CHECK_instructorID = self.curs.execute("""SELECT instructorID FROM instructor WHERE instructorID = ? """), (
            self.instructorID)
        CHECK_sectionID = self.curs.execute("""SELECT sectionID FROM Section WHERE sectionID = ? """), (self.sectionID)

        if (CHECK_instructorID != False) and (CHECK_sectionID != False):
            self.curs.execute("""INSERT INTO Section (instructorID, sectionID)
                                                             VALUES (?,?,?)""", (self.studentID, self.sectionID))
            self.conn.commit()

    def removeInstructorFromSection(self):

        self.curs.execute("""DELETE FROM Section WHERE instructorID = ?, sectionID = ? """), \
        (self.insturctorID, self.sectionID)
        self.conn.commit()

    def addSection(self):
        courseID_exists, sectionID_form, sectionID_exists, instructorID_exists, section_capacity_form \
            = self.valid_section()
        if courseID_exists == 1 and sectionID_form == 0 and sectionID_exists == 0 and instructorID_exists == 1:
            self.curs.execute("""INSERT INTO Course_Section (CourseSectionID, CourseID, SectionID, Section_Capacity, InstructorID)
                                VALUES (?,?,?,?,?)""", (self.CourseSectionID, self.CourseID, self.SectionID,
                                                        self.Section_Capacity, self.InstructorID))
            self.conn.commit()
        return courseID_exists, sectionID_form, sectionID_exists, instructorID_exists, section_capacity_form

    def removeSection(self):
        sql_update_query = """DELETE FROM Section WHERE sectionID = ?"""
        data = self.CourseSectionID,
        self.curs.execute(sql_update_query, data)
        self.conn.commit()

    def valid_section(self):
        self.sectionID_exists = 0
        self.sectionID_form = 0
        self.courseID_exists = 0
        self.instructorID_exists = 0
        self.section_capacity_form = 0

        # checking if sectionID is right form
        if len(self.SectionID) != 3:
            self.sectionID_form = 1
        else:
            for i in range(3):
                if self.SectionID[i].isalpha():
                    self.sectionID_form = 1
                    break

        # check for valid courseID
        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Course WHERE  CourseID = ?) """
        data = self.CourseID,
        self.curs.execute(check_exists_query, data)
        if self.curs.fetchone()[0] == 1:
            self.courseID_exists = 1

        # check if sectionID already exists given courseID exists
        if self.courseID_exists == 1:
            # check if sectionID already exists
            check_exists_query = """SELECT EXISTS(SELECT 1 FROM Course_Section WHERE CourseID = ? AND SectionID = ?) """
            data = self.CourseID, self.SectionID
            self.curs.execute(check_exists_query, data)
            # only commits if course doesnt already exist
            if self.curs.fetchone()[0] == 1:
                self.sectionID_exists = 1

        # check if valid instructor given
        if self.InstructorID != 'N/A':
            check_exists_query = """SELECT EXISTS(SELECT 1 FROM Instructor WHERE InstructorID = ?)"""
            data = self.InstructorID,
            self.curs.execute(check_exists_query, data)
            if self.curs.fetchone()[0] == 1:
                self.instructorID_exists = 1
        else:
            self.instructorID_exists = 1

        # check for valid section_capacity
        for i in range(len(self.Section_Capacity)):
            if not self.Section_Capacity[i].isdigit():
                self.section_capacity_form = 1

        return self.courseID_exists, self.sectionID_form, self.sectionID_exists, self.instructorID_exists, self.section_capacity_form
