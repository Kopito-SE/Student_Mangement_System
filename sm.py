import json
from typing import Dict, List
DATA_FILE = "students.json"
SUBJECTS= [
    "SAD",
    "MIS",
    "Web Tech",
    "Client-Side",
    "Prob & Stats"
    "Calculus"
    "DBMS"

]

class Student:
    def __init__(self,student_id:str, name:str):
        self.student_id = student_id
        self.name = name
        self.subjects:Dict[str,float] = {}
    def add_marks(self,subject:str,marks:float):

        if not 0<= marks <=100:
            raise ValueError("Marks should exceed 0 but not more than 100")
        self.subjects[subject] = marks

    def average(self) -> float:

        if not self.subjects:
            return 0.0
        return sum(self.subjects.values()) / len(self.subjects)


    def grade(self) -> str:
        avg = self.average()
        if avg >= 70:
            return "A"
        elif avg >= 60:
            return "B"
        elif avg >= 50:
            return "C"
        elif avg >= 40:
            return "D"
        else:
            return "FAIL"

    def to_dict(self) -> dict:
        return{
            "student_id":self.student_id,
            "name":self.name,
            "subjects":self.subjects
        }
    @staticmethod
    def from_dict(data: dict) -> "Student" :
        s = Student(data["student_id"],data["name"])
        s.subjects = data.get("subjects",{})
        return s

class StudentManager:
    def __init__(self):
        self.students:Dict[str,Student] = {}
        self.load()

    def add_student(self, student_id:str , name: str):
        if student_id in self.students:
            raise ValueError(f"Student ID {student_id} already exist")
        self.students[student_id] = Student(student_id, name)
        self.save()
    def add_marks(self,student_id:str,subject:str,marks:float):
        if student_id not in self.students:
            raise KeyError("Student not found")

        self.students[student_id].add_marks(subject,marks)
        self.save()
    def save(self):
        #Save all students to JSON file
        with open(DATA_FILE, "w") as f:
            json.dump({sid: s.to_dict() for sid,s in self.students.items()}, f,indent=4)
    def load(self):
        #Load Students from JSON File
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.students = {sid:Student.from_dict(sd) for sid, sd in data.items()}
        except FileNotFoundError:
            self.students = {}
    def list_students(self)-> List[Student]:
        #Return all students as a list
        return list(self.students.values())
#---Delete and Search student by ID features--
    def get_student(self,student_id:str)-> Student:
        if student_id not in self.students:
            raise KeyError(f"Student ID {student_id} not found")
        return self.students[student_id]
    def delete_student(self,student_id:str):
        if student_id not in self.students:
            raise KeyError("Student ID doesnt Exist")
        del self.students[student_id]
        self.save()


#----------MENU/USER INTERFACE---------
def get_float(prompt:str) -> float:
    '''Safely gets a float user input'''
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("❌ please enter a valid input")

def display_student(s: Student):
    print("*"* 40)
    print(f"ID    : {s.student_id}")
    print(f"NAME  : {s.name}")
    print("SUBJECT")
    if not s.subjects:
        print("NONE")
    else:
        for subject, marks in s.subjects.items():
            print(f"{subject:<15} : {marks}")
    print(f"Average : {s.average():2f}")
    print(f"Grade: {s.grade()}")
    print("="* 40)


def menu():
    manager = StudentManager()
    while True:
        print("====Student Management System===")
        print("1:Add Student")
        print("2:Add Subject And Marks")
        print("3:View all Students")
        print("4:Search Student by ID")
        print("5:Delete student")
        print("6:Exit")

        choice = input("Chose an Option :")
        if choice == "1":
            # Get valid student_id
            while True:
                student_id = input("Enter Student ID:")
                if len(student_id) == 16:
                    break
                print("Invalid ID! Must be 16 characters")

            # Get valid name
            while True:
                name = input("Enter Student Name:")
                if len(name) > 0:  # Valid name (not empty)
                    break
                print("Name cannot be empty")

            # Only reaches here if BOTH are valid
            try:
                manager.add_student(student_id, name)
                print(f"✅ {name} added successfully")
            except ValueError as e:
                print(f"❌ {e}")


        elif choice == "2":
            student_id = input("Enter Student ID:")
            try:
                student = manager.get_student(student_id)
            except ValueError as e:
                print(f"❌ , {e}")
                continue
            print("Enter marks for the Seven(7) subjects")
            for  subject in SUBJECTS:
                # Skip subject if already recorded
                if subject in student.subjects:
                    print(f"{subject} already recorded({student.subjects[subject]})")
                    continue

                marks = get_float(f"Enter {subject} marks (0-100):")
                try:
                    manager.add_marks(student_id, subject, marks)
                except ValueError as e:
                    print(f"❌ {e}")


            print("Marks Entry complete")

        elif choice == "3":
            students = manager.list_students()
            if not students:
                print("No student Found")
            for s in students:
                print("*" * 40)
                print(f"ID:{s.student_id}")
                print(f"NAME:{s.name}")
                print(f"SUBJECTS:{s.subjects}")
                print(f"AVERAGE : {s.average():.2f}")
                print(f"GRADE:{s.grade()}")

        elif choice == "4":
            student_id = input("Enter Student ID:")
            try:
                student= manager.get_student(student_id)
                display_student(student)
            except KeyError as e:
                print(f"❌ {e}")

        elif choice == "5":
            student_id = input("Enter Student ID to Delete:")
            try:
                manager.delete_student(student_id)
                print("Student Deleted Successfully")
            except KeyError as e:
                print(f"❌ {e}")


        elif choice == "6":
            print("Goodbye👋")
            break
        else:
            print("❌ Invalid Choice . Try Again")


if __name__ == "__main__":
    menu()





