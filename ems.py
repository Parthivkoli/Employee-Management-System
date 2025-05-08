import streamlit as st
import sqlite3
import pandas as pd
import re
import io
from openpyxl import Workbook

# Set up the page metadata
st.set_page_config(
    page_title="Employee Management System",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DatabaseManager:
    def __init__(self, db_name='employee.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.recreate_table()

    def recreate_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS employees")
        self.cursor.execute('''CREATE TABLE employees
                              (id TEXT PRIMARY KEY, name TEXT, age INTEGER, role TEXT)''')
        self.conn.commit()

    def get_column_names(self):
        self.cursor.execute("PRAGMA table_info(employees)")
        return [info[1] for info in self.cursor.fetchall()]

    def insert_employee(self, details):
        try:
            self.cursor.execute("INSERT INTO employees (id, name, age, role) VALUES (?, ?, ?, ?)", details)
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_employee(self, id, details):
        try:
            self.cursor.execute("UPDATE employees SET name=?, age=?, role=? WHERE id=?", 
                               (details[1], details[2], details[3], id))
            self.conn.commit()
            return self.conn.total_changes > 0
        except sqlite3.Error:
            return False

    def delete_employee(self, employee_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        self.conn.commit()
        return self.conn.total_changes > 0

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

    def search_employees(self, query):
        query = f"%{query}%"
        self.cursor.execute("SELECT * FROM employees WHERE name LIKE ? OR id LIKE ?", (query, query))
        return self.cursor.fetchall()

def normalize_column_name(col):
    col = col.lower().strip()
    mapping = {
        'id': ['id', 'employee id', 'emp id', 'identifier'],
        'name': ['name', 'employee name', 'full name', 'person'],
        'age': ['age', 'years', 'employee age'],
        'role': ['role', 'position', 'job title', 'title', 'occupation']
    }
    for standard, variations in mapping.items():
        if col in variations or col.replace(' ', '') in [v.replace(' ', '') for v in variations]:
            return standard
    return col

def validate_inputs(id, name, age, role):
    errors = []
    if not id or not isinstance(id, str) or not re.match(r'^[a-zA-Z0-9-]+$', id):
        errors.append("ID must be non-empty and alphanumeric (hyphens allowed).")
    if not name or not isinstance(name, str) or len(name.strip()) < 2:
        errors.append("Name must be at least 2 characters long.")
    try:
        age = int(age)
        if not (18 <= age <= 100):
            errors.append("Age must be a number between 18 and 100.")
    except (ValueError, TypeError):
        errors.append("Age must be a valid number.")
    if not role or not isinstance(role, str):
        errors.append("Role must be specified.")
    return errors

def validate_imported_data(df):
    expected_columns = ["id", "name", "age", "role"]
    # Normalize column names
    df.columns = [normalize_column_name(col) for col in df.columns]
    
    # Check for required columns
    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        return False, [f"Missing required columns: {', '.join(missing_cols)}"], df
    
    # Keep only the required columns
    df = df[expected_columns]
    
    # Clean data
    df = df.fillna('')  # Replace NaN with empty string
    df['id'] = df['id'].astype(str).str.strip()
    df['name'] = df['name'].astype(str).str.strip()
    df['role'] = df['role'].astype(str).str.strip()
    
    errors = []
    valid_rows = []
    statuses = []
    for index, row in df.iterrows():
        row_errors = validate_inputs(row['id'], row['name'], row['age'], row['role'])
        if row_errors:
            errors.append(f"Row {index + 1}: {', '.join(row_errors)}")
            statuses.append(f"Failed: {', '.join(row_errors)}")
        else:
            valid_rows.append((row['id'], row['name'], int(row['age']), row['role']))
            statuses.append("Success")
    
    df['Status'] = statuses
    return valid_rows, errors, df

def main():
    # Load custom CSS
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("<style>body {font-family: Arial, sans-serif;}</style>", unsafe_allow_html=True)

    # Title and description
    st.title("Employee Management System")
    st.markdown("A modern system to manage employee records efficiently.")

    # Sidebar
    with st.sidebar:
        st.header("About")
        # Styled name with custom class
        st.markdown('<p class="developer-name">Parthiv Koli</p>', unsafe_allow_html=True)
        st.markdown("""
            This app provides a robust interface to:
            - Add new employees ➕
            - Update employee details ✏️
            - Delete employees 🗑️
            - Search employees 🔍
            - Import and export employee data 📊
        """)
        # Profile section
        st.markdown("### Developer Profile")
        st.markdown("""
            <div class="profile-links">
                <p><span class="icon">🌐</span> <a href="https://github.com/Parthivkoli" target="_blank">GitHub</a></p>
                <p><span class="icon">💼</span> <a href="https://www.linkedin.com/in/parthiv-koli" target="_blank">LinkedIn</a></p>
            </div>
        """, unsafe_allow_html=True)

    db_manager = DatabaseManager()
    columns = db_manager.get_column_names()
    expected_columns = ["id", "name", "age", "role"]
    if columns != expected_columns:
        st.warning(f"Database schema mismatch. Expected columns: {expected_columns}, Found: {columns}")

    # Tabs for different functionalities
    tab1, tab2, tab3, tab4 = st.tabs(["Manage Employees", "View & Search", "Export Data", "Import Data"])

    with tab1:
        st.subheader("Manage Employee Records")
        with st.form("employee_form"):
            col1, col2 = st.columns(2)
            with col1:
                id = st.text_input("Employee ID", placeholder="e.g., EMP-123", help="Unique alphanumeric ID")
            with col2:
                name = st.text_input("Name", placeholder="e.g., John Doe")

            col3, col4 = st.columns(2)
            with col3:
                age = st.text_input("Age", placeholder="e.g., 30")
            with col4:
                role_options = ["Manager", "Developer", "Designer", "Custom Role"]
                role = st.selectbox("Role", role_options)
                if role == "Custom Role":
                    role = st.text_input("Custom Role", placeholder="e.g., Analyst")

            submitted = st.form_submit_button("Save Employee")
            if submitted:
                errors = validate_inputs(id, name, age, role)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    employee_data = (id, name, int(age), role)
                    if db_manager.insert_employee(employee_data):
                        st.success("Employee added successfully!")
                    else:
                        st.error("Failed to add employee. ID may already exist.")

        st.subheader("Update or Delete Employee")
        update_id = st.text_input("Enter ID to Update/Delete", key="update_id")
        if update_id:
            employees = db_manager.search_employees(update_id)
            if employees:
                emp = employees[0]
                with st.form("update_form"):
                    u_name = st.text_input("Name", value=emp[1])
                    u_age = st.text_input("Age", value=str(emp[2]))
                    u_role = st.selectbox("Role", ["Manager", "Developer", "Designer", "Custom Role"], 
                                         index=role_options.index(emp[3]) if emp[3] in role_options else 0)
                    if u_role == "Custom Role":
                        u_role = st.text_input("Custom Role", value=emp[3])

                    col5, col6 = st.columns(2)
                    with col5:
                        if st.form_submit_button("Update"):
                            errors = validate_inputs(update_id, u_name, u_age, u_role)
                            if errors:
                                for error in errors:
                                    st.error(error)
                            else:
                                if db_manager.update_employee(update_id, (update_id, u_name, int(u_age), u_role)):
                                    st.success("Employee updated successfully!")
                                else:
                                    st.error("Failed to update employee.")
                    with col6:
                        if st.form_submit_button("Delete"):
                            if db_manager.delete_employee(update_id):
                                st.success("Employee deleted successfully!")
                            else:
                                st.error("Failed to delete employee. ID not found.")
            else:
                st.warning("No employee found with this ID.")

    with tab2:
        st.subheader("Employee List")
        search_query = st.text_input("Search by Name or ID", placeholder="Type to search...")
        employees = db_manager.search_employees(search_query) if search_query else db_manager.get_employees()
        if employees:
            df = pd.DataFrame(employees, columns=columns)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No employees found.")

    with tab3:
        st.subheader("Export Employee Data")
        employees = db_manager.get_employees()
        if employees:
            df = pd.DataFrame(employees, columns=columns)

            # Export as CSV
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="employees.csv",
                mime="text/csv"
            )

            # Export as Excel
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            st.download_button(
                label="Download as Excel",
                data=excel_buffer,
                file_name="employees.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Export as TXT
            txt = df.to_string(index=False)
            st.download_button(
                label="Download as TXT",
                data=txt,
                file_name="employees.txt",
                mime="text/plain"
            )
        else:
            st.warning("No data to export.")

    with tab4:
        st.subheader("Import Employee Data")
        st.markdown("Upload a file in CSV, Excel, or TXT format. Expected columns: id, name, age, role (case-insensitive, variations accepted).")
        
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "txt"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    try:
                        df = pd.read_csv(uploaded_file, encoding='utf-8')
                    except UnicodeDecodeError:
                        uploaded_file.seek(0)
                        df = pd.read_csv(uploaded_file, encoding='latin1')
                elif uploaded_file.name.endswith('.xlsx'):
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                elif uploaded_file.name.endswith('.txt'):
                    uploaded_file.seek(0)
                    content = uploaded_file.read().decode('utf-8')
                    if '\t' in content:
                        uploaded_file.seek(0)
                        df = pd.read_table(uploaded_file, sep='\t')
                    elif ',' in content:
                        uploaded_file.seek(0)
                        df = pd.read_table(uploaded_file, sep=',')
                    else:
                        uploaded_file.seek(0)
                        df = pd.read_table(uploaded_file, delim_whitespace=True)

                # Validate and import data
                valid_rows, errors, df_with_status = validate_imported_data(df)
                
                # Display editable table
                st.subheader("Edit Imported Data")
                edited_df = st.data_editor(df_with_status.drop(columns=["Status"], errors="ignore"), num_rows="dynamic")
                
                if st.button("Validate and Import"):
                    # Re-validate edited data
                    valid_rows, errors, edited_df_with_status = validate_imported_data(edited_df)
                    
                    # Display updated status
                    st.dataframe(edited_df_with_status, use_container_width=True)
                    
                    # Import valid rows
                    success_count = 0
                    for row in valid_rows:
                        if db_manager.insert_employee(row):
                            success_count += 1
                    
                    if success_count > 0:
                        st.success(f"Successfully imported {success_count} out of {len(edited_df)} records.")
                    if errors:
                        for error in errors:
                            st.error(error)
                    if success_count == 0 and not errors:
                        st.warning("No valid records to import.")
            except Exception as e:
                st.error(f"Error processing file: {str(e)}")

if __name__ == "__main__":
    main()