# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions, arguments, returns, and classes with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   ABelhumeur, 11/19/2023, Began Assignment06
#   ABelhumeur, 11/21/2023, Program Polish
# ------------------------------------------------------------------------------------------ #

# Import Libraries
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ''  # Hold the choice made by the user.


# ---------- Classes ---------- #

class FileProcessor:

    @staticmethod
    def read_data_from_file(file_name: str) -> list[dict[str, str, str]]:
        """
        This function reads JSON information from the specified file.
        :param file_name: A string indicating the specified file name.
        :return: Return the roster of student data currently saved to the file.
        """
        file: TextIO = None
        student_data: list[dict[str, str, str]] = []
        try:
            file = open(file_name, 'r')
            student_data = json.load(file)
            for student_row in student_data:
                print(f'{student_row['first_name']} {student_row['last_name']}, {student_row['course']}')
        except FileNotFoundError as e:
            IO.output_error_message("Text file not found", e)
            IO.output_error_message("Creating file since it doesn't exist")
            file = open(file_name, 'w')
            json.dump(student_data, file)
        except Exception as e:
            IO.output_error_message("Unhandled exception", e)
        finally:
            if not file.closed:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list[dict[str, str, str]]) -> bool:
        """
        This function saves all entered data to the JSON file without erasing existing entries.
        :param file_name: A string indicating the specified file name.
        :param student_data: The roster of student data currently waiting to be saved to the file.
        :return: Returns a boolean to say if the data was successfully written to the file or not.
        """
        file = None
        try:
            file = open(file_name, 'w')
            json.dump(student_data, file, indent=1)
            file.close()
            print("All entries have been saved to the file 'Enrollments.json'.")
            return True
        except TypeError as e:
            IO.output_error_message('JSON data was malformed', e)
        except Exception as e:
            IO.output_error_message('Unhandled exception while writing to JSON file.', e)
        finally:
            if not file.closed:
                file.close()
        return False


class IO:

    @staticmethod
    def output_error_message(message: str, exception: Exception = None):
        """
        This function displays error messaging should an exception get called.
        :param message: Prints a string for custom error messaging or explaining how errors are addressed in
        the case of an exception.
        :param exception: If there is an exception error, this parameter will print technical information.
        If there is no error, it will do nothing. By default, there is no error.
        """
        print(message)
        if exception is not None:
            print('---Technical Information---')
            print(exception, exception.__doc__, type(exception), sep='\n')

    @staticmethod
    def input_menu_choice(menu: str) -> str:
        """
        This function inputs the user's menu selection of either 1, 2, 3, or 4.
        :param menu: This variable is a string value that is the user's input.
        :return: Return the user's input.
        """
        global menu_choice
        menu_choice = input(menu)
        while menu_choice not in ['1', '2', '3', '4']:
            IO.output_error_message("Please enter an option between 1 and 4")
            menu_choice = input(menu)
        return menu_choice

    @staticmethod
    def input_student_data(student_data: list[dict[str, str, str]]) -> list[dict[str, str, str]]:
        """
        Asks the user to input information required for each student, including the student's first name, last name,
        and the name of the course they're registering for, which all gets appended to student_data.
        :param student_data: The roster of all current student data.
        """
        student_first_name: str = ''
        student_last_name: str = ''
        course_name: str = ''
        student_row: dict[str, str, str] = {}
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("First name can only contain alphabetic characters.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("Last name can only contain alphabetic characters.")
            course_name = input("Enter the name of the course: ")
            student_row = {'first_name': student_first_name, 'last_name': student_last_name, 'course': course_name}
            student_data.append(student_row)
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_message("User entered invalid information.", e)
        except Exception as e:
            IO.output_error_message("Unhandled exception", e)
        return student_data

    @staticmethod
    def output_student_courses(student_data: list[dict[str, str, str]]) -> None:
        """
        Displays all entered student data, showing the names of students and what course they are registered for.
        :param student_data: The roster of student data.
        :return: Returns nothing.
        """
        print("-" * 50)
        for student_row in student_data:
            student_first_name = student_row['first_name']
            student_last_name = student_row['last_name']
            course_name = student_row['course']
            print(
                f"Student {student_row['first_name']} {student_row['last_name']} is enrolled in {student_row['course']}")
        print("-" * 50)


# ---------- Program: Present and Process Data ---------- #

students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

while True:
    menu_choice = IO.input_menu_choice(MENU)
    if menu_choice == '1':
        students = IO.input_student_data(student_data=students)
    elif menu_choice == '2':
        IO.output_student_courses(student_data=students)
    elif menu_choice == '3':
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
    elif menu_choice == '4':
        break
    else:
        print("I did not understand that command.")

print("Program Ended")
