from models.employee import Employee
from extensions import db


def get_all_employees():
    return Employee.query.all()


def create_employee(data):
    # check duplicate employee_code or email
    existing = Employee.query.filter(
        (Employee.employee_code == data["employee_code"]) |
        (Employee.email == data["email"])
    ).first()

    if existing:
        return None

    employee = Employee(
        employee_code=data["employee_code"],
        full_name=data["full_name"],
        email=data["email"],
        department=data["department"]
    )

    db.session.add(employee)
    db.session.commit()
    return employee


def delete_employee(employee_code):
    employee = Employee.query.filter_by(employee_code=employee_code).first()

    if not employee:
        return False

    db.session.delete(employee)
    db.session.commit()
    return True
