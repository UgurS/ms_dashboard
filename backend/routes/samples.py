from flask import Blueprint, request, jsonify
from backend.services.sample_service import SampleService
from flask_jwt_extended import jwt_required

samples_bp = Blueprint('samples', __name__)
sample_service = SampleService()


@samples_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_sample():
    image_file = request.files['file']
    patient_id = request.form['patient_id']

    blob_url = sample_service.upload_sample(image_file, patient_id)
    return jsonify(blob_url=blob_url), 201
