from extensions import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    department = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100))
    salary = db.Column(db.Float)
    
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Employee {self.full_name}>"
