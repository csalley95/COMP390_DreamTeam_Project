import sqlite3 as sql

class Section:

    def __init__(self, sectionID, conn: sql.Connection, curs: sql.Cursor):
        self.sectionID = sectionID

    #def addInstructorToSection(self, instructor):

    #def removeInstructorFromSection(self, instructor):

    #def addSection(self):

    #def removeSection(self):

