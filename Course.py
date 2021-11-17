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
        self.curs.execute("""INSERT INTO Course (CourseID, Course_Credits, Course_Description)
                        VALUES (?,?,?)""", (self.Course_ID, self.Course_Credits, self.Course_Description))
        self.conn.commit()

    def getCourse(self):
        self.curs.execute("""SELECT * FROM Course WHERE CourseID = ?, self.CourseID""")
        course_info = self.curs.fetchone()
        return course_info

    def editCourse(self):
        global field_to_edit
        valid_entry = None
        while(valid_entry != True):
            field_to_edit = input("1) Course Credits 2) Course Description")  # place holder until gui
            if(field_to_edit == 1 or field_to_edit == 2):
                valid_entry = True
        if(field_to_edit == 1):  # edit Course_Credits
            updated_credits = input('Enter credit amount: ')  # place holder until gui
            sql_update_query = """Update Course set Coures_Credits = ? WHERE CourseID = ?"""
            data = (updated_credits, self.Course_ID)
            self.curs.execute(sql_update_query, data)
            self.conn.commit()
        elif(field_to_edit == 2):  # edit Course_Description
            updated_description = input('Enter new Course Description: ')  # place holder until gui
            sql_update_query = """Update Course set Coures_Description = ? WHERE CourseID = ?"""
            data = (updated_description, self.Course_ID)
            self.curs.execute(sql_update_query, data)
            self.conn.commit()


