from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from datetime import date

from config import Config
from extensions import db

from models.employee import Employee
from models.attendance import Attendance

from routes.auth_routes import auth_bp
from routes.employee_routes import employee_bp
from routes.attendance_routes import attendance_bp
from routes.leave_routes import leave_bp
from routes.salary_routes import salary_bp


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = "super-secret-key"

# init db
db.init_app(app)

# register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(leave_bp)
app.register_blueprint(salary_bp)


# 🔐 Login required
@app.before_request
def require_login():
    allowed_routes = ["auth.login", "static"]
    if request.endpoint not in allowed_routes and "user_id" not in session:
        return redirect(url_for("auth.login"))


# 🏠 Home
@app.route("/")
def home():
    return redirect(url_for("dashboard"))


# 📊 Dashboard
@app.route("/dashboard")
def dashboard():
    today = date.today()

    total_employees = Employee.query.count()

    present_count = Attendance.query.filter_by(
        status="Present",
        date=today
    ).count()

    absent_count = Attendance.query.filter_by(
        status="Absent",
        date=today
    ).count()

    return render_template(
        "dashboard.html",
        total_employees=total_employees,
        present_count=present_count,
        absent_count=absent_count
    )


# 👨‍💼 Employees Page
@app.route("/employees-page")
def employees_page():
    employees = Employee.query.all()
    return render_template("employees.html", employees=employees)


# 📅 Attendance Page
@app.route("/attendance-page")
def attendance_page():
    attendance = Attendance.query.all()
    return render_template("attendance.html", attendance=attendance)


# 📡 Employees API
@app.route("/employees", methods=["GET"])
def get_employees():
    employees = Employee.query.all()
    return jsonify([
        {
            "id": e.id,
            "employee_code": e.employee_code,
            "full_name": e.full_name,
            "email": e.email,
            "department": e.department
        }
        for e in employees
    ])


# create tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)



