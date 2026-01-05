import pymysql
from tkinter import messagebox

conn = None
mycursor = None

def connect_database():
    global conn, mycursor
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='Prachi@61',
            database='employee_data'
        )
        mycursor = conn.cursor()
    except:
        messagebox.showerror('Error', 'MySQL is not running')
        return

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS data (
            Id VARCHAR(20) PRIMARY KEY,
            Name VARCHAR(50),
            Phone VARCHAR(15),
            Role VARCHAR(50),
            Gender VARCHAR(20),
            Salary DECIMAL(10,2)
        )
    """)

def insert(id, name, phone, role, gender, salary):
    try:
        mycursor.execute(
            "INSERT INTO data VALUES (%s,%s,%s,%s,%s,%s)",
            (id, name, phone, role, gender, salary)
        )
        conn.commit()
    except pymysql.IntegrityError:
        messagebox.showerror('Error', f'Employee ID "{id}" already exists')

def fetch_all():
    mycursor.execute("SELECT * FROM data")
    return mycursor.fetchall()

def update_employee(id, name, phone, role, gender, salary):
    mycursor.execute("""
        UPDATE data SET Name=%s, Phone=%s, Role=%s, Gender=%s, Salary=%s WHERE Id=%s
    """, (name, phone, role, gender, salary, id))
    conn.commit()

def delete_employee(id):
    mycursor.execute("DELETE FROM data WHERE Id=%s", (id,))
    conn.commit()

def delete_all():
    mycursor.execute("DELETE FROM data")
    conn.commit()
