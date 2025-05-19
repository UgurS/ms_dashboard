from backend.models.patient import Patient
from backend.models.base import db


class PatientService:
    def add_patient(self, data):
        patient = Patient(
            first_name=data['first_name'],
            last_name=data['last_name'],
            gender=data['gender'],
            date_of_birth=data['date_of_birth']
        )
        db.session.add(patient)
        db.session.commit()
        return patient.to_dict()

    def get_all_patients(self):
        return [p.to_dict() for p in Patient.query.all()]

    def delete_patient(self, patient_id):
        patient = Patient.query.get_or_404(patient_id)
        db.session.delete(patient)
        db.session.commit()
        return {"message": "Patient deleted"}
