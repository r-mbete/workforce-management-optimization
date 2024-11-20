from app import db

# Employee Model
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    education_level = db.Column(db.String(50), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    years_experience = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Employee {self.name}>'

# Prediction Model
class Prediction(db.Model):
    __tablename__ = 'predictions'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    performance_rating = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    employee = db.relationship('Employee', backref=db.backref('predictions', lazy=True))

    def __repr__(self):
        return f'<Prediction {self.performance_rating} for {self.employee.name}>'
