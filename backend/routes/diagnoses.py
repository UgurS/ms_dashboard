from flask import Blueprint, request, jsonify
from backend.services.diagnosis_service import DiagnosisService
import base64

diagnosis_bp = Blueprint('diagnosis', __name__)
diagnoser = DiagnosisService()


@diagnosis_bp.route('/', methods=['POST'])
def run_diagnosis():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({"error": "Missing image"}), 400

    result = diagnoser.predict(image_file)

    # Encode heatmap as base64 string to return in JSON
    heatmap_base64 = base64.b64encode(result["heatmap"]).decode('utf-8')

    return jsonify({
        "prediction": result["prediction"],
        "confidence": result["confidence"],
        "heatmap_base64": heatmap_base64
    })
