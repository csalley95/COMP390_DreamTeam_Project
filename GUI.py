import sqlite3
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit

from Student import Student


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
        self.student_menu = StudentMenu(self, self.conn, self.curs)
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

    def __init__(self, previous_window, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.conn = conn
        self.curs = curs
        self.previous_window = previous_window
        super(StudentMenu, self).__init__()
        self.setWindowTitle('NorthStar Registration System/Student')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        # create buttons for window
        self.add_student_open = False
        self.add_student_button = QPushButton(self)
        self.remove_student_open = False
        self.remove_student_button = QPushButton(self)
        self.back_button = QPushButton(self)

        # add student buttons/text boxes
        self.studentID_entry = QLineEdit(self)
        self.studentID_entry.setPlaceholderText('StudentID')
        self.studentID_entry.move(400, 200)
        self.studentID_entry.resize(280, 40)
        self.studentID_entry.hide()

        self.studentName_entry = QLineEdit(self)
        self.studentName_entry.setPlaceholderText('Student Name')
        self.studentName_entry.move(400, 300)
        self.studentName_entry.resize(280, 40)
        self.studentName_entry.hide()

        self.add_student_done = QPushButton(self)
        self.add_student_done.setText('Done')
        self.add_student_done.move(400, 400)
        self.add_student_done.resize(150, 50)
        self.add_student_done.clicked.connect(self.add_student_submit)
        self.add_student_done.hide()

        # remove student boxes/text boxes
        self.studentID_entry = QLineEdit(self)
        self.studentID_entry.setPlaceholderText('StudentID')
        self.studentID_entry.move(400, 200)
        self.studentID_entry.resize(280, 40)
        self.studentID_entry.hide()

        self.remove_student_done = QPushButton(self)
        self.remove_student_done.setText('Remove')
        self.remove_student_done.move(400, 400)
        self.remove_student_done.resize(150, 50)
        self.remove_student_done.clicked.connect(self.remove_student_submit)
        self.remove_student_done.hide()

        # set up buttons for window
        self.back_button.setText("Back")
        self.back_button.resize(150, 50)
        self.back_button.move(50, 300)
        self.back_button.clicked.connect(self.go_back)

        self.add_student_button.setText('Add Student')
        self.add_student_button.resize(150, 50)
        self.add_student_button.move(50, 200)
        self.add_student_button.clicked.connect(self.add_student)

        self.remove_student_button.setText('Remove Student')
        self.remove_student_button.resize(150, 50)
        self.remove_student_button.move(50, 250)
        self.remove_student_button.clicked.connect(self.remove_student)

    def go_back(self):
        if self.add_student_open:
            self.close_add_student()
        elif self.remove_student_open:
            self.close_remove_student()
        else:
            self.previous_window.show()
            self.close()

    def add_student(self):
        self.add_student_open = True
        self.studentID_entry.show()
        self.studentName_entry.show()
        self.add_student_done.show()

    def add_student_submit(self):
        student_to_add = Student(self.studentID_entry.text().strip(), self.studentName_entry.text().strip(),
                                 self.conn, self.curs)
        # student_to_add.addStudent()
        # need to have database check for validity
        # display confirmation screen
        self.close_add_student()

    def close_add_student(self):
        self.studentID_entry.close()
        self.studentName_entry.close()
        self.add_student_done.close()
        self.studentID_entry.setText('')
        self.studentName_entry.setText('')
        self.add_student_open = False

    def remove_student(self):
        self.remove_student_open = True
        self.studentID_entry.show()
        self.remove_student_done.show()

    def remove_student_submit(self):
        student_to_remove = Student(self.studentID_entry.text().strip(), 0,
                                 self.conn, self.curs)
        # student_to_remove.removeStudent()
        # check for validity
        # display confirmation
        self.close_remove_student()

    def close_remove_student(self):
        self.studentID_entry.close()
        self.remove_student_done.close()
        self.studentID_entry.setText('')
        self.remove_student_open = False


class FacultyMenu(QMainWindow):

    def __init__(self, previous_window):
        self.previous_window = previous_window
        super(FacultyMenu, self).__init__()
        self.setWindowTitle('NorthStar Registration System/Faculty')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.resize(150, 50)
        self.back_button.move(50, 200)
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        self.previous_window.show()
        self.hide()


class CourseMenu(QMainWindow):

    def __init__(self, previous_window):
        self.previous_window = previous_window
        super(CourseMenu, self).__init__()
        self.setWindowTitle('NorthStar Registration System/Course')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.resize(150, 50)
        self.back_button.move(50, 200)
        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        self.previous_window.show()
        self.hide()
