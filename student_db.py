import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Return results as dictionary-like objects
        return conn

    def init_db(self):
        """Initialize the database tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    roll_no TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    class TEXT,
                    section TEXT,
                    math REAL,
                    physics REAL,
                    chemistry REAL,
                    english REAL,
                    computer REAL,
                    total REAL,
                    percentage REAL,
                    grade TEXT
                )
            """)
            conn.commit()

    def add_student(self, student_data):
        """Add a new student record."""
        sql = """
            INSERT INTO students (roll_no, name, class, section, math, physics, chemistry, english, computer, total, percentage, grade)
            VALUES (:roll_no, :name, :class, :section, :math, :physics, :chemistry, :english, :computer, :total, :percentage, :grade)
        """
        # Flatten marks for SQL
        data = student_data.copy()
        marks = data.pop('marks')
        data.update({
            'math': marks.get('Mathematics', 0),
            'physics': marks.get('Physics', 0),
            'chemistry': marks.get('Chemistry', 0),
            'english': marks.get('English', 0),
            'computer': marks.get('Computer Science', 0)
        })
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, data)
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def update_student(self, roll_no, student_data):
        """Update an existing student record."""
        sql = """
            UPDATE students 
            SET name=:name, class=:class, section=:section, 
                math=:math, physics=:physics, chemistry=:chemistry, english=:english, computer=:computer,
                total=:total, percentage=:percentage, grade=:grade
            WHERE roll_no=:roll_no
        """
        data = student_data.copy()
        marks = data.pop('marks')
        data.update({
            'math': marks.get('Mathematics', 0),
            'physics': marks.get('Physics', 0),
            'chemistry': marks.get('Chemistry', 0),
            'english': marks.get('English', 0),
            'computer': marks.get('Computer Science', 0)
        })
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()

    def delete_student(self, roll_no):
        """Delete a student by Roll No."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE roll_no = ?", (roll_no,))
            conn.commit()

    def get_all_students(self):
        """Retrieve all students as a list of dictionaries."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            
            students = []
            for row in rows:
                r = dict(row)
                # Reconstruct nested marks structure
                r['marks'] = {
                    'Mathematics': r['math'],
                    'Physics': r['physics'],
                    'Chemistry': r['chemistry'],
                    'English': r['english'],
                    'Computer Science': r['computer']
                }
                # Remove flat mark keys to match app structure
                for k in ['math', 'physics', 'chemistry', 'english', 'computer']:
                    del r[k]
                students.append(r)
            return students

    def get_student(self, roll_no):
        """Retrieve a single student."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE roll_no = ?", (roll_no,))
            row = cursor.fetchone()
            if row:
                r = dict(row)
                r['marks'] = {
                    'Mathematics': r['math'],
                    'Physics': r['physics'],
                    'Chemistry': r['chemistry'],
                    'English': r['english'],
                    'Computer Science': r['computer']
                }
                for k in ['math', 'physics', 'chemistry', 'english', 'computer']:
                    del r[k]
                return r
            return None
