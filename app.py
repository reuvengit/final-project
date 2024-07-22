

from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

# MongoDB connection setup
mongo_host = os.getenv('MONGO_HOST', 'localhost')
client = MongoClient(host='mongo', port=27017)
db = client.Student_db
students_collection = db.students

@app.route('/')
def home():
    try:
        students = students_collection.find()
        students_list = list(students)
        print(f"Retrieved students: {students_list}")  # Add this line to print students to the logs
        return render_template('index.html', students=students_list)
    except Exception as e:
        print(f"Error: {e}")  # Add this line to print any error to the logs
        return str(e)

@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            'name': request.form['name'],
            'roll_number': request.form['roll_number'],
            'grade': request.form['grade']
        }
        try:
            students_collection.insert_one(student_data)
            print(f"Inserted student: {student_data}")  # Add this line to print inserted student to the logs
        except Exception as e:
            print(f"Error: {e}")  # Add this line to print any error to the logs
            return str(e)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = 5000)
