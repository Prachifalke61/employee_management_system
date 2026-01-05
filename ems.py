from customtkinter import *
from tkinter import ttk, messagebox
import database

# ---------------- CRUD FUNCTIONS ----------------
def add_employee():
    id_val = idEntry.get()
    name_val = nameEntry.get()
    phone_val = phoneEntry.get()
    role_val = roleBox.get()
    gender_val = genderBox.get()
    salary_val = salaryEntry.get()

    if '' in [id_val, name_val, phone_val, salary_val]:
        messagebox.showerror('Error','All fields are required')
        return

    database.insert(id_val, name_val, phone_val, role_val, gender_val, salary_val)
    show_employees()
    clear_entries()

def show_employees():
    for item in tree.get_children():
        tree.delete(item)
    records = database.fetch_all()
    for row in records:
        tree.insert('', END, values=row)

def update_employee():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error','Select employee to update')
        return
    id_val = tree.item(selected,'values')[0]
    database.update_employee(
        id_val,
        nameEntry.get(),
        phoneEntry.get(),
        roleBox.get(),
        genderBox.get(),
        salaryEntry.get()
    )
    show_employees()
    clear_entries()

def delete_employee():
    selected = tree.focus()
    if not selected:
        messagebox.showerror('Error','Select employee to delete')
        return
    id_val = tree.item(selected,'values')[0]
    database.delete_employee(id_val)
    show_employees()
    clear_entries()

def select_employee(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected,'values')
        idEntry.delete(0, END); idEntry.insert(0, values[0])
        nameEntry.delete(0, END); nameEntry.insert(0, values[1])
        phoneEntry.delete(0, END); phoneEntry.insert(0, values[2])
        roleBox.set(values[3])
        genderBox.set(values[4])
        salaryEntry.delete(0, END); salaryEntry.insert(0, values[5])

def clear_entries():
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    salaryEntry.delete(0, END)
    roleBox.set('Web Developer')
    genderBox.set('Male')

# ---------------- GUI ----------------
def start_ems():
    database.connect_database()

    global window
    global idEntry, nameEntry, phoneEntry, salaryEntry, roleBox, genderBox, tree

    set_appearance_mode("dark")
    set_default_color_theme("blue")

    window = CTk()
    window.geometry('1050x600')
    window.title('Employee Management System')
    window.resizable(False, False)

    # Left Frame
    leftFrame = CTkFrame(window, fg_color='#161C30')
    leftFrame.grid(row=0, column=0, padx=20, pady=10, sticky='ns')

    CTkLabel(leftFrame, text='ID', font=('Arial',14,'bold'), text_color='white').grid(row=0,column=0,pady=5)
    idEntry = CTkEntry(leftFrame, width=180); idEntry.grid(row=0,column=1)

    CTkLabel(leftFrame, text='Name', font=('Arial',14,'bold'), text_color='white').grid(row=1,column=0,pady=5)
    nameEntry = CTkEntry(leftFrame, width=180); nameEntry.grid(row=1,column=1)

    CTkLabel(leftFrame, text='Phone', font=('Arial',14,'bold'), text_color='white').grid(row=2,column=0,pady=5)
    phoneEntry = CTkEntry(leftFrame, width=180); phoneEntry.grid(row=2,column=1)

    CTkLabel(leftFrame, text='Role', font=('Arial',14,'bold'), text_color='white').grid(row=3,column=0,pady=5)
    roleBox = CTkComboBox(leftFrame,
        values=['Web Developer','Cloud Architecture','Technical Writer','Network Engineer','DevOps',
                'Data Scientist','Business Analyst','IT Consultant','UI/UX Designer'],
        width=180, state='readonly')
    roleBox.grid(row=3,column=1); roleBox.set('Web Developer')

    CTkLabel(leftFrame, text='Gender', font=('Arial',14,'bold'), text_color='white').grid(row=4,column=0,pady=5)
    genderBox = CTkComboBox(leftFrame, values=['Male','Female'], width=180, state='readonly')
    genderBox.grid(row=4,column=1); genderBox.set('Male')

    CTkLabel(leftFrame, text='Salary', font=('Arial',14,'bold'), text_color='white').grid(row=5,column=0,pady=5)
    salaryEntry = CTkEntry(leftFrame, width=180); salaryEntry.grid(row=5,column=1)

    CTkButton(leftFrame, text='Add', width=160, command=add_employee).grid(row=6,column=0,columnspan=2,pady=5)
    CTkButton(leftFrame, text='Update', width=160, command=update_employee).grid(row=7,column=0,columnspan=2,pady=5)
    CTkButton(leftFrame, text='Delete', width=160, command=delete_employee).grid(row=8,column=0,columnspan=2,pady=5)

    # Right Frame
    rightFrame = CTkFrame(window)
    rightFrame.grid(row=0,column=1,padx=20,pady=10)

    tree = ttk.Treeview(rightFrame, height=25, columns=('Id','Name','Phone','Role','Gender','Salary'), show='headings')
    tree.grid(row=1, column=0, columnspan=4, pady=10)
    for col in ('Id','Name','Phone','Role','Gender','Salary'):
        tree.heading(col, text=col)
        tree.column(col, width=120)
    tree.bind('<ButtonRelease-1>', select_employee)

    show_employees()
    window.mainloop()
