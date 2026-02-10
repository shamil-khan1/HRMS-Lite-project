from extensions import db

class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50))
    amount = db.Column(db.Float)
    month = db.Column(db.String(20))
