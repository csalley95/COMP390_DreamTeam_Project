import sqlite3
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLineEdit, QMessageBox, QRadioButton, QButtonGroup

from Course import Course
from Instructor import Instructor
from Section import Section
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
        self.enrollment_menu_button = QPushButton(self)

        # sub menu
        self.student_menu = StudentMenu(self, self.conn, self.curs)
        self.faculty_menu = InstructorMenu(self, self.conn, self.curs)
        self.course_menu = CourseMenu(self, self.conn, self.curs)
        self.enrollment_menu = EnrollmentMenu(self, self.conn, self.curs)

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

        self.faculty_menu_button.setText("Instructors")
        self.faculty_menu_button.resize(150, 50)
        self.faculty_menu_button.move(50, 275)
        self.faculty_menu_button.clicked.connect(self.open_faculty_menu)

        self.course_menu_button.setText("Courses")
        self.course_menu_button.resize(150, 50)
        self.course_menu_button.move(50, 350)
        self.course_menu_button.clicked.connect(self.open_course_menu)

        self.enrollment_menu_button.setText("Enrollment")
        self.enrollment_menu_button.resize(150, 50)
        self.enrollment_menu_button.move(50, 425)
        self.enrollment_menu_button.clicked.connect(self.open_enrollment_menu)

    def open_student_menu(self):
        self.hide()
        self.student_menu.show()

    def open_faculty_menu(self):
        self.hide()
        self.faculty_menu.show()

    def open_course_menu(self):
        self.hide()
        self.course_menu.show()

    def open_enrollment_menu(self):
        self.hide()
        self.enrollment_menu.show()


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

        # pop up window
        self.result_msg = QMessageBox(self)
        self.result_msg.setWindowTitle('Results')
        self.result_msg.resize(300, 300)
        self.result_msg.move(400, 300)
        self.result_msg.hide()

    def msg_popup(self, msg: str, icon):
        self.result_msg.setText(msg)
        self.result_msg.setIcon(icon)
        self.result_msg.show()

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
        studentID_form, studentID_exists = student_to_add.addStudent()
        # need to have database check for validity
        if studentID_form == 0 and studentID_exists == 0:
            # confirmation window
            self.msg_popup('Student Successfully Added to Database', QMessageBox.Information)
            self.close_add_student()
        else:
            error_str = 'Errors Detected!'
            if studentID_form == 1:
                error_str = error_str + '\n Invalid StudentID: Incorrect form'
            if studentID_exists == 1:
                error_str = error_str + '\n Invalid StudentID: StudentID already exists'

            self.msg_popup(error_str, QMessageBox.Warning)

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
        student_to_remove.removeStudent()
        # check for validity
        # display confirmation
        confirmation = 'Student removed from Database!'
        self.msg_popup(confirmation, QMessageBox.Information)
        self.close_remove_student()

        # add student doesnt exist error

    def close_remove_student(self):
        self.studentID_entry.close()
        self.remove_student_done.close()
        self.studentID_entry.setText('')
        self.remove_student_open = False


