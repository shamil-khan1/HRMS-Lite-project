from extensions import db
from datetime import date

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50))
    reason = db.Column(db.String(200))
    leave_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default="Pending")
