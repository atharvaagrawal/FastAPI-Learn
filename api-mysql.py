from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Atharva@007",
    "database": "ORG",
    "port": "3306"
}


# Connect to MySQL Database
def connect_db():
    try:
        cnx = mysql.connector.connect(**db_config)
        return cnx
    except mysql.connector.Error as err:
        print(err)


# Define Pydantic Models
class Worker(BaseModel):
    worker_id: Optional[int] = None
    first_name: str
    last_name: str
    salary: int
    joining_date: str
    department: str


class UpdateWorker(BaseModel):
    worker_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    salary: Optional[int] = None
    joining_date: Optional[str] = None
    department: Optional[str] = None


""" 
mysql> describe Worker;
+--------------+----------+------+-----+---------+----------------+
| Field        | Type     | Null | Key | Default | Extra          |
+--------------+----------+------+-----+---------+----------------+
| WORKER_ID    | int      | NO   | PRI | NULL    | auto_increment |
| FIRST_NAME   | char(25) | YES  |     | NULL    |                |
| LAST_NAME    | char(25) | YES  |     | NULL    |                |
| SALARY       | int      | YES  |     | NULL    |                |
| JOINING_DATE | datetime | YES  |     | NULL    |                |
| DEPARTMENT   | char(25) | YES  |     | NULL    |                |
+--------------+----------+------+-----+---------+----------------+
 """


@app.get("/get-all")
def get_all_worker():
    cnx = connect_db()
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Worker"
        cursor.execute(query)
        workers = cursor.fetchall()
        return workers
    finally:
        cursor.close()
        cnx.close()


@app.get("/get-by-id/{worker_id}")
def get_by_id(worker_id: int):
    cnx = connect_db()
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT * FROM Worker where worker_id ="+str(worker_id)
        cursor.execute(query)
        workers = cursor.fetchall()
        return workers
    finally:
        cursor.close()
        cnx.close()


@app.post("/create")
def create_worker(worker: Worker):
    cnx = connect_db()
    cursor = cnx.cursor()

    try:
        # Insert record into Worker table
        query = ("INSERT INTO Worker "
                 "(first_name, last_name, salary, joining_date, department) "
                 "VALUES ( %s, %s, %s, %s, %s)")

        # now.strftime('%Y-%m-%d %H:%M:%S')
        values = (worker.first_name, worker.last_name,
                  worker.salary, worker.joining_date, worker.department)
        cursor.execute(query, values)
        cnx.commit()
        return {"Message": "Worker Created Successfully!"}
    except mysql.connector.Error as err:
        cnx.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        cnx.close()


@app.put("/update/{worker_id}")
def update_worker(worker_id: int, worker: UpdateWorker):
    cnx = connect_db()
    cursor = cnx.cursor()

    query = "SELECT * FROM Worker WHERE worker_id=%s"
    cursor.execute(query, (worker_id,))
    result = cursor.fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="Worker not found")

    query = "UPDATE Worker SET "
    columns = []

    if worker.first_name:
        columns.append(f"first_name = '{worker.first_name}'")
    if worker.last_name:
        columns.append(f"last_name = '{worker.last_name}'")
    if worker.salary:
        columns.append(f"salary = {worker.salary}")
    if worker.joining_date:
        columns.append(f"joining_date = '{worker.joining_date}'")
    if worker.department:
        columns.append(f"department = '{worker.department}'")

    if len(columns) == 0:
        raise HTTPException(status_code=400, detail="No fields to update")

    query += ", ".join(columns)
    query += f" WHERE worker_id = {worker_id}"
    cursor.execute(query)
    cnx.commit()

    return {"message": "Worker updated successfully"}


@app.delete("/delete/{worker_id}")
def delete_worker(worker_id: int):
    cnx = connect_db()
    cursor = cnx.cursor()

    try:
        query = "DELETE FROM Worker where worker_id="+str(worker_id)
        cursor.execute(query)
        cnx.commit()

        return {"Message": "Deleted Successfully"}
    except mysql.connector.Error as err:
        cnx.rollback()
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()
        cnx.close()