class InstructorMenu(QMainWindow):

    def __init__(self, previous_window, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.previous_window = previous_window
        self.conn = conn
        self.curs = curs
        super(InstructorMenu, self).__init__()
        self.setWindowTitle('NorthStar Registration System/Instructor')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.resize(150, 50)
        self.back_button.move(50, 400)
        self.back_button.clicked.connect(self.go_back)

        # buttons for window
        self.add_instructor_open = False
        self.add_instructor_button = QPushButton(self)
        self.add_instructor_button.setText('Add Instructor')
        self.add_instructor_button.resize(150, 50)
        self.add_instructor_button.move(50, 200)
        self.add_instructor_button.clicked.connect(self.add_instructor)

        self.remove_instructor_open = False
        self.remove_instructor_button = QPushButton(self)
        self.remove_instructor_button.setText('Remove Instructor')
        self.remove_instructor_button.resize(150, 50)
        self.remove_instructor_button.move(50, 250)
        self.remove_instructor_button.clicked.connect(self.remove_instructor)

        self.add_instructor_to_section_open = False
        self.add_instructor_to_section_button = QPushButton(self)
        self.add_instructor_to_section_button.setText('Add to Section')
        self.add_instructor_to_section_button.resize(150, 50)
        self.add_instructor_to_section_button.move(50, 300)
        self.add_instructor_to_section_button.clicked.connect(self.add_instructor_to_section)

        self.remove_instructor_from_section_open = False
        self.remove_instructor_from_section_button = QPushButton(self)
        self.remove_instructor_from_section_button.setText('Remove from Section')
        self.remove_instructor_from_section_button.resize(150, 50)
        self.remove_instructor_from_section_button.move(50, 350)
        self.remove_instructor_from_section_button.clicked.connect(self.remove_instructor_from_section)

        # widgets for add_instructor
        self.instructorID_entry = QLineEdit(self)
        self.instructorID_entry.setPlaceholderText('Instructor ID')
        self.instructorID_entry.resize(280, 40)
        self.instructorID_entry.move(400, 200)
        self.instructorID_entry.hide()

        self.instructor_Name_entry = QLineEdit(self)
        self.instructor_Name_entry.setPlaceholderText('Instructor Name')
        self.instructor_Name_entry.resize(280, 40)
        self.instructor_Name_entry.move(400, 250)
        self.instructor_Name_entry.hide()

        self.courseSectionID_entry = QLineEdit(self)
        self.courseSectionID_entry.setPlaceholderText('Course Section ID')
        self.courseSectionID_entry.resize(280, 40)
        self.courseSectionID_entry.move(400, 250)
        self.courseSectionID_entry.hide()

        self.add_instructor_done = QPushButton(self)
        self.add_instructor_done.setText('Add Instructor')
        self.add_instructor_done.resize(150, 50)
        self.add_instructor_done.move(400, 300)
        self.add_instructor_done.hide()
        self.add_instructor_done.clicked.connect(self.add_instructor_submit)

        # widgets for remove_instructor
        self.remove_instructor_done = QPushButton(self)
        self.remove_instructor_done.setText('Remove Instructor')
        self.remove_instructor_done.resize(150, 50)
        self.remove_instructor_done.move(400, 250)
        self.remove_instructor_done.hide()
        self.remove_instructor_done.clicked.connect(self.remove_instructor_submit)

        # widgets for add_instructor_to_section
        self.add_instructor_to_section_done = QPushButton(self)
        self.add_instructor_to_section_done.setText('Assign Instructor')
        self.add_instructor_to_section_done.resize(150, 50)
        self.add_instructor_to_section_done.move(400, 300)
        self.add_instructor_to_section_done.hide()
        self.add_instructor_to_section_done.clicked.connect(self.add_instructor_to_section_submit)

        # widgets for remove_instructor_from_section
        self.remove_instructor_from_section_done = QPushButton(self)
        self.remove_instructor_from_section_done.setText('Remove Instructor')
        self.remove_instructor_from_section_done.resize(150, 50)
        self.remove_instructor_from_section_done.move(400, 300)
        self.remove_instructor_from_section_done.hide()
        self.remove_instructor_from_section_done.clicked.connect(self.remove_instructor_from_section_submit)

        # pop up window
        self.result_msg = QMessageBox(self)
        self.result_msg.setWindowTitle('Results')
        self.result_msg.resize(300, 300)
        self.result_msg.move(400, 300)
        self.result_msg.hide()

    def msg_popup(self, msg: str, icon):
        self.result_msg.setText(msg)
        self.result_msg.setIcon(icon)
        self.result_msg.show()

    def go_back(self):
        if self.add_instructor_open:
            self.close_add_instructor()
        elif self.remove_instructor_open:
            self.close_remove_instructor()
        elif self.add_instructor_to_section_open:
            self.close_add_instructor_to_section()
        elif self.remove_instructor_from_section_open:
            self.close_remove_instructor_from_section()
        else:
            self.previous_window.show()
            self.hide()

    def add_instructor(self):
        self.add_instructor_open = True
        self.instructorID_entry.show()
        self.instructor_Name_entry.show()
        self.add_instructor_done.show()

    def add_instructor_submit(self):
        instructor_to_add = Instructor(self.instructorID_entry.text().strip(),
                                       self.instructor_Name_entry.text().strip(),
                                       self.conn, self.curs)
        instructorID_form, instructorID_exists = instructor_to_add.addInstructor()
        # need to have database check for validity
        if instructorID_form == 0 and instructorID_exists == 0:
            # confirmation window
            self.msg_popup('Instructor Successfully Added to Database', QMessageBox.Information)
            self.close_add_instructor()
        else:
            error_str = 'Errors Detected!'
            if instructorID_form == 1:
                error_str = error_str + '\n Invalid InstructorID: Incorrect form'
            if instructorID_exists == 1:
                error_str = error_str + '\n Invalid InstructorID: CourseID already exists'

            self.msg_popup(error_str, QMessageBox.Warning)

    def close_add_instructor(self):
        self.instructorID_entry.hide()
        self.instructor_Name_entry.hide()
        self.add_instructor_done.hide()
        self.instructorID_entry.setText('')
        self.instructor_Name_entry.setText('')
        self.add_instructor_open = False

    def remove_instructor(self):
        self.remove_instructor_open = True
        self.instructorID_entry.show()
        self.remove_instructor_done.show()

    def remove_instructor_submit(self):
        instructor_to_remove = Instructor(self.instructorID_entry.text().strip(), 0,
                                          self.conn, self.curs)
        instructor_to_remove.removeInstructor()
        # check for validity
        # display confirmation
        confirmation = 'Instructor removed from Database!'
        self.msg_popup(confirmation, QMessageBox.Warning)
        self.close_remove_instructor()

    def close_remove_instructor(self):
        self.instructorID_entry.hide()
        self.remove_instructor_done.hide()
        self.instructorID_entry.setText('')
        self.remove_instructor_open = False

    def add_instructor_to_section(self):
        self.add_instructor_to_section_open = True
        self.instructorID_entry.show()
        self.courseSectionID_entry.show()
        self.add_instructor_to_section_done.show()

    def add_instructor_to_section_submit(self):
        temp_section = Section(0, 0, 0, 0, self.conn, self.curs)
        courseSection_exists, instructor_exists = temp_section.\
            addInstructorToSection(self.courseSectionID_entry.text().strip(), self.instructorID_entry.text().strip())

        if courseSection_exists == 1 and instructor_exists == 1:
            self.msg_popup('Instructor added to Section', QMessageBox.Information)
            self.close_add_instructor_to_section()
        else:
            error_str = 'Errors Detected!'
            if courseSection_exists != 1:
                error_str = f'{error_str} \n Invalid Course Section ID: Course Section ID does not exist'
            if instructor_exists != 1:
                error_str = f'{error_str} \n Invalid Instructor ID: Instructor ID does not exist'
            self.msg_popup(error_str, QMessageBox.Warning)

    def close_add_instructor_to_section(self):
        self.instructorID_entry.hide()
        self.courseSectionID_entry.hide()
        self.add_instructor_to_section_done.hide()
        self.instructorID_entry.setText('')
        self.courseSectionID_entry.setText('')
        self.add_instructor_to_section_open = False

    def remove_instructor_from_section(self):
        self.remove_instructor_from_section_open = True
        self.instructorID_entry.show()
        self.courseSectionID_entry.show()
        self.remove_instructor_from_section_done.show()

    def remove_instructor_from_section_submit(self):
        temp_section = Section(0, 0, 0, 0, self.conn, self.curs)
        courseSection_exists = temp_section. \
           removeInstructorFromSection(self.courseSectionID_entry.text().strip(), self.instructorID_entry.text().strip())
        if courseSection_exists == 1:
            self.msg_popup('Instructor removed from Section', QMessageBox.Information)
            self.close_add_instructor_from_section()
        else:
            error_str = 'Errors Detected!'
            if courseSection_exists != 1:
                error_str = f'{error_str} \n Invalid Course Section ID: Course Section ID does not exist'
            self.msg_popup(error_str, QMessageBox.Warning)

    def close_remove_instructor_from_section(self):
        self.instructorID_entry.hide()
        self.courseSectionID_entry.hide()
        self.remove_instructor_from_section_done.hide()
        self.instructorID_entry.setText('')
        self.courseSectionID_entry.setText('')
        self.remove_instructor_from_section_open = False


class CourseMenu(QMainWindow):

    def __init__(self, previous_window, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.conn = conn
        self.curs = curs
        self.previous_window = previous_window
        super(CourseMenu, self).__init__()
        self.setWindowTitle('NorthStar Registration System/Course')
        self.setGeometry(400, 200, 1000, 750)
        self.setFixedSize(1000, 750)

        self.back_button = QPushButton(self)
        self.back_button.setText("Back")
        self.back_button.resize(150, 50)
        self.back_button.move(50, 400)
        self.back_button.clicked.connect(self.go_back)

        # buttons for window
        self.add_course_open = False
        self.add_course_button = QPushButton(self)
        self.add_course_button.setText('Add Course')
        self.add_course_button.resize(150, 50)
        self.add_course_button.move(50, 200)
        self.add_course_button.clicked.connect(self.add_course)

        self.edit_course_open = False
        self.edit_course_button = QPushButton(self)
        self.edit_course_button.setText('Edit Course')
        self.edit_course_button.resize(150, 50)
        self.edit_course_button.move(50, 250)
        self.edit_course_button.clicked.connect(self.edit_course)

        self.add_section_open = False
        self.add_section_button = QPushButton(self)
        self.add_section_button.setText('Add Section')
        self.add_section_button.resize(150, 50)
        self.add_section_button.move(50, 300)
        self.add_section_button.clicked.connect(self.add_section)

        self.remove_section_open = False
        self.remove_section_button = QPushButton(self)
        self.remove_section_button.setText('Remove Section')
        self.remove_section_button.resize(150, 50)
        self.remove_section_button.move(50, 350)
        self.remove_section_button.clicked.connect(self.remove_section)

        # widgets for add_course
        self.courseID_entry = QLineEdit(self)
        self.courseID_entry.setPlaceholderText('Course ID')
        self.courseID_entry.resize(280, 40)
        self.courseID_entry.move(400, 200)
        self.courseID_entry.hide()

        self.course_credits_entry = QLineEdit(self)
        self.course_credits_entry.setPlaceholderText('Credits')
        self.course_credits_entry.resize(140, 40)
        self.course_credits_entry.move(400, 300)
        self.course_credits_entry.hide()

        self.course_description_entry = QLineEdit(self)
        self.course_description_entry.setPlaceholderText('Course Description')
        self.course_description_entry.resize(280, 40)
        self.course_description_entry.move(400, 400)
        self.course_description_entry.hide()

        self.add_course_done = QPushButton(self)
        self.add_course_done.setText('Add')
        self.add_course_done.resize(150, 50)
        self.add_course_done.move(400, 500)
        self.add_course_done.hide()
        self.add_course_done.clicked.connect(self.add_course_submit)

        # widgets for edit_course
        self.get_course_info_button = QPushButton(self)
        self.get_course_info_button.setText('Search')
        self.get_course_info_button.resize(150, 50)
        self.get_course_info_button.move(700, 200)
        self.get_course_info_button.hide()
        self.get_course_info_button.clicked.connect(self.get_course_info)

        self.edit_course_done = QPushButton(self)
        self.edit_course_done.setText('Update Course')
        self.edit_course_done.resize(150, 50)
        self.edit_course_done.move(400, 500)
        self.edit_course_done.hide()
        self.edit_course_done.clicked.connect(self.edit_course_submit)

        # widgets for add_section
        self.courseID_entry = QLineEdit(self)
        self.courseID_entry.setPlaceholderText('Course ID')
        self.courseID_entry.resize(280, 40)
        self.courseID_entry.move(400, 200)
        self.courseID_entry.hide()

        self.sectionNumber_entry = QLineEdit(self)
        self.sectionNumber_entry.setPlaceholderText('Section Number')
        self.sectionNumber_entry.resize(280, 40)
        self.sectionNumber_entry.move(400, 250)
        self.sectionNumber_entry.hide()

        self.assign_instructor_yes = QRadioButton(self)
        self.assign_instructor_yes.setText('Yes')
        self.assign_instructor_yes.move(350, 295)
        self.assign_instructor_yes.hide()

        self.assign_instructor_no = QRadioButton(self)
        self.assign_instructor_no.setText('No')
        self.assign_instructor_no.move(350, 310)
        self.assign_instructor_no.setChecked(True)
        self.assign_instructor_no.hide()

        self.assign_instructor_group = QButtonGroup(self)
        self.assign_instructor_group.addButton(self.assign_instructor_yes)
        self.assign_instructor_group.addButton(self.assign_instructor_no)

        self.instructorID_entry = QLineEdit(self)
        self.instructorID_entry.setPlaceholderText('Instructor ID')
        self.instructorID_entry.resize(280, 40)
        self.instructorID_entry.move(400, 300)
        self.instructorID_entry.hide()

        self.sectionCapacity_entry = QLineEdit(self)
        self.sectionCapacity_entry.setPlaceholderText('Course Capacity')
        self.sectionCapacity_entry.resize(280, 40)
        self.sectionCapacity_entry.move(400, 350)
        self.sectionCapacity_entry.hide()

        self.add_section_done = QPushButton(self)
        self.add_section_done.setText('Add Section')
        self.add_section_done.resize(150, 50)
        self.add_section_done.move(400, 400)
        self.add_section_done.hide()
        self.add_section_done.clicked.connect(self.add_section_submit)

        # widgets for remove_section
        self.courseSectionID_entry = QLineEdit(self)
        self.courseSectionID_entry.setPlaceholderText('Course Section ID')
        self.courseSectionID_entry.resize(280, 40)
        self.courseSectionID_entry.move(400, 200)
        self.courseSectionID_entry.hide()

        self.remove_section_done = QPushButton(self)
        self.remove_section_done.setText('Remove Section')
        self.remove_section_done.resize(150, 50)
        self.remove_section_done.move(400, 300)
        self.remove_section_done.hide()
        self.remove_section_done.clicked.connect(self.remove_section_submit)

        # pop up window
        self.result_msg = QMessageBox(self)
        self.result_msg.setWindowTitle('Results')
        self.result_msg.resize(300, 300)
        self.result_msg.move(400, 300)
        self.result_msg.hide()

    def msg_popup(self, msg: str, icon):
        self.result_msg.setText(msg)
        self.result_msg.setIcon(icon)
        self.result_msg.show()

    def go_back(self):
        if self.add_course_open:
            self.close_add_course()
        elif self.edit_course_open:
            self.close_edit_course()
        elif self.add_section_open:
            self.close_add_section()
        elif self.remove_section_open:
            self.close_remove_section()
        else:
            self.previous_window.show()
            self.close()

    def add_course(self):
        self.add_course_open = True
        self.courseID_entry.show()
        self.course_credits_entry.show()
        self.course_description_entry.show()
        self.add_course_done.show()

    def add_course_submit(self):
        course_to_add = Course(self.courseID_entry.text().strip(), self.course_credits_entry.text().strip(),
                               self.course_description_entry.text().strip(),
                               self.conn, self.curs)
        courseID_form, course_ID_exists, valid_credit_value = course_to_add.addCourse()
        # need to have database check for validity
        if courseID_form == 0 and course_ID_exists == 0 and valid_credit_value is True:
            # confirmation window
            self.msg_popup('Course Successfully Added to Database', QMessageBox.Information)
            self.close_add_course()
        else:
            error_str = 'Errors Detected!'
            if courseID_form == 1:
                error_str = error_str + '\n Invalid CourseID: Incorrect form'
            if course_ID_exists == 1:
                error_str = error_str + '\n Invalid CourseID: CourseID already exists'
            if valid_credit_value is False:
                error_str = error_str + '\n Invalid Credit Value: Must be digit'

            self.msg_popup(error_str, QMessageBox.Warning)

    def close_add_course(self):
        self.courseID_entry.hide()
        self.course_credits_entry.hide()
        self.course_description_entry.hide()
        self.add_course_done.hide()
        self.courseID_entry.setText('')
        self.course_credits_entry.setText('')
        self.course_description_entry.setText('')
        self.add_course_open = False

    def edit_course(self):
        self.edit_course_open = True
        self.courseID_entry.show()
        self.get_course_info_button.show()

    def get_course_info(self):
        self.courseID_entry.close()
        self.get_course_info_button.close()
        temp_course = Course(self.courseID_entry.text().strip(), 0, 0, self.conn, self.curs)
        course_ID_form, course_ID_exists = temp_course.valid_courseID()
        if course_ID_form == 0 and course_ID_exists == 1:
            course_to_edit_info = temp_course.getCourse()
            courseID = course_to_edit_info[0]
            self.courseID_entry.setText(courseID)
            credits = str(course_to_edit_info[1])
            self.course_credits_entry.setText(credits)
            description = course_to_edit_info[2]
            self.course_description_entry.setText(description)
            self.course_to_edit = Course(courseID, credits, description, self.conn, self.curs)
            self.courseID_entry.show()
            self.course_credits_entry.show()
            self.course_description_entry.show()
            self.edit_course_done.show()
        else:
            error_str = 'Errors Detected!'
            if course_ID_exists == 0:
                error_str = error_str + '\n Invalid CourseID: CourseID does not exist'
            if course_ID_form == 1:
                error_str = error_str + '\n Invalid CourseID: Incorrect form'
            self.msg_popup(error_str, QMessageBox.Warning)

    def edit_course_submit(self):
        # make sure course credit value is valid entry
        if self.course_credits_entry.text().strip().isdigit():
            self.course_to_edit.Course_Credits = self.course_credits_entry.text().strip()
            self.course_to_edit.Course_Description = self.course_description_entry.text().strip()
            self.course_to_edit.editCourse()
            # confirmation window
            self.msg_popup('Course Successfully Updated In Database', QMessageBox.Information)
            self.close_add_course()
            self.close_edit_course()
        else:
            error_str = 'Errors Detected! \n Invalid Credit Value: Must be digit'
            self.msg_popup(error_str, QMessageBox.Warning)

    def close_edit_course(self):
        self.courseID_entry.hide()
        self.get_course_info_button.hide()
        self.course_credits_entry.hide()
        self.course_description_entry.hide()
        self.edit_course_done.hide()
        self.courseID_entry.setText('')
        self.course_credits_entry.setText('')
        self.course_description_entry.setText('')
        self.edit_course_open = False

    def add_section(self):
        self.add_section_open = True
        self.courseID_entry.show()
        self.sectionNumber_entry.show()
        self.add_section_done.show()
        self.instructorID_entry.show()
        self.assign_instructor_yes.show()
        self.assign_instructor_no.show()
        self.sectionCapacity_entry.show()

    def add_section_submit(self):
        if self.assign_instructor_yes.isChecked():
            section_to_add = Section(self.courseID_entry.text().strip(), self.sectionNumber_entry.text().strip(),
                                     self.instructorID_entry.text().strip(), self.sectionCapacity_entry.text().strip(),
                                     self.conn, self.curs)
        else:
            section_to_add = Section(self.courseID_entry.text().strip(), self.sectionNumber_entry.text().strip(),
                                     'N/A', self.sectionCapacity_entry.text().strip(),
                                     self.conn, self.curs)

        courseID_exists, sectionID_form, sectionID_exists, instructorID_exists, section_capacity_form = section_to_add.addSection()
        # need to have database check for validity
        if courseID_exists == 1 and sectionID_form == 0 and sectionID_exists == 0 and instructorID_exists == 1\
                and section_capacity_form == 0:
            # confirmation window
            self.msg_popup('Section Successfully Added to Database', QMessageBox.Information)
            self.close_add_section()
        else:
            error_str = 'Errors Detected!'
            if courseID_exists == 0:
                error_str = f'{error_str} \n Invalid Course ID: Course ID does not exist'
            if sectionID_form == 1:
                error_str = f'{error_str} \n Invalid Section Number: Incorrect form'
            if sectionID_exists == 1:
                error_str = f'{error_str} \n Invalid Section Number: Section Number already exists'
            if instructorID_exists == 0:
                error_str = f'{error_str} \n Invalid Instructor ID: Instructor ID does not exist '
            if section_capacity_form == 1:
                error_str = f'{error_str} \n Invalid Section Capacity: Section Capacity must be a number greater than 0'

            self.msg_popup(error_str, QMessageBox.Warning)

    def close_add_section(self):
        self.sectionNumber_entry.hide()
        self.instructorID_entry.hide()
        self.courseID_entry.hide()
        self.add_section_done.hide()
        self.assign_instructor_yes.hide()
        self.assign_instructor_no.hide()
        self.sectionCapacity_entry.hide()
        self.courseID_entry.setText('')
        self.sectionNumber_entry.setText('')
        self.instructorID_entry.setText('')
        self.sectionCapacity_entry.setText('')
        self.add_section_open = False

    def remove_section(self):
        self.remove_section_open = True
        self.courseSectionID_entry.show()
        self.remove_section_done.show()

    def remove_section_submit(self):
        section_to_remove = Section(0, 0, 0, 0, self.conn, self.curs)
        # check for validity
        section_deleted = section_to_remove.removeSection(self.courseSectionID_entry.text().strip())
        if section_deleted == 1:
            self.msg_popup('Section removed from Database', QMessageBox.Information)
            self.close_remove_section()
        else:
            self.msg_popup('Invalid Section ID: Section ID does not exist', QMessageBox.Warning)

    def close_remove_section(self):
        self.couseSectionID_entry.close()
        self.remove_section_done.close()
        self.courseSectionID_entry.setText('')
        self.remove_section_open = False


class EnrollmentMenu(QMainWindow):

    def __init__(self, previous_window, conn: sqlite3.Connection, curs: sqlite3.Cursor):
        self.previous_window = previous_window
        super(EnrollmentMenu, self).__init__()
        self.setWindowTitle('NorthStar Registration System/Enrollment')
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
