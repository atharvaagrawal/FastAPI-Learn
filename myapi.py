from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1: {
        "name": "Atharva",
        "age": 20,
        "year": "3rd Year"
    }
}


@app.get("/")
def index():
    return {"name": "First Data"}


# Path Parameter
# gt(Greater Than) parameter
# lt(Less Than)
@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(description="The ID of the student you want to view", gt=0)):
    return students[student_id]


# Query Parameter
# = None to make it optional
@app.get("/get-by-name")
def get_student(name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not Found"}


# Request Body and Post Method
class Student(BaseModel):
    name: str
    age: int
    year: str


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student Exists"}

    students[student_id] = student
    return students[student_id]


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not Exists"}

    if student.name != None:
        students[student_id].name = student.name

    if student.age != None:
        students[student_id].age = student.age

    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student Does Not Exists"}

    del students[student_id]
    return {"Message": "Student Deleted Successfully!"}
