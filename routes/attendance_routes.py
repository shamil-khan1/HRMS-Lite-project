from flask import Blueprint, request, jsonify
from extensions import db
from models.attendance import Attendance
from utils.validators import is_valid_status
from services.attendance_service import mark_attendance

attendance_bp = Blueprint("attendance", __name__)

@attendance_bp.route("/", methods=["POST"])
def add_attendance():
    data = request.json
    mark_attendance(data)
    return jsonify({"message": "Attendance marked"}), 201

@attendance_bp.route("/", methods=["POST"])
def add_attendance():
    data = request.json

    if not is_valid_status(data["status"]):
        return jsonify({"error": "Invalid attendance status"}), 400

    mark_attendance(data)
    return jsonify({"message": "Attendance marked"}), 201

from flask import Blueprint, render_template, request, redirect
from services.attendance_service import mark_attendance

attendance_bp = Blueprint("attendance", __name__)

# 👉 Attendance Page
@attendance_bp.route("/attendance", methods=["GET"])
def attendance_page():
    return render_template("attendance.html")

# 👉 Mark Attendance
@attendance_bp.route("/attendance", methods=["POST"])
def submit_attendance():
    data = {
        "employee_code": request.form["employee_code"],
        "date": request.form["date"],
        "status": request.form["status"]
    }

    mark_attendance(data)
    return redirect("/attendance")

@attendance_bp.route("/attendance/add", methods=["POST"])
def add_attendance():

    employee_code = request.form["employee_code"]
    status = request.form["status"]

    new_attendance = Attendance(
        employee_code=employee_code,
        status=status
    )

    db.session.add(new_attendance)
    db.session.commit()

    return redirect("/attendance-page")


