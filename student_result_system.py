import json
import os
import sys
import time

# ==========================================
# 🎓 Smart Student Result Management System
# ==========================================
# Author: Senior Python Engineer
# Description: A menu-driven console application for managing student results.
#              Suitable for first-year college assignments.

# 📁 File to store student data persistently
DATA_FILE = "students_data.json"

# 🔐 Default Login Credentials (for demonstration)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

def clear_screen():
    """Clears the console screen for better UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_data():
    """Loads student data from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []  # Return empty list if file doesn't exist
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_data(students):
    """Saves student data to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(students, file, indent=4)
        print("✅ Data saved successfully!")
    except IOError as e:
        print(f"❌ Error saving data: {e}")

def calculate_grade(percentage):
    """Calculates grade based on percentage."""
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    elif percentage >= 50: return "D"
    else: return "Fail"

def get_valid_marks(subject_name):
    """Helper to get valid marks input (0-100)."""
    while True:
        try:
            marks = float(input(f"   Enter marks for {subject_name} (0-100): "))
            if 0 <= marks <= 100:
                return marks
            print("   ⚠️ Marks must be between 0 and 100.")
        except ValueError:
            print("   ⚠️ Invalid input. Please enter a number.")

def add_student(students):
    """Adds a new student record."""
    print("\n--- ➕ Add New Student ---")
    
    while True:
        roll_no = input("   Enter Roll Number: ").strip()
        if not roll_no:
            print("   ⚠️ Roll Number cannot be empty.")
            continue
        
        # Check for duplicate roll number
        if any(s['roll_no'] == roll_no for s in students):
            print("   ⚠️ Student with this Roll Number already exists!")
            return
        break

    name = input("   Enter Student Name: ").strip()
    
    print("   📝 Enter Marks for 5 Subjects:")
    subjects = ["Matches", "Physics", "Chemistry", "English", "Computer Science"]
    marks_dict = {}
    total_marks = 0
    
    for subject in subjects:
        mark = get_valid_marks(subject)
        marks_dict[subject] = mark
        total_marks += mark
    
    percentage = (total_marks / 500) * 100
    grade = calculate_grade(percentage)
    
    student = {
        "roll_no": roll_no,
        "name": name,
        "marks": marks_dict,
        "total": total_marks,
        "percentage": round(percentage, 2),
        "grade": grade
    }
    
    students.append(student)
    save_data(students)
    print(f"\n✅ Student {name} added successfully with Grade {grade}!")
    input("\nPress Enter to continue...")

def view_students(students):
    """Displays all student records."""
    clear_screen()
    print("\n--- 📋 All Student Records ---\n")
    if not students:
        print("   No records found.")
    else:
        print(f"{'Roll No':<10} | {'Name':<20} | {'Total':<8} | {'%':<6} | {'Grade':<5}")
        print("-" * 60)
        for s in students:
            print(f"{s['roll_no']:<10} | {s['name']:<20} | {s['total']:<8} | {s['percentage']:<6} | {s['grade']:<5}")
    
    input("\nPress Enter to continue...")

def search_student(students):
    """Searches for a student by Roll Number."""
    print("\n--- 🔍 Search Student ---")
    roll_no = input("   Enter Roll Number to search: ").strip()
    
    found = False
    for s in students:
        if s['roll_no'] == roll_no:
            print("\n   🎓 Student Found!")
            print(f"   Name: {s['name']}")
            print(f"   Roll No: {s['roll_no']}")
            print("   --- Marks ---")
            for sub, mark in s['marks'].items():
                print(f"   {sub}: {mark}")
            print(f"   ----------------")
            print(f"   Total: {s['total']}/500")
            print(f"   Percentage: {s['percentage']}%")
            print(f"   Grade: {s['grade']}")
            found = True
            break
    
    if not found:
        print(f"   ❌ Student with Roll No {roll_no} not found.")
    input("\nPress Enter to continue...")

def update_student(students):
    """Updates student details."""
    print("\n--- ✏️ Update Student ---")
    roll_no = input("   Enter Roll Number to update: ").strip()
    
    for s in students:
        if s['roll_no'] == roll_no:
            print(f"   Updating record for {s['name']}...")
            
            # Update name (optional)
            new_name = input(f"   Enter New Name (current: {s['name']}, press Enter to keep): ").strip()
            if new_name:
                s['name'] = new_name
            
            # Update marks?
            if input("   Update marks? (y/n): ").lower() == 'y':
                total_marks = 0
                for subject in s['marks']:
                    mark = get_valid_marks(subject)
                    s['marks'][subject] = mark
                    total_marks += mark
                
                s['total'] = total_marks
                s['percentage'] = round((total_marks / 500) * 100, 2)
                s['grade'] = calculate_grade(s['percentage'])
            
            save_data(students)
            print("✅ Student details updated successfully!")
            input("\nPress Enter to continue...")
            return

    print("❌ Student not found.")
    input("\nPress Enter to continue...")

def delete_student(students):
    """Deletes a student record."""
    print("\n--- 🗑️ Delete Student ---")
    roll_no = input("   Enter Roll Number to delete: ").strip()
    
    for i, s in enumerate(students):
        if s['roll_no'] == roll_no:
            confirm = input(f"   Are you sure you want to delete {s['name']}? (y/n): ").lower()
            if confirm == 'y':
                del students[i]
                save_data(students)
                print("✅ Student record deleted.")
            else:
                print("   Deletion cancelled.")
            input("\nPress Enter to continue...")
            return

    print("❌ Student not found.")
    input("\nPress Enter to continue...")

def export_data(students):
    """Exports student data to a text file."""
    print("\n--- 📤 Export Data ---")
    filename = "student_report.txt"
    try:
        with open(filename, 'w') as f:
            f.write("===== 🎓 Student Result Report =====\n\n")
            f.write(f"{'Roll No':<10} | {'Name':<20} | {'Total':<8} | {'%':<6} | {'Grade':<5}\n")
            f.write("-" * 60 + "\n")
            for s in students:
                f.write(f"{s['roll_no']:<10} | {s['name']:<20} | {s['total']:<8} | {s['percentage']:<6} | {s['grade']:<5}\n")
        print(f"✅ Data exported successfully to {filename}")
    except IOError as e:
        print(f"❌ Error exporting data: {e}")
    input("\nPress Enter to continue...")

def login():
    """Simple Login System."""
    clear_screen()
    print("===== 🔐 Login System =====")
    print("Default User: admin | Pass: password123")
    
    attempts = 3
    while attempts > 0:
        user = input("\nUsername: ")
        password = input("Password: ")
        
        if user == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("\n✅ Login Successful! Welcome.")
            time.sleep(1)
            return True
        else:
            attempts -= 1
            print(f"❌ Invalid Credentials. Attempts left: {attempts}")
    
    print("\n🚫 Access Denied. Exiting...")
    return False

def main_menu():
    """Main Menu Loop."""
    if not login():
        return

    # Load data once at the start
    students = load_data()

    while True:
        clear_screen()
        print("===========================================")
        print("   🎓 SMART STUDENT RESULT MANAGEMENT SYSTEM")
        print("===========================================")
        print("1. Add Student ➕")
        print("2. View All Students 📋")
        print("3. Search Student 🔍")
        print("4. Update Student ✏️")
        print("5. Delete Student 🗑️")
        print("6. Export Report 📤")
        print("7. Exit 🚪")
        print("===========================================")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            add_student(students)
        elif choice == '2':
            view_students(students)
        elif choice == '3':
            search_student(students)
        elif choice == '4':
            update_student(students)
        elif choice == '5':
            delete_student(students)
        elif choice == '6':
            export_data(students)
        elif choice == '7':
            print("\nExiting Program. Goodbye! 👋")
            break
        else:
            print("❌ Invalid Choice! Please try again.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting...")
        sys.exit()
