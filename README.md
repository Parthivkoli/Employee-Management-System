# Employee Management System 👥

Welcome to the **Employee Management System (EMS)** — a modern, user-friendly web application for managing employee data efficiently. Ideal for HR teams, startups, and small businesses, EMS simplifies everything from hiring to exporting reports. 🚀

---

## ✨ Features

- **🌐 Streamlit-Powered Interface**: Built with a sleek UI inspired by [this Figma dashboard](https://www.figma.com/community/file/994627233772773456/employer-management-dashboard-sass-freebie).
- **🔍 Search & View**: Easily browse, search, and filter employee records in a responsive, tabular layout.
- **➕ Add / ✏️ Edit / ❌ Delete**: Manage employee records with just a few clicks.
- **📁 Import & Export**: 
  - Import from `.xlsx`, `.csv`, or `.txt`
  - Inline editing of imported data before saving
  - Export to Excel, CSV, or plain text
- **🌓 Light/Dark Mode**: Toggle between light and dark themes based on your preference.
- **✅ Data Validation**: Ensures accurate entries — age between 18–100, unique IDs, and clean formatting.

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Streamlit** – UI framework
- **SQLite** – Local data storage
- **Pandas** – Data handling
- **OpenPyXL** – Excel file processing
- **Custom CSS** – Modern, responsive styling via `style.css`

---

## 🚀 Getting Started

Follow these steps to run EMS locally:

```bash
# 1. Clone the repository
git clone https://github.com/Parthivkoli/Employee-Management-System.git
cd Employee-Management-System

# 2. (Optional) Set up a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
````

Then open your browser at `http://localhost:8501`.

---

## 🌐 Live Demo

Try it online with zero setup!
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ems-pro.streamlit.app/)

---

## 📸 Screenshots

### 🖥️ Modern Streamlit UI

![Streamlit UI](https://github.com/user-attachments/assets/22dfe301-8373-4749-9088-a09e1dd65bca)

### 🧱 Legacy Tkinter Version

![Tkinter UI](https://github.com/Parthivkoli/Employee-Management-System/assets/89799632/bd97b8e1-24d8-4c13-88ac-caddac2062a6)

---

## 📁 Project Structure

```
Employee-Management-System/
├── app.py              # Main Streamlit app
├── style.css           # Custom styling
├── requirements.txt    # Python dependencies
├── employee.db         # SQLite database (auto-generated)
└── README.md           # You're reading this!
```

---

## 🤝 Contributing

Want to make this better? Awesome! Here's how:

1. **Fork** this repo
2. **Create** your feature branch (`git checkout -b feature/new-feature`)
3. **Commit** your changes (`git commit -m "Add new feature"`)
4. **Push** to the branch (`git push origin feature/new-feature`)
5. **Create a Pull Request**

Need ideas or want to report bugs? Check out [issues](https://github.com/Parthivkoli/Employee-Management-System/issues) 🐛

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 About the Developer

Hi, I’m **Parthiv Koli** — a Python developer passionate about building smart, simple tools that solve real-world problems. Feel free to connect!

* [GitHub](https://github.com/Parthivkoli)
* [LinkedIn](https://www.linkedin.com/in/parthiv-koli)

---

## 🌟 Acknowledgments

* Huge thanks to [Streamlit](https://streamlit.io/) for making web apps fun and fast.
* UI inspired by this [Figma design](https://www.figma.com/community/file/994627233772773456/employer-management-dashboard-sass-freebie).
* Emoji assets from [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet).

---

⭐ **Star this repo** if you found it helpful — let's simplify employee management together! 🌈

