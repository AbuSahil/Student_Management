from flask import Flask, render_template, request, redirect,session,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime   

app = Flask(__name__)
app.secret_key='secret123'
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
    roll = db.Column(db.Integer, unique=True)
    date_created = db.Column(db.Date, default=date.today)   # ✅ correct default

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

class User(db.Model):
    __tablenmae__ = 'users'
    sno = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(50), nullable=False)
    role=db.Column(db.String(50),nullable=False)    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Get user by username
        user = User.query.filter_by(username=username).first()

        # Check user exists
        if not user:
            return render_template('login.html', error="User not found ❌")

        # Check password
        if user.password != password:
            return render_template('login.html', error="Wrong password ❌")

        # Store session
        session['user'] = user.username
        session['role'] = user.role

        # Redirect based on role
        if user.role == 'admin':
            return redirect('/admin_dashboard')
        elif user.role == 'teacher':
            return redirect('/teacher_dashboard')
        elif user.role == 'student':
            return redirect('/student_dashboard')

    return render_template('login.html')


# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()   # Remove all session data
    return redirect('/login')
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
@app.route('/login', methods=['POST','GET'])
def login():
    if request.form=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query

    return render_template('/login.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # creates todo.db and tables if not exist
    app.run(host='0.0.0.0',port=5000, debug=True)