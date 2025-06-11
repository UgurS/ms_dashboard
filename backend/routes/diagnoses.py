from flask import Blueprint, request, jsonify
from backend.services.diagnosis_service import DiagnosisService
from backend.models.diagnosis import Diagnosis
from backend.models.patient import Patient
from backend.models.base import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import base64

diagnosis_bp = Blueprint('diagnosis', __name__)


@diagnosis_bp.route('/', methods=['POST'])
@jwt_required()
def run_diagnosis():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "Missing image"}), 400

    model_used = request.form.get('model_used')
    diagnoser = DiagnosisService(model_used)
    result = diagnoser.predict(image_file)

    heatmap_base64 = base64.b64encode(result["heatmap"]).decode('utf-8')

    # Save diagnosis to database
    patient_id = request.form.get('patient_id')
    admin_id = get_jwt_identity()
    if not patient_id:
        return jsonify({"error": "Missing patient_id"}), 400

    diagnosis = Diagnosis(
        patient_id=patient_id,
        admin_id=admin_id,
        prediction=result["prediction"],
        confidence=result["confidence"],
        heatmap_base64=heatmap_base64,
        model_used=model_used
    )

    db.session.add(diagnosis)
    db.session.commit()

    return jsonify({
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "heatmap_base64": heatmap_base64
    })

@diagnosis_bp.route('/<int:diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis_report(diagnosis_id):
    diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
    patient = Patient.query.get(diagnosis.patient_id)

    return jsonify({
        "id": diagnosis.id,
        "prediction": diagnosis.prediction,
        "confidence": diagnosis.confidence,
        "model_used": diagnosis.model_used,
        "heatmap_base64": diagnosis.heatmap_base64,  # store this when saving diagnosis
        "patient_code": patient.patient_code if patient else "Unknown"
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
            "patient_code": patient.patient_code if patient else "Unknown",
            "date": diag.created_at.strftime('%Y-%m-%d'),
            "diagnosis": diag.prediction,
            "confidence": f"{int(diag.confidence * 100)}%",
            "model_used": diag.model_used,
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
@diagnosis_bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_diagnoses_for_patient(patient_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Diagnosis.query.filter_by(patient_id=patient_id).order_by(Diagnosis.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    diagnoses = pagination.items
    results = []
    for diag in diagnoses:
        patient = Patient.query.get(diag.patient_id)
        results.append({
            "id": diag.id,
            "patient_code": patient.patient_code if patient else "Unknown",
            "date": diag.created_at.strftime('%Y-%m-%d'),
            "diagnosis": diag.prediction,
            "confidence": f"{int(diag.confidence * 100)}%",
            "model_used": diag.model_used,
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