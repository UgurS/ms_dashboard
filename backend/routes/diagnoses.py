from flask import Blueprint, request, jsonify
from backend.services.diagnosis_service import DiagnosisService
from backend.models.diagnosis import Diagnosis
from backend.models.patient import Patient
from backend.models.base import db
from flask_jwt_extended import jwt_required
import base64

diagnosis_bp = Blueprint('diagnosis', __name__)
diagnoser = DiagnosisService()


@diagnosis_bp.route('/', methods=['POST'])
def run_diagnosis():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "Missing image"}), 400

    result = diagnoser.predict(image_file)

    heatmap_base64 = base64.b64encode(result["heatmap"]).decode('utf-8')

    return jsonify({
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "heatmap_base64": heatmap_base64
    })


@diagnosis_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_diagnoses():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Diagnosis.query.order_by(Diagnosis.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    diagnoses = pagination.items
    results = []
    for diag in diagnoses:
        patient = Patient.query.get(diag.patient_id)
        results.append({
            "id": diag.id,
            "patient": f"{patient.first_name} {patient.last_name}" if patient else "Unknown",
            "date": diag.created_at.strftime('%Y-%m-%d'),
            "diagnosis": diag.prediction,
            "confidence": f"{int(diag.confidence * 100)}%"
        })
    return jsonify({
        "diagnoses": results,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    })
