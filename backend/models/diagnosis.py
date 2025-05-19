from backend.models.base import db


class Diagnosis(db.Model):
    __tablename__ = 'diagnoses'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    prediction = db.Column(db.String(10), nullable=False)  # "MSP" or "HC"
    confidence = db.Column(db.Float, nullable=False)
    model_used = db.Column(db.String(32), nullable=False)  # e.g. "mobilenet_v2"
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    samples = db.relationship('Sample', backref='diagnosis', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "admin_id": self.admin_id,
            "prediction": self.prediction,
            "confidence": self.confidence,
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat()
        }