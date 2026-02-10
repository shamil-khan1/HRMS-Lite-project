from extensions import db
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from models.employee import Employee
from services.employee_service import (
    create_employee,
    get_all_employees,
    delete_employee
)

employee_bp = Blueprint("employee", __name__)

# ---------------- API ROUTES ----------------

@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    employees = get_all_employees()

    data = []
    for emp in employees:
        data.append({
            "employee_code": emp.employee_code,
            "full_name": emp.full_name,
            "email": emp.email,
            "department": emp.department
        })

    return jsonify(data), 200


@employee_bp.route("/employees", methods=["POST"])
def add_employee_api():
    data = request.json
    employee = create_employee(data)

    if not employee:
        return jsonify({"error": "Employee already exists"}), 400

    return jsonify({"message": "Employee created successfully"}), 201


@employee_bp.route("/employees/<employee_code>", methods=["DELETE"])
def remove_employee_api(employee_code):
    deleted = delete_employee(employee_code)

    if not deleted:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee deleted"}), 200


# ---------------- HTML ROUTES ----------------

@employee_bp.route("/employees/page", methods=["GET"])
def employee_page():
    employees = get_all_employees()
    return render_template("employees.html", employees=employees)


@employee_bp.route("/employees/page", methods=["POST"])
def add_employee_page():
    data = {
        "employee_code": request.form["employee_code"],
        "full_name": request.form["full_name"],
        "email": request.form["email"],
        "department": request.form["department"]
    }

    create_employee(data)
    return redirect(url_for("employee.employee_page"))


@employee_bp.route("/employees/page/delete/<employee_code>")
def delete_employee_page(employee_code):
    delete_employee(employee_code)
    return redirect(url_for("employee.employee_page"))


@employee_bp.route("/employees/edit/<employee_code>", methods=["GET", "POST"])
def edit_employee(employee_code):
    

    emp = Employee.query.filter_by(employee_code=employee_code).first()

    if request.method == "POST":
        emp.full_name = request.form["full_name"]
        emp.email = request.form["email"]
        emp.department = request.form["department"]

        db.session.commit()
        return redirect("/employees-page")

    return render_template("edit_employee.html", emp=emp)

@employee_bp.route("/employees/add", methods=["POST"])
def add_employee():

    employee_code = request.form["employee_code"]
    full_name = request.form["full_name"]
    email = request.form["email"]
    department = request.form["department"]

    new_employee = Employee(
        employee_code=employee_code,
        full_name=full_name,
        email=email,
        department=department
    )

    db.session.add(new_employee)
    db.session.commit()

    return redirect("/employees-page")

