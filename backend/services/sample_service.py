import os
import uuid

from backend.models.base import db
from backend.models.sample import Sample

UPLOAD_FOLDER = "uploads"


class SampleService:
    def __init__(self):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def upload_sample(self, image_file, patient_id):
        filename = f"{patient_id}_{uuid.uuid4()}.jpg"
        path = os.path.join(UPLOAD_FOLDER, filename)

        with open(path, 'wb') as f:
            f.write(image_file.read())

        sample = Sample(
            image_url=path,
            diagnosis_id=None
        )
        db.session.add(sample)
        db.session.commit()

        return path
