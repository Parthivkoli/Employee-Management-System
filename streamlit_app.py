import streamlit as st
import sqlite3
import pandas as pd

# Set up the page metadata
st.set_page_config(
    page_title="Employee Management System 👩‍💼👨‍💼",
    page_icon=":guardsman:",  # You can replace this with any emoji or image
    layout="wide",  # This makes the layout more spacious
    initial_sidebar_state="expanded"
)

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
            st.error("❌ An error occurred while inserting data: " + str(e))
            return False

    def delete_employee(self, employee_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

def main():
    # Add title and description
    st.title("Employee Management System 👩‍💼👨‍💼")
    st.markdown("## Manage employee records with ease. Add, delete, and view employee details.")

    # Sidebar with app info
    with st.sidebar:
        st.subheader("📚 About This App")
        st.write("""
            This app allows you to manage employees in a simple way. You can:
            - Add new employees ➕
            - Delete existing employees by ID 🗑️
            - View the full list of employees in a table 📊
        """)
        st.write("Developed by Parthiv Koli 🧑‍💻")

    db_manager = DatabaseManager()

    # Input fields for employee details
    st.subheader("👤 Employee Details")
    col1, col2 = st.columns([1, 3])  # Using columns to better organize the layout

    with col1:
        id = st.text_input("ID", placeholder="Enter employee ID")
    with col2:
        name = st.text_input("Name", placeholder="Enter employee name")
    
    age = st.text_input("Age", placeholder="Enter employee age")
    role = st.selectbox("Role", ["Manager 👩‍💼", "Developer 👨‍💻", "Designer 🎨"])

    # Buttons for actions
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("Save 💾"):
            if id and name and age and role:
                if db_manager.insert_employee((id, name, age, role)):
                    st.success("✅ Employee added successfully!")
            else:
                st.error("❌ Please fill all fields.")

    with col4:
        if st.button("Delete 🗑️"):
            if id:
                db_manager.delete_employee(id)
                st.success("✅ Employee deleted successfully!")
            else:
                st.error("❌ Please enter an ID to delete.")

    # Display employees
    st.subheader("📋 Employee List")
    employees = db_manager.get_employees()
    if employees:
        df = pd.DataFrame(employees, columns=["ID", "Name", "Age", "Role"])
        st.dataframe(df)
    else:
        st.warning("⚠️ No employees found.")

if __name__ == "__main__":
    main()
