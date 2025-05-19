from backend.models.base import db


class Sample(db.Model):
    __tablename__ = 'samples'

    id = db.Column(db.Integer, primary_key=True)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnoses.id'), nullable=False)
    image_url = db.Column(db.String, nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "diagnosis_id": self.diagnosis_id,
            "image_url": self.image_url,
            "uploaded_at": self.uploaded_at.isoformat()
        }