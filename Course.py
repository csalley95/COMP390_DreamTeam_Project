import sqlite3 as sql
from typing import Tuple
import pandas as pd
import sys


class Course:

    def __init__(self, CourseID, Course_Credits, Course_Description, conn: sql.Connection, curs: sql.Cursor):
        self.Course_ID = CourseID
        self.Course_Credits = Course_Credits
        self.Course_Description = Course_Description
        self.conn = conn
        self.curs = curs

    def addCourse(self):
        courseID_form, courseID_exists = self.valid_courseID()
        if courseID_form == 0 and courseID_exists == 0:
            self.curs.execute("""INSERT INTO Course (CourseID, Course_Credits, Course_Description)
                        VALUES (?,?,?)""", (self.Course_ID, self.Course_Credits, self.Course_Description))
            self.conn.commit()
        return courseID_form, courseID_exists

    def getCourse(self):
        print(self.Course_ID)
        get_course_query = """SELECT * FROM Course WHERE CourseID = ?"""
        data = self.Course_ID,
        self.curs.execute(get_course_query, data)
        course_info = self.curs.fetchone()
        return course_info

    def valid_courseID(self):
        self.courseID_form = 0
        self.courseID_exists = 0

        for i in range(3):
            if not self.Course_ID[i].isalpha():
                self.courseID_form = 1
                break
        if self.courseID_form == 0:
            for i in range(4, 6):
                if not self.Course_ID[i].isdigit():
                    self.courseID_form = 1
                    break

        check_exists_query = """SELECT EXISTS(SELECT 1 FROM Course WHERE CourseID = ?) """
        data = self.Course_ID,
        self.curs.execute(check_exists_query, data)
        # only commits if course doesnt already exist
        if self.curs.fetchone()[0] == 1:
            self.courseID_exists = 1

        return self.courseID_form, self.courseID_exists

    def editCourse(self):
        global field_to_edit
        valid_entry = None
        while (valid_entry != True):
            field_to_edit = input("1) Course Credits 2) Course Description")  # place holder until gui
            if (field_to_edit == 1 or field_to_edit == 2):
                valid_entry = True
        if (field_to_edit == 1):  # edit Course_Credits
            updated_credits = input('Enter credit amount: ')  # place holder until gui
            sql_update_query = """Update Course set Coures_Credits = ? WHERE CourseID = ?"""
            data = (updated_credits, self.Course_ID)
            self.curs.execute(sql_update_query, data)
            self.conn.commit()
        elif (field_to_edit == 2):  # edit Course_Description
            updated_description = input('Enter new Course Description: ')  # place holder until gui
            sql_update_query = """Update Course set Coures_Description = ? WHERE CourseID = ?"""
            data = (updated_description, self.Course_ID)
            self.curs.execute(sql_update_query, data)
            self.conn.commit()
