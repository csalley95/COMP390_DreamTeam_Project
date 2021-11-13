import sqlite3 as sql
from typing import Tuple
import pandas as pd
import sys


class Course:

    def __init__(self, CourseID, Course_Credits, Course_Description):
        self.Course_ID = CourseID
        self.Course_Credits = Course_Credits
        self.Course_Description = Course_Description

    def addCourse(self, conn: sql.Connection, curs: sql.Cursor):
        curs.execute("""INSERT INTO Course (CourseID, Course_Credits, Course_Description)
                        VALUES (?,?,?)""", (self.Course_ID, self.Course_Credits, self.Course_Description))
        conn.commit()

    #def editCourse(self):