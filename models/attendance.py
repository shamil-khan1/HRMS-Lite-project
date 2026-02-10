from extensions import db
from datetime import date

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50))
    status = db.Column(db.String(20))
    date = db.Column(db.Date, default=date.today)

