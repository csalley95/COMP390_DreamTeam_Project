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
        if courseID_form == 0 and courseID_exists == 0 and self.Course_Credits.isdigit():
            self.curs.execute("""INSERT INTO Course (CourseID, Course_Credits, Course_Description)
                        VALUES (?,?,?)""", (self.Course_ID, self.Course_Credits, self.Course_Description))
            self.conn.commit()
        return courseID_form, courseID_exists, self.Course_Credits.isdigit()

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

        sql_update_query = """Update Course set Course_Credits = ? WHERE CourseID = ?"""
        data = (self.Course_Credits, self.Course_ID)
        self.curs.execute(sql_update_query, data)
        self.conn.commit()

        sql_update_query = """Update Course set Course_Description = ? WHERE CourseID = ?"""
        data = (self.Course_Description, self.Course_ID)
        self.curs.execute(sql_update_query, data)
        self.conn.commit()