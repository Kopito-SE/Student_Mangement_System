import json
from symtable import Class
from typing import Dict,List

class Student:
    def __init__(self,student_id:int, name:str):
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

class StudentMangement:
    pass