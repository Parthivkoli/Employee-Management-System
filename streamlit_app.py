import streamlit as st
import sqlite3
import pandas as pd

class DatabaseManager:
    def __init__(self, db_name='employee.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS employees
                              (id INTEGER PRIMARY KEY, name TEXT, age TEXT, role TEXT)''')
        self.conn.commit()

    def insert_employee(self, details):
        try:
            self.cursor.execute("INSERT INTO employees (id, name, age, role) VALUES (?, ?, ?, ?)", details)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            st.error("An error occurred while inserting data: " + str(e))
            return False

    def delete_employee(self, employee_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

def main():
    st.title("Employee Management System")
    db_manager = DatabaseManager()

    # Input fields for employee details
    id = st.text_input("ID")
    name = st.text_input("Name")
    age = st.text_input("Age")
    role = st.selectbox("Role", ["Manager", "Developer", "Designer"])

    # Buttons for actions
    if st.button("Save"):
        if id and name and age and role:
            db_manager.insert_employee((id, name, age, role))
            st.success("Employee added successfully!")
        else:
            st.error("Please fill all fields.")

    if st.button("Delete"):
        if id:
            db_manager.delete_employee(id)
            st.success("Employee deleted successfully!")
        else:
            st.error("Please enter an ID to delete.")

    # Display employees
    st.subheader("Employee List")
    employees = db_manager.get_employees()
    df = pd.DataFrame(employees, columns=["ID", "Name", "Age", "Role"])
    st.dataframe(df)

if __name__ == "__main__":
    main() 