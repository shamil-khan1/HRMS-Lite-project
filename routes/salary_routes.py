from flask import Blueprint, request, render_template, redirect
from extensions import db
from models.salary import Salary
from flask import send_file
from reportlab.pdfgen import canvas
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from models.employee import Employee
import io


salary_bp = Blueprint("salary", __name__)

@salary_bp.route("/salary-page")
def salary_page():
    salaries = Salary.query.all()
    return render_template("salary.html", salaries=salaries)


@salary_bp.route("/salary/add", methods=["POST"])
def add_salary():

    employee_code = request.form["employee_code"]
    amount = request.form["amount"]
    month = request.form["month"]

    new_salary = Salary(
        employee_code=employee_code,
        amount=amount,
        month=month
    )

    db.session.add(new_salary)
    db.session.commit()

    return redirect("/salary-page")





@salary_bp.route("/salary/payslip/<int:salary_id>")
def generate_payslip(salary_id):

    salary = Salary.query.get_or_404(salary_id)
    emp = Employee.query.filter_by(employee_code=salary.employee_code).first()

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Salary Payslip", styles['Title']))
    elements.append(Spacer(1,12))

    elements.append(Paragraph(f"Employee: {emp.full_name}", styles['Normal']))
    elements.append(Paragraph(f"Employee Code: {emp.employee_code}", styles['Normal']))
    elements.append(Paragraph(f"Month: {salary.month}", styles['Normal']))
    elements.append(Paragraph(f"Salary: {salary.amount}", styles['Normal']))

    doc.build(elements)

    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="payslip.pdf", mimetype='application/pdf')
