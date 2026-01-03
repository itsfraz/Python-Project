# 🎓 Smart Student Result Management System

## 🚀 Project Description

A menu-driven, professional, beginner-friendly Python application built for managing student results. It allows users (teachers/admins) to add student records, calculate grades automatically, and perform various data operations like searching, updating, and deleting records.

## ✨ Features

- **Student Management**: Add students with Roll No, Name, and Marks for 5 subjects.
- **Automatic Calculations**: Automatically calculates Total Marks, Percentage, and Grade (A+, A, B, C, Fail).
- **Data Persistence**: Saves all data to `students_data.json` so records are not lost after closing the program.
- **Search & Filter**: Search for specific students by Roll Number.
- **Report Generation**: View all records in a formatted table or export them to `student_report.txt`.
- **Login System**: Basic authentication (Admin/Password) to secure the system.
- **Input Validation**: Ensures valid marks (0-100) and prevents duplicate Roll Numbers.

## 🛠️ How to Run

### Option 1: CLI Version (Console)

1. Open a terminal/command prompt in the project folder.
2. Run the command:

   ```bash
   python student_result_system.py
   ```

### Option 2: GUI Version (Graphical Interface)

1. Open a terminal/command prompt.
2. Run the command:

   ```bash
   python student_result_system_gui.py
   ```

**Login Details (for both):**

- **Username**: `admin`
- **Password**: `password123`

## 🧠 Code Logic (Viva Q&A)

- **Data Structure**: We use a **List of Dictionaries**. Each student is a dictionary containing keys like `roll_no`, `name`, `marks` (which is another dictionary), `total`, etc.
- **File Handling**: We use the `json` module. `json.load()` reads data from the file into a Python list, and `json.dump()` writes the list back to the file. This is shared between both CLI and GUI versions.
- **Modular Functions**: Each feature (Add, View, Search) is broken down into its own function (e.g., `add_student()`, `search_student()`) to keep the code clean and manageable.
- **Exception Handling**: We use `try-except` blocks to handle errors like missing files or invalid number inputs (e.g., entering text instead of marks).

## 🔮 Future Enhancements

- ✅ **GUI Version**: (Completed) Built using **Tkinter**.
- 🌐 **Web App**: Convert to a web application using **Flask**.
- 📊 **Graphs**: Add performance analysis graphs using `matplotlib`.
- 📄 **PDF Support**: Generate PDF result cards.
