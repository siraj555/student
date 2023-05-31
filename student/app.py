from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roll_number = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)


@app.route('/api/students/', methods=['GET'])
def get_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        student_data = {
            'id': student.id,
            'roll_number': student.roll_number,
            'name': student.name,
            'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d')
        }
        student_list.append(student_data)
    return jsonify(student_list)


@app.route('/api/student/add/', methods=['POST'])
def add_student():
    data = request.get_json()
    roll_number = data.get('roll_number')
    name = data.get('name')
    date_of_birth = data.get('date_of_birth')

    student = Student(roll_number=roll_number, name=name, date_of_birth=date_of_birth)
    db.session.add(student)
    db.session.commit()

    return jsonify({'message': 'Student added successfully.'})


@app.route('/api/student/<int:pk>/', methods=['GET'])
def get_student(pk):
    student = Student.query.get(pk)
    if not student:
        return jsonify({'message': 'Student not found.'}), 404

    student_data = {
        'id': student.id,
        'roll_number': student.roll_number,
        'name': student.name,
        'date_of_birth': student.date_of_birth.strftime('%Y-%m-%d')
    }
    return jsonify(student_data)


@app.route('/api/student/<int:pk>/add-mark/', methods=['POST'])
def add_mark(pk):
    student = Student.query.get(pk)
    if not student:
        return jsonify({'message': 'Student not found.'}), 404

    data = request.get_json()
    mark = data.get('mark')

    # Add your mark saving logic here

    return jsonify({'message': 'Mark added successfully.'})


@app.route('/api/student/<int:pk>/mark/', methods=['GET'])
def get_student_mark(pk):
    student = Student.query.get(pk)
    if not student:
        return jsonify({'message': 'Student not found.'}), 404

    # Retrieve the student's mark based on the pk value

    return jsonify({'message': 'Student mark fetched successfully.'})


@app.route('/api/student/results/', methods=['GET'])
def get_results():
    # Calculate and retrieve the analyzed report based on the mentioned conditions

    return jsonify({'message': 'Results fetched successfully.'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
