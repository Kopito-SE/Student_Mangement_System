import json
from typing import Dict, List
DATA_FILE = "students.json"

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
        s.subjects = data.get("subjects", {})
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
    def add_marks(self,student_id:str,subject:str,mark:float):
        if student_id not in self.students:
            raise KeyError("Student not found")

        self.students[student_id].add_marks(subject,mark)
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
        return List(self.students.values())

