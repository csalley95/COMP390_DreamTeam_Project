import sqlite3
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QRadioButton, QPushButton, QFrame


class MainWindow(QMainWindow):

    def __init__(self, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.conn = conn
        self.curs = curs
        super().__init__()

        #  main menu
        self.student_menu_button = QPushButton(self)
        self.faculty_menu_button = QPushButton(self)
        self.course_menu_button = QPushButton(self)

        # sub menu
        self.student_menu = StudentMenu(self)
        self.faculty_menu = FacultyMenu(self)
        self.course_menu = CourseMenu(self)

        self.setup_ui()  # needs to be at end of constructor

    def setup_ui(self):
        self.setWindowTitle('NorthStar Registration System')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        # button setup section
        self.student_menu_button.setText("Students")
        self.student_menu_button.resize(150, 50)
        self.student_menu_button.move(50, 200)
        self.student_menu_button.clicked.connect(self.open_student_menu)

        self.faculty_menu_button.setText("Faculty")
        self.faculty_menu_button.resize(150, 50)
        self.faculty_menu_button.move(50, 300)
        self.faculty_menu_button.clicked.connect(self.open_faculty_menu)

        self.course_menu_button.setText("Courses")
        self.course_menu_button.resize(150, 50)
        self.course_menu_button.move(50, 400)
        self.course_menu_button.clicked.connect(self.open_course_menu)

    def open_student_menu(self):
        self.hide()
        self.student_menu.show()

    def open_faculty_menu(self):
        self.hide()
        self.faculty_menu.show()

    def open_course_menu(self):
        self.hide()
        self.course_menu.show()



class StudentMenu(QMainWindow):

    def __init__(self, parent=None):
        super(StudentMenu, self).__init__(parent)
        self.setWindowTitle('NorthStar Registration System/Student')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.resize(150, 50)
        self.back_button.move(50, 200)
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        MainWindow.show(self)
        self.hide()

class FacultyMenu(QMainWindow):

    def __init__(self, parent=None):
        super(FacultyMenu, self).__init__(parent)
        self.setWindowTitle('NorthStar Registration System/Faculty')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)


class CourseMenu(QMainWindow):

    def __init__(self, parent=None):
        super(CourseMenu, self).__init__(parent)
        self.setWindowTitle('NorthStar Registration System/Course')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)