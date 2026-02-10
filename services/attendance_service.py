from models.attendance import Attendance
from extensions import db

def mark_attendance(data):
    attendance = Attendance(**data)
    db.session.add(attendance)
    db.session.commit()
    return attendance


def get_attendance_by_employee(employee_code):
    return Attendance.query.filter_by(employee_code=employee_code).all()
