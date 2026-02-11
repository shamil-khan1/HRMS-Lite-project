import os
from flask import Flask, jsonify, render_template, session, redirect, url_for, request
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


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = "super-secret-key"

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(salary_bp)

    @app.before_request
    def require_login():
        allowed_routes = ["auth.login", "static"]
        if "user_id" not in session and request.endpoint not in allowed_routes:
            return redirect(url_for("auth.login"))

    @app.route("/")
    def home():
        return redirect(url_for("dashboard"))

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

    @app.route("/employees-page")
    def employees_page():
        employees = Employee.query.all()
        return render_template("employees.html", employees=employees)

    @app.route("/attendance-page")
    def attendance_page():
        attendance = Attendance.query.all()
        return render_template("attendance.html", attendance=attendance)

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

    with app.app_context():
        if os.environ.get("RENDER") != "true":
            with app.app_context():
                return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
