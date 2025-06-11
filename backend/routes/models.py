from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from backend.services.models.model_factory import ModelFactory

models_bp = Blueprint('models', __name__)
model_factory = ModelFactory()


@models_bp.route('/', methods=['GET'])
@jwt_required()
def get_models():
    models_info = model_factory.get_all_model_info()
    results = []
    for model in models_info:
        results.append({
            "model_name": model.model_name,
            "display_name": model.display_name,
            "train_set": model.train_set,
            "test_set": model.test_set
        })
    return jsonify(results)
