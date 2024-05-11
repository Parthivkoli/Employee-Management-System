import tkinter as tk
from tkinter import ttk, messagebox, filedialog, END
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
            messagebox.showerror(title="Error", message="An error occurred while inserting data: " + str(e))
            return False

    def delete_employee(self, employee_id):
        self.cursor.execute("DELETE FROM employees WHERE id=?", (employee_id,))
        self.conn.commit()

    def get_employees(self):
        self.cursor.execute("SELECT * FROM employees")
        return self.cursor.fetchall()

class CustomTkinterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Employee Management System")
        self.geometry("1000x600")  # Set window size
        self.config(bg="#f0f0f0")  # Set background color

        # Initialize DatabaseManager
        self.db_manager = DatabaseManager()

        # Set custom fonts
        self.base_font_size = 12
        self.font1 = ("Arial", int(self.base_font_size * 1.5), "bold")
        self.font2 = ("Arial", int(self.base_font_size * 1.2))
        self.font3 = ("Arial", int(self.base_font_size * 1.1))

        # Create custom frame
        self.frame1 = tk.Frame(self, bg="#f0f0f0")
        self.frame1.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9, anchor=tk.NW)

        # Create frame for entry fields and buttons
        self.left_frame = tk.Frame(self.frame1, bg="#f0f0f0")
        self.left_frame.place(relx=0, rely=0, relwidth=0.4, relheight=1, anchor=tk.NW)

        # Labels
        tk.Label(self.left_frame, text="ID:", font=self.font1, bg='#f0f0f0', fg='#333').grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.left_frame, text="Name:", font=self.font1, bg="#f0f0f0", fg="#333").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.left_frame, text="Age:", font=self.font1, bg="#f0f0f0", fg="#333").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.left_frame, text="Role:", font=self.font1, bg="#f0f0f0", fg="#333").grid(row=3, column=0, padx=10, pady=5, sticky="e")

        # Entry fields
        self.id_entry = tk.Entry(self.left_frame, font=self.font2, bg="#fff", fg="#333", width=25)
        self.id_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.name_entry = tk.Entry(self.left_frame, font=self.font2, bg="#fff", fg="#333", width=25)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.age_entry = tk.Entry(self.left_frame, font=self.font2, bg="#fff", fg="#333", width=25)
        self.age_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.role_entry = tk.Entry(self.left_frame, font=self.font2, bg="#fff", fg="#333", width=25)
        self.role_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Buttons
        self.save_button = tk.Button(self.left_frame, text="Save", font=self.font1, fg="#fff", bg="#4CAF50", command=self.insert, width=10)
        self.save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.clear_button = tk.Button(self.left_frame, text="Clear", font=self.font1, fg="#fff", bg="#f44336", command=self.clear, width=10)
        self.clear_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.delete_button = tk.Button(self.left_frame, text="Delete", font=self.font1, fg="#fff", bg="#2196F3", command=self.delete, width=10)
        self.delete_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Add Import and Export buttons
        self.import_button = tk.Button(self.left_frame, text="Import", font=self.font1, fg="#fff", bg="#FF9800", command=self.import_data, width=10)
        self.import_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.export_button = tk.Button(self.left_frame, text="Export", font=self.font1, fg="#fff", bg="#607D8B", command=self.export_data, width=10)
        self.export_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create separator between left and right frames
        self.separator = ttk.Separator(self.frame1, orient="vertical")
        self.separator.place(relx=0.4, rely=0, relheight=1)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.frame1, style="mystyle.Treeview", columns=("ID", "Name", "Age", "Role"), show="headings")
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.tree.heading("Age", text="Age", anchor=tk.CENTER)
        self.tree.heading("Role", text="Role", anchor=tk.CENTER)
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.CENTER)
        self.tree.column("Age", width=100, anchor=tk.CENTER)
        self.tree.column("Role", width=150, anchor=tk.CENTER)
        self.tree.place(relx=0.5, rely=0, relwidth=0.5, relheight=1, anchor=tk.NW)

        # Configure tag for font color
        self.tree.tag_configure("colored", foreground="#000000")  # Change font color to black

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", font=self.font3, rowheight=int(self.base_font_size * 2), background="#fff", foreground="#333", highlightthickness=1, highlightcolor="#ccc", selectbackground="#f0f0f0")
        self.style.configure("mystyle.Treeview.Heading", font=self.font2, background="#4CAF50", foreground="#000000")  # Change header font color to black

        self.display_data()

        # Bind treeview click event
        self.tree.bind("<ButtonRelease-1>", self.get_data)

        # Bind window resize event
        self.bind("<Configure>", self.resize_fonts)

        # Save data when window is closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Add menu
        self.create_menu()

    def export_data(self):
        filename = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if filename:
            data = []
            for item in self.tree.get_children():
                data.append(self.tree.item(item)["values"][:4])  # Limit to the first 4 columns
            df = pd.DataFrame(data, columns=["ID", "Name", "Age", "Role"])
            if filename.endswith(".xlsx"):
                df.to_excel(filename, index=False)
            elif filename.endswith(".csv"):
                df.to_csv(filename, index=False)

    def import_data(self):
        filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if filename:
            try:
                if filename.endswith(".xlsx"):
                    df = pd.read_excel(filename)
                elif filename.endswith(".csv"):
                    df = pd.read_csv(filename)

                # Clear existing data
                self.db_manager.cursor.execute("DELETE FROM employees")
                self.db_manager.conn.commit()

                # Add new columns dynamically
                for column in df.columns:
                    if column.lower() not in ['id', 'name', 'age', 'role']:
                        self.db_manager.cursor.execute(f"ALTER TABLE employees ADD COLUMN '{column}' TEXT")
                self.db_manager.conn.commit()

                # Insert imported data into the database
                for index, row in df.iterrows():
                    details = tuple(row)
                    self.db_manager.insert_employee(details)

                # Refresh displayed data
                self.display_data()

            except Exception as e:
                messagebox.showerror(title="Error", message=f"An error occurred: {str(e)}")

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export Data", command=self.export_data)
        file_menu.add_command(label="Import Data", command=self.import_data)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.db_manager.conn.commit()  # Commit any pending changes to the database
            self.db_manager.conn.close()  # Close database connection
            self.destroy()

    def resize_fonts(self, event):
        # Adjust font sizes based on window dimensions
        window_width = event.width
        window_height = event.height
        font_size = min(window_width, window_height) // 50
        self.base_font_size = font_size
        self.font1 = ("Arial", int(self.base_font_size * 1.5), "bold")
        self.font2 = ("Arial", int(self.base_font_size * 1.2))
        self.font3 = ("Arial", int(self.base_font_size * 1.1))

        # Update font styles
        self.style.configure("mystyle.Treeview", font=self.font3, rowheight=int(self.base_font_size * 2))
        self.style.configure("mystyle.Treeview.Heading", font=self.font2)

        # Update font for labels, entries, and buttons
        for widget in self.left_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(font=self.font1)
            elif isinstance(widget, tk.Entry):
                widget.config(font=self.font2)
            elif isinstance(widget, tk.Button):
                widget.config(font=self.font1)

    def insert(self):
        if self.id_entry.get() == "" or self.name_entry.get() == "" or self.age_entry.get() == "" or self.role_entry.get() == "":
            messagebox.showerror(title="Error", message="Please Enter All The Data.")
        else:
            details = (self.id_entry.get(), self.name_entry.get(), self.age_entry.get(), self.role_entry.get())
            self.db_manager.insert_employee(details)
            self.display_data()

    def delete(self):
        selected_row = self.tree.focus()
        if not selected_row:
            messagebox.showerror(title="Error", message="Please select a row to delete.")
            return
        employee_id = self.tree.item(selected_row)["values"][0]
        self.db_manager.delete_employee(employee_id)
        self.display_data()
        self.clear()

    def get_data(self, event):
        selected_row = self.tree.focus()
        if not selected_row:
            return
        data = self.tree.item(selected_row)
        row = data["values"]
        self.clear()
        self.id_entry.insert(0, row[0])
        self.name_entry.insert(0, row[1])
        self.age_entry.insert(0, row[2])
        self.role_entry.insert(0, row[3])

    def display_data(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.db_manager.get_employees():
            # Apply "colored" tag to Role column
            self.tree.insert("", tk.END, values=row, tags=("colored" if row[3] == "Manager" else ""))

    def clear(self):
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.age_entry.delete(0, END)
        self.role_entry.delete(0, END)

if __name__ == "__main__":
    app = CustomTkinterApp()
    app.mainloop()
