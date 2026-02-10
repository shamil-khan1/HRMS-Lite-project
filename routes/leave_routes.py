from flask import Blueprint, request, render_template, redirect
from extensions import db
from models.leave import Leave

leave_bp = Blueprint("leave", __name__)

@leave_bp.route("/leave-page")
def leave_page():
    leaves = Leave.query.all()
    return render_template("leave.html", leaves=leaves)


@leave_bp.route("/leave/apply", methods=["POST"])
def apply_leave():

    employee_code = request.form["employee_code"]
    reason = request.form["reason"]

    new_leave = Leave(
        employee_code=employee_code,
        reason=reason
    )

    db.session.add(new_leave)
    db.session.commit()

    return redirect("/leave-page")
