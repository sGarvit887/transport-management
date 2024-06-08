from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import time

app = Flask(__name__)
app.secret_key = '20242024'

def get_db_connection():
    conn = sqlite3.connect('students.db', timeout=10)  # Setting a timeout of 10 seconds
    conn.row_factory = sqlite3.Row
    return conn

def execute_db_command(command, args=(), commit=True, retry=5, delay=1):
    for i in range(retry):
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute(command, args)
            if commit:
                conn.commit()
            result = c.fetchall()
            conn.close()
            return result
        except sqlite3.OperationalError as e:
            if 'database is locked' in str(e) and i < retry - 1:
                time.sleep(delay)
            else:
                raise
        except Exception as e:
            print("Error executing database command:", e)
            raise

def add_student(name, dob, mobile, admission_number, pickup_location):
    if student_exists(admission_number):
        return False
    command = '''
        INSERT INTO students (name, dob, mobile, admission_number, pickup_location) 
        VALUES (?, ?, ?, ?, ?)
    '''
    execute_db_command(command, (name, dob, mobile, admission_number, pickup_location))
    return True

def student_exists(admission_number):
    command = 'SELECT * FROM students WHERE admission_number = ?'
    result = execute_db_command(command, (admission_number,), commit=False)
    return bool(result)

def get_student(admission_number):
    command = 'SELECT * FROM students WHERE admission_number = ?'
    result = execute_db_command(command, (admission_number,), commit=False)
    return result[0] if result else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student_route():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        mobile = request.form['mobile']
        admission_number = request.form['admission_number']
        pickup_location = request.form['pickup_location']
        if add_student(name, dob, mobile, admission_number, pickup_location):
            flash('Student added successfully!', 'success')
        else:
            flash('Admission number already exists.', 'danger')
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/search_student', methods=['GET', 'POST'])
def search_student_route():
    student = None
    message = None
    if request.method == 'POST':
        admission_number = request.form['admission_number']
        student = get_student(admission_number)
        if not student:
            message = "Student not found."
    return render_template('search_student.html', student=student, message=message)

@app.route('/locate_pickup_location/<admission_number>')
def locate_pickup_location(admission_number):
    student = get_student(admission_number)
    if student:
        return render_template('maps.html', admission_number=admission_number, pickup_location=student['pickup_location'])
    else:
        return "Student not found."

if __name__ == '__main__':
    app.run(debug=True)
