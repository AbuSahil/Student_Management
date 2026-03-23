from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime   

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Student model
class Student(db.Model):
    # __tablename__ = 'student'   # ✅ explicit table name
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    last = db.Column(db.String(200), nullable=False)
    father = db.Column(db.String(500), nullable=False)
    mother = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    std = db.Column(db.String(10), nullable=False)
    roll = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.Date, default=date.today)   # ✅ correct default

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

# Route for adding and listing students
@app.route('/', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        # Convert DOB string to date object
        dob = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()

        new_student = Student(
            name=request.form['name'],
            last=request.form['last'],
            father=request.form['father'],
            mother=request.form['mother'],
            dob=dob,
            phone=request.form['phone'],
            pin=request.form['pin'],
            std=request.form['std'],
            roll=request.form['roll']
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect("/")

    class_students = Student.query.all()
    return render_template("add.html", class_student=class_students)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method == "POST":
        # parse and update fields
        name = request.form['name']
        last = request.form['last']
        father = request.form['father']
        mother = request.form['mother']
        dob = datetime.strptime(request.form['dob'], "%Y-%m-%d").date()
        phone = request.form['phone']
        pin = request.form['pin']
        std = request.form['std']
        roll = request.form['roll']
        class_student= Student.query.filter_by(sno=sno).first()
        class_student.name=name
        class_student.last=last
        class_student.father=father
        class_student.mother=mother
        class_student.dob=dob
        class_student.phone=phone
        class_student.pin=pin
        class_student.std=std
        class_student.roll=roll
        db.session.add(class_student)
        db.session.commit()
        return redirect("/")
       
    student = Student.query.filter_by(sno=sno).first()
    return render_template("update.html", student=student)

@app.route('/delete/<int:sno>')
def delete(sno):
    class_student = Student.query.filter_by(sno=sno).first()
    db.session.delete(class_student)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # creates todo.db and tables if not exist
    app.run(port=5000, debug=True)