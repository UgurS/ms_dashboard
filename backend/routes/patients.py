from flask import Blueprint, request, jsonify
from backend.models.patient import Patient
from backend.models.base import db
from flask_jwt_extended import jwt_required

patients_bp = Blueprint('patients', __name__)


@patients_bp.route('/', methods=['GET'])
@jwt_required()
def get_patients():
    # Get page and per_page from query params, with defaults
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = Patient.query.paginate(page=page, per_page=per_page, error_out=False)

    patients = [p.to_dict() for p in pagination.items]

    return jsonify({
        "patients": patients,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
        "has_next": pagination.has_next,
        "has_prev": pagination.has_prev,
    })


@patients_bp.route('/', methods=['POST'])
@jwt_required()
def add_patient():
    data = request.get_json()
    patient = Patient(
        first_name=data['first_name'],
        last_name=data['last_name'],
        gender=data['gender'],
        date_of_birth=data['date_of_birth']
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201


@patients_bp.route('/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify(message="Patient deleted"), 200