from backend.models.base import db


class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(64), nullable=False, unique=True)
    gender = db.Column(db.String(16), nullable=False)

    diagnoses = db.relationship('Diagnosis', backref='patient', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "patient_code": self.patient_code,
            "gender": self.gender,
        }